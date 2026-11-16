---
name: job-hunt
description: "Run a job-search batch for any job seeker, in any country or occupation, using their saved profile. Discovers live openings, applies hard filters, researches each company and its employee reviews, scores fit on a 100-point framework, picks a resume variant, and logs every role in the profile's tracker. Use this whenever the user says \"run a batch\", \"find me jobs\", \"search for roles\", \"what's out there for me\", \"job hunt\", or names a profile and asks for openings, even if they never say \"batch\". If no job-hunt workspace or profile exists yet, hand off to the setup skill first."
---

# Job Hunt — batch engine

This skill finds, filters, researches, scores and logs jobs for one profile at a time. It writes nothing about a person that the person has not confirmed, and it submits nothing without the approval the profile's autonomy level requires.

Sibling skills in this plugin:
- `setup` creates workspaces and profiles. Run it when anything below is missing.
- `resume-lab` audits resumes and runs JD match / Estimated ATS Compatibility.
- `tailor` drafts resumes, cover letters and application answers.
- `follow-up` reviews the pipeline after applications go out.

This skill runs on any agent platform. Wherever it says "search the web", "open a page", "use a browser" or "read a file", use whatever web search, page-reading, browser and file tools the current environment provides. If a capability is missing, say so in the run report and carry on with what is available.

**Paths.** Every path below is relative to the workspace root, the `job-hunt/` folder that `WORKSPACE.md` sits in. Run commands from there.

**The tracker script.** When the plugin is installed whole, it is `<this-skill-dir>/scripts/tracker.py`. Sibling skills reach it at `<their-skill-dir>/../job-hunt/scripts/tracker.py`, or at `<their-skill-dir>/scripts/tracker.py` when they were uploaded as standalone skills. It needs Python 3 and `openpyxl`.

## 1. Load the workspace

Locate the candidate workspace: a `job-hunt/` folder in the working directory or a folder the user points to, or a connected Drive folder or Google Sheet when the user chose cloud storage. If the session keeps no files between conversations, ask the user to upload their workspace zip. `WORKSPACE.md` (or the connected tracker) names the active profile and the available profiles.

- If the user named a profile, use it. Otherwise use the active profile.
- If no candidate workspace/profile exists, hand off to `setup` before searching.

Read, in this order, before evaluating anything:
1. `rules.md` (or the connected `Agent Rules` equivalent): region, currency, compensation bands, scoring weights, thresholds, autonomy, batch size, target roles, hard filters, approval triggers and positioning guardrails.
2. `profile.md` (or the connected `Candidate Profile` equivalent): the confirmed facts. This is the truth anchor for everything downstream.
3. `references/regions/<region>.md` for each region in the rules. Use `_global.md` when nothing more specific exists.
4. The active tracker so you know what has already been seen and can avoid duplicates. If the tracker is a local XLSX, use the bundled tracker script when useful. If it is Google Sheets, use the connected Google Drive/Sheets integration and preserve its structure.

If rules and tracker metadata disagree on weights, surface the drift and use the tracker's live schema for arithmetic unless the user tells you otherwise.

## 2. Discover

Default batch size comes from `rules.md` (`batch_size`). Fifteen is a sane default; thirty researched roles take a long time. A batch is a research target, never an application quota.

Use the environment's web search and page reading, and a browser tool where one is available and a page needs it. Search with the region pack's job boards plus company career pages for the target roles. Vary queries by role title, synonyms, seniority words and location. Prefer postings from the last 21 days. Older listings are often filled or ghost postings, so record the posted date. Flag anything older than `max_posting_age_days` from `rules.md` (default 30) in Notes.

Open and read the full job description before you score anything. A search snippet is not a JD. If the full JD will not load, log the role with `status: Found`, note "JD unreadable" in Notes, and do not score it.

## 3. Filter, then de-duplicate

Apply the hard filters in `rules.md` first. A hard-filter failure means `decision: SKIP`, scores left blank, and the failed filter named in `hard_filter`. Hard filters are absolute. If the user wants an exception, they edit the rule.

Common hard filters (only the ones the user chose apply): pay below floor, location outside allowed set, onsite when remote-only, experience demanded far beyond reality, required licence or language the user lacks, sponsorship needed but not offered, banned company.

