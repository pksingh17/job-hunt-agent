#!/usr/bin/env python3
"""
tracker.py - deterministic read/write for a job-hunt-agent tracker workbook.

The agent never edits tracker.xlsx by hand. Every read and write goes through
this script, so formatting, dropdowns and Dashboard formulas survive every run.

Commands
  init   <tracker.xlsx> [--weights JSON]       create a fresh tracker
  list   <tracker.xlsx> [--status S ...]       print existing rows as JSON
  add    <tracker.xlsx> <rows.json>            append rows, skipping duplicates
  update <tracker.xlsx> <ID> <field=value>...  change fields on one row

Requires: openpyxl (pip install openpyxl)
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError:
    sys.exit("openpyxl is missing. Install it with: pip install openpyxl")

SHEET = "Job Tracker"
MAX_ROWS = 2000  # dropdowns and formulas are pre-applied down to this row

SCORE_KEYS = ["role", "skills", "growth", "comp", "company", "reviews", "worklife", "location"]
SCORE_LABELS = {
    "role": "Role Fit", "skills": "Skills Fit", "growth": "Growth", "comp": "Comp",
    "company": "Company", "reviews": "Reviews", "worklife": "Work-Life", "location": "Location",
}
DEFAULT_WEIGHTS = {"role": 25, "skills": 15, "growth": 15, "comp": 15,
                   "company": 10, "reviews": 10, "worklife": 5, "location": 5}

DECISIONS = ["PRIORITY APPLY", "APPLY", "STRETCH / REVIEW", "SKIP"]
STATUSES = ["Found", "Shortlisted", "Awaiting Approval", "Drafted", "Applied",
            "Assessment", "Interviewing", "Offer", "Rejected", "Withdrawn",
            "Skipped", "Closed"]
EVIDENCE = ["Strong", "Moderate", "Thin", "None"]

# (key, header, width) in column order. Score columns are inserted after "posted".
BASE_COLUMNS = [
    ("id", "ID", 7), ("found", "Date Found", 12), ("company", "Company", 22),
    ("role", "Role", 28), ("url", "Job URL", 34), ("source", "Source", 14),
    ("location", "Location", 18), ("work_model", "Work Model", 12),
    ("salary", "Salary (as listed)", 18), ("experience", "Experience Req.", 14),
    ("posted", "Posted Date", 12),
]
TAIL_COLUMNS = [
    ("total", "Total /100", 10), ("decision", "Decision", 16),
    ("hard_filter", "Hard Filter Fail", 22), ("review_summary", "Review Summary", 40),
    ("red_flags", "Red Flags", 30), ("evidence", "Review Evidence", 12),
    ("resume_variant", "Resume Variant", 16), ("applied", "Applied Date", 12),
    ("status", "Status", 16), ("next_action", "Next Action", 28),
    ("next_date", "Next Action Date", 14), ("notes", "Notes", 30),
]

HEADER_FILL = PatternFill("solid", fgColor="1F3A5F")
HEADER_FONT = Font(name="Arial", bold=True, color="FFFFFF")
BODY_FONT = Font(name="Arial", size=10)


def columns(weights):
    score_cols = [(f"s_{k}", f"{SCORE_LABELS[k]} /{weights[k]}", 10) for k in SCORE_KEYS]
    return BASE_COLUMNS + score_cols + TAIL_COLUMNS


def read_weights(ws):
    """Recover the weights a tracker was built with from its score headers."""
    weights = {}
    for cell in ws[1]:
        for k in SCORE_KEYS:
            m = re.fullmatch(rf"{re.escape(SCORE_LABELS[k])} /(\d+)", str(cell.value or ""))
            if m:
                weights[k] = int(m.group(1))
    return weights if len(weights) == len(SCORE_KEYS) else DEFAULT_WEIGHTS


def colmap(ws):
    """Map field key -> column index, using header text so it survives reordering."""
    weights = read_weights(ws)
    by_header = {h: k for k, h, _ in columns(weights)}
    out = {}
    for cell in ws[1]:
        key = by_header.get(cell.value)
        if key:
            out[key] = cell.column
    return out


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", str(text or "").lower()).strip()


def put(ws, row, col, value):
    """Write a cell. Text is always stored as text: openpyxl would otherwise turn
    any string starting with '=' (for example scraped web content) into a live formula."""
    cell = ws.cell(row=row, column=col)
    cell.value = value  # ws.cell(value=None) silently keeps the old value
    if isinstance(value, str) and value.startswith("="):
        cell.data_type = "s"
    return cell


def norm_url(url):
    u = str(url or "").strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = u.split("#")[0]
    # drop tracking parameters, keep ids that some boards put in the query
    if "?" in u:
        base, query = u.split("?", 1)
        keep = [p for p in query.split("&") if not p.startswith(("utm_", "ref", "src", "trk"))]
        u = base + ("?" + "&".join(keep) if keep else "")
    return u.rstrip("/")


# ----------------------------------------------------------------- init

def cmd_init(path, weights=None):
    weights = weights or DEFAULT_WEIGHTS
    if set(weights) != set(SCORE_KEYS):
        sys.exit(f"weights must have exactly these keys: {SCORE_KEYS}")
    if sum(weights.values()) != 100:
        sys.exit(f"weights must sum to 100 (got {sum(weights.values())})")
    if Path(path).exists():
        sys.exit(f"{path} already exists. Refusing to overwrite a tracker.")

    cols = columns(weights)
    wb = Workbook()
    ws = wb.active
    ws.title = SHEET

    for i, (_, header, width) in enumerate(cols, start=1):
        c = ws.cell(row=1, column=i, value=header)
        c.fill, c.font = HEADER_FILL, HEADER_FONT
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(cols))}1"

    idx = {k: i for i, (k, _, _) in enumerate(cols, start=1)}
    first = get_column_letter(idx["s_role"])
    last = get_column_letter(idx["s_location"])
    total_col = get_column_letter(idx["total"])

    def add_list(key, values):
        col = get_column_letter(idx[key])
        dv = DataValidation(type="list", formula1='"' + ",".join(values) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col}2:{col}{MAX_ROWS}")

    add_list("decision", DECISIONS)
    add_list("status", STATUSES)
    add_list("evidence", EVIDENCE)

    # Dashboard
    db = wb.create_sheet("Dashboard", 0)
    db["A1"], db["A1"].font = "Job Hunt Dashboard", Font(name="Arial", bold=True, size=14)
    tr = f"'{SHEET}'"
    dcol = get_column_letter(idx["decision"])
    scol = get_column_letter(idx["status"])
    ccol = get_column_letter(idx["company"])
    rng = lambda c: f"{tr}!${c}$2:${c}${MAX_ROWS}"
    rows = [
        ("Roles logged", f"=COUNTA({rng(ccol)})"),
        ("Priority apply", f'=COUNTIF({rng(dcol)},"PRIORITY APPLY")'),
        ("Apply", f'=COUNTIF({rng(dcol)},"APPLY")'),
        ("Stretch / review", f'=COUNTIF({rng(dcol)},"STRETCH / REVIEW")'),
        ("Skipped (decision)", f'=COUNTIF({rng(dcol)},"SKIP")'),
        ("Awaiting your approval", f'=COUNTIF({rng(scol)},"Awaiting Approval")'),
        ("Applied", f'=COUNTIF({rng(scol)},"Applied")'),
        ("Assessments", f'=COUNTIF({rng(scol)},"Assessment")'),
        ("Interviewing", f'=COUNTIF({rng(scol)},"Interviewing")'),
        ("Offers", f'=COUNTIF({rng(scol)},"Offer")'),
        ("Rejected", f'=COUNTIF({rng(scol)},"Rejected")'),
        ("Average fit score", f'=IFERROR(AVERAGEIF({rng(total_col)},">0"),"-")'),
    ]
    for r, (label, formula) in enumerate(rows, start=3):
        db.cell(row=r, column=1, value=label).font = BODY_FONT
        db.cell(row=r, column=2, value=formula).font = Font(name="Arial", bold=True)
    db.column_dimensions["A"].width = 26
    db.column_dimensions["B"].width = 12
    db["A17"] = "Edit rows on the Job Tracker tab. The agent writes through tracker.py; this tab updates itself."
    db["A17"].font = Font(name="Arial", italic=True, size=9, color="666666")
    db["A18"] = f"Scoring weights: " + ", ".join(f"{SCORE_LABELS[k]} {weights[k]}" for k in SCORE_KEYS)
    db["A18"].font = Font(name="Arial", italic=True, size=9, color="666666")

    wb.save(path)
    print(json.dumps({"created": str(path), "weights": weights}))


# ----------------------------------------------------------------- list

def load(path):
    if not Path(path).exists():
        sys.exit(f"{path} not found. Run: tracker.py init {path}")
    wb = load_workbook(path)
    if SHEET not in wb.sheetnames:
        sys.exit(f"{path} has no '{SHEET}' tab.")
    return wb, wb[SHEET]


def row_dict(ws, r, cmap):
    d = {k: ws.cell(row=r, column=c).value for k, c in cmap.items()}
    # Total is a formula; compute it here so callers get a number
    d["total"] = sum(int(d.get(f"s_{k}") or 0) for k in SCORE_KEYS)
    for k, v in list(d.items()):
        if hasattr(v, "isoformat"):
            d[k] = v.isoformat()[:10]
    return d


def last_row(ws, cmap):
    r = ws.max_row
    while r > 1 and not any(ws.cell(row=r, column=cmap[k]).value for k in ("company", "role", "url")):
        r -= 1
    return r


def cmd_list(path, statuses=None):
    _, ws = load(path)
    cmap = colmap(ws)
    out = []
    for r in range(2, last_row(ws, cmap) + 1):
        d = row_dict(ws, r, cmap)
        if statuses and d.get("status") not in statuses:
            continue
        out.append(d)
    print(json.dumps({"weights": read_weights(ws), "count": len(out), "rows": out},
                     ensure_ascii=False, indent=1, default=str))


# ----------------------------------------------------------------- add

def validate(row, weights):
    errors = []
    for k in SCORE_KEYS:
        v = row.get(f"s_{k}")
        if v is None:
            continue
        if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= weights[k]:
            errors.append(f"s_{k}={v!r} must be an integer 0..{weights[k]}")
    if row.get("decision") and row["decision"] not in DECISIONS:
        errors.append(f"decision {row['decision']!r} not in {DECISIONS}")
    if row.get("status") and row["status"] not in STATUSES:
        errors.append(f"status {row['status']!r} not in {STATUSES}")
    if row.get("evidence") and row["evidence"] not in EVIDENCE:
        errors.append(f"evidence {row['evidence']!r} not in {EVIDENCE}")
    if not (row.get("company") and row.get("role")):
        errors.append("company and role are required")
    return errors


def cmd_add(path, rows_file):
    wb, ws = load(path)
    cmap = colmap(ws)
    weights = read_weights(ws)
    rows = json.loads(Path(rows_file).read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = [rows]

    end = last_row(ws, cmap)
    # seen_pairs: (company, role) -> [(location, id), ...]. The same title at the
    # same company in a different city is a different opening, not a duplicate.
    seen_urls, seen_pairs, max_id = {}, {}, 0

    def pair_dup(pair, loc):
        for other_loc, other_id in seen_pairs.get(pair, []):
            # an unknown location on either side cannot prove the roles differ
            if not loc or not other_loc or loc == other_loc:
                return other_id
        return None

    for r in range(2, end + 1):
        d = row_dict(ws, r, cmap)
        if d.get("url"):
            seen_urls[norm_url(d["url"])] = d.get("id")
        seen_pairs.setdefault((norm(d.get("company")), norm(d.get("role"))), []).append(
            (norm(d.get("location")), d.get("id")))
        try:
            max_id = max(max_id, int(d.get("id") or 0))
        except (TypeError, ValueError):
            pass

    total_col = get_column_letter(cmap["total"])
    first = get_column_letter(cmap["s_role"])
    last = get_column_letter(cmap["s_location"])

    added, duplicates, rejected = [], [], []
    for row in rows:
        errs = validate(row, weights)
        if errs:
            rejected.append({"company": row.get("company"), "role": row.get("role"), "errors": errs})
            continue
        u = norm_url(row.get("url"))
        pair = (norm(row.get("company")), norm(row.get("role")))
        loc = norm(row.get("location"))
        dup_of = seen_urls.get(u) if u else None
        dup_of = dup_of or pair_dup(pair, loc)
        if dup_of is not None:
            duplicates.append({"company": row["company"], "role": row["role"], "existing_id": dup_of})
            continue

        end += 1
        max_id += 1
        row = dict(row)
        row["id"] = max_id
        row.setdefault("found", date.today().isoformat())
        row.setdefault("status", "Found")
        for key, col in cmap.items():
            if key == "total":
                cell = ws.cell(row=end, column=col, value=f"=SUM({first}{end}:{last}{end})")
            else:
                cell = put(ws, end, col, row.get(key))
            cell.font = BODY_FONT
            cell.alignment = Alignment(vertical="top", wrap_text=key in
                                       ("review_summary", "red_flags", "notes", "hard_filter", "next_action"))
        if u:
            seen_urls[u] = max_id
        seen_pairs.setdefault(pair, []).append((loc, max_id))
        added.append({"id": max_id, "company": row["company"], "role": row["role"]})

    wb.save(path)
    print(json.dumps({"added": added, "duplicates": duplicates, "rejected": rejected},
                     ensure_ascii=False, indent=1))


# ----------------------------------------------------------------- update

def cmd_update(path, row_id, assignments):
    wb, ws = load(path)
    cmap = colmap(ws)
    weights = read_weights(ws)
    target = None
    for r in range(2, last_row(ws, cmap) + 1):
        if str(ws.cell(row=r, column=cmap["id"]).value) == str(row_id):
            target = r
            break
    if target is None:
        sys.exit(f"No row with ID {row_id}")

    changes = {}
    for a in assignments:
        if "=" not in a:
            sys.exit(f"Bad assignment {a!r}; use field=value")
        k, v = a.split("=", 1)
        if k not in cmap or k in ("id", "total"):
            sys.exit(f"Unknown or protected field {k!r}. Fields: {sorted(set(cmap) - {'id', 'total'})}")
        if v == "":
            v = None  # an empty value clears the field
        elif k.startswith("s_"):
            try:
                v = int(v)
            except ValueError:
                sys.exit(f"Rejected: {k}={v!r} must be a whole number 0..{weights[k[2:]]}, "
                         f"or empty ({k}=) to clear it")
        changes[k] = v

    probe = row_dict(ws, target, cmap)
    probe.update(changes)
    errs = validate(probe, weights)
    if errs:
        sys.exit("Rejected: " + "; ".join(errs))

    if changes.get("status") == "Applied" and not probe.get("applied"):
        changes["applied"] = date.today().isoformat()
    for k, v in changes.items():
        put(ws, target, cmap[k], v)
    wb.save(path)
    print(json.dumps({"updated": row_id, "changes": changes}, ensure_ascii=False))


# ----------------------------------------------------------------- main

def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    cmd, path = argv[1], argv[2]
    if cmd == "init":
        weights = None
        if "--weights" in argv:
            weights = json.loads(argv[argv.index("--weights") + 1])
        cmd_init(path, weights)
    elif cmd == "list":
        statuses = argv[argv.index("--status") + 1:] if "--status" in argv else None
        cmd_list(path, statuses)
    elif cmd == "add" and len(argv) == 4:
        cmd_add(path, argv[3])
    elif cmd == "update" and len(argv) >= 5:
        cmd_update(path, argv[3], argv[4:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