Duplicate checking happens automatically when you add rows, by normalised URL and by company plus role plus location, so the same title posted in two cities is logged twice. Always fill `location`. Skip rows the tracker already holds, and say so in the summary.

## 4. Research the company

Read `references/review-research.md` before the first company in a batch. In short: look for patterns repeated across several reviews and sources, weigh recent reviews above old ones, separate one angry review from a pattern, and record how strong your evidence is (`Strong`, `Moderate`, `Thin`, `None`). Many review sites block automated reading. When you cannot read them, say so, score Reviews at the neutral midpoint, and mark evidence `Thin` or `None`. Never invent review content.

## 5. Score

Read `references/scoring.md` for the rubric. Score each dimension as an integer from 0 to the profile's weight for it. The Total is computed by the tracker. Map the total to a Decision using the profile's thresholds (defaults: 80 PRIORITY APPLY, 70 APPLY, 60 STRETCH / REVIEW, below that SKIP).

Score against the person's real experience in `profile.md`, never against the version of them that would be convenient. If a role wants five years and they have one, Skills Fit drops, and the summary says why.

## 6. Pick a resume variant

`profile.md` lists the user's variants and what each emphasises. Pick the one whose emphasis best matches the JD's top three responsibilities. On a tie, prefer the variant aligned with the user's primary direction in `rules.md`. Record the variant name in the tracker.

## 7. Log every processed role

Write a JSON array of rows to a scratch file outside the workspace (any temp or scratch directory the environment offers) and add it in one call:

```bash
python <this-skill-dir>/scripts/tracker.py add profiles/<slug>/<tracker> <scratch-dir>/batch.json
```

Text that starts with `=`, `+`, `-` or `@` is stored as plain text, so scraped content can never become a live spreadsheet formula.

Row fields: `company`, `role`, `url`, `source`, `location`, `work_model`, `salary` (exactly as listed, or "Undisclosed"), `experience`, `posted`, the eight scores `s_role s_skills s_growth s_comp s_company s_reviews s_worklife s_location`, `decision`, `hard_filter`, `review_summary`, `red_flags`, `evidence`, `resume_variant`, `status`, `next_action`, `notes`.

Status values allowed: Found, Shortlisted, Awaiting Approval, Drafted, Applied, Assessment, Interviewing, Offer, Rejected, Withdrawn, Skipped, Closed. Use `Skipped` for SKIP decisions, `Shortlisted` for APPLY and PRIORITY APPLY, `Awaiting Approval` for anything that hits an approval trigger.

Read the script's output. Rejected rows mean you sent bad data, so fix them and re-add. Report duplicates instead of hiding them. Never claim the tracker was updated unless the script reported the row as added.

To change a row later:
```bash
python <this-skill-dir>/scripts/tracker.py update profiles/<slug>/<tracker> <ID> status=Applied next_action="Follow up on 14 Oct"
```

## 8. Apply, within the autonomy level

Read `references/application-controls.md` before any application step. The profile's `autonomy` setting decides how far you go:

- `research-only`: stop after logging.
- `draft` (default): for each APPLY and PRIORITY APPLY role:
  1. `resume-lab`, JD Match mode: score the chosen variant against the full JD and save the report to `profiles/<slug>/resume-lab/<company>-<role>-match.md`. This yields the safe keywords, the real gaps and the DO NOT ADD list.
  2. `tailor`: draft the resume, cover letter and form answers using that report, saved under `profiles/<slug>/applications/`.
  3. `resume-lab`, Improvement Pass (optional, worth it for PRIORITY APPLY): before/after compatibility plus a final truth audit.
  4. Set status `Drafted`. The user submits.

  If `resume-lab` is not installed, go straight to `tailor`.
- `assisted-apply`: with a browser tool available, fill applications only for roles the user approved in this conversation, pause before every final submit, and stop at anything on the never-autonomous list.

## 9. Close the batch

Save a short run report to `profiles/<slug>/runs/<date>-batch.md` and show it to the user:

- counts: found, filtered out, duplicates, scored, by decision
- the strongest three to five matches, each with one line on why
- roles waiting on the user's approval, with the trigger for each
- recurring gaps across the batch, such as a skill or credential many JDs asked for, so the user can decide whether to close it
- evidence caveats, such as review sites that blocked access
- the next action you recommend

Keep it short. The tracker holds the detail.
