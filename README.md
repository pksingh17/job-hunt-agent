<p align="center"><img src="assets/icon-256.png" width="128" alt="job-hunt-agent icon"></p>

# Job Hunt Agent

**v1.0.0 — First public release** · Open-source agent core · MIT License

An open-source career agent for anyone, in any country and any occupation. One set of skills runs on Claude (Claude Code, Cowork, claude.ai) and on ChatGPT / Codex, with a manifest for each platform.

You register once by answering an interview. After that, one sentence runs a full batch:

> Run a batch.

The agent finds live openings, drops the ones that break your dealbreakers, researches companies and employee reviews, scores every role on a transparent framework, runs Resume Lab against relevant jobs, prepares truthful applications, and keeps track of the pipeline.


## Platforms

Five skills: `setup`, `job-hunt`, `resume-lab`, `tailor` and `follow-up`. The skill text is platform-neutral: it asks for "web search", "a browser" and "file storage" and uses whatever the host provides. Each platform reads its own manifest:

| Platform | Manifest |
|---|---|
| Claude Code, Cowork | `.claude-plugin/plugin.json` (+ `marketplace.json`) |
| ChatGPT (Agent Plugins 1.0) | `plugin.json` |
| Codex | `.codex-plugin/plugin.json` |
| claude.ai chat, any skills-only host | standalone skill zips built by `tools/package_skills.py` |

Where available, the skills can also use connected Google Drive / Google Sheets, email and calendar. User-specific candidate data always stays outside the public core.

## What makes it different

- **It never lies for you.** Your confirmed facts are the ceiling. Tailoring can reorder and rephrase them and can never add a skill, number or job you don't have.
- **You stay in control.** By default it stops at drafts and you press submit. Anything unusual (relocation, bonds, night shifts, salary questions) comes back to you.
- **It's honest about evidence.** When a review site blocks it, the tracker says so instead of inventing a verdict.
- **Your data stays yours.** No project-operated server or telemetry. Profiles and trackers live in your chosen workspace, which may be local or hosted by your AI platform.
- **One person, many searches.** Run an industry search and an academic search side by side, each with its own rules and scoring weights.
- **Resume Lab is evidence-grounded.** Audit a resume, build one from confirmed facts, compare it with a JD, and get an **Estimated ATS Compatibility** score without pretending there is one universal ATS algorithm.

## Install

### Claude Code
```
/plugin marketplace add vivek-vankar/job-hunt-agent
/plugin install job-hunt-agent@job-hunt-agent
```

### Cowork (Claude Desktop)
Download this repository as a zip and upload it as a custom plugin from Cowork's Customize menu. Pick a working folder (ideally a synced one) when you start the session; your workspace will live there.

### claude.ai chat
Build standalone skill zips, then add each one under custom skills:
```
python tools/package_skills.py      # writes dist/setup.zip, dist/job-hunt.zip, ...
```
Don't zip the `skills/` folders by hand: the script copies the tracker into every skill that needs it, which a hand-made zip would miss. Chat sessions don't keep files between conversations, so setup hands you a workspace zip to download, and you upload it again next time.

### ChatGPT / Codex
Install from this repository using the platform's plugin flow. ChatGPT reads the root `plugin.json`; Codex reads `.codex-plugin/plugin.json`.

**Requirement:** Python 3 with `openpyxl` for the tracker (`pip install openpyxl`).

## First run

> Set me up.

Setup asks for your resume, has you confirm every fact it extracts, then asks about direction, pay, locations, dealbreakers and how much autonomy you want. It creates:

```
job-hunt/
├── WORKSPACE.md
└── profiles/<you>/
    ├── profile.md       confirmed facts (the truth anchor)
    ├── rules.md         targets, pay bands, filters, weights, autonomy
    ├── resumes/
    ├── resume-lab/      audits and JD-match reports
    ├── applications/    tailored drafts, one folder per role
    ├── runs/            batch reports
    └── tracker.xlsx     every role ever seen, with a live dashboard
```

## Everyday commands

| Say | What happens |
|---|---|
| `Run a batch` | Search, filter, research, score, log (default 15 roles) |
| `Run a batch of 30 on maria-uk` | Same, chosen size and profile |
| `Check my resume` | Resume Health audit with prioritized fixes |
| `Match my resume to this JD` | Estimated ATS Compatibility, gaps, safe keywords, and DO NOT ADD list |
| `Build me a resume` | Creates a resume from confirmed profile facts |
| `Tailor my application for #12` | Resume and cover letter drafts for tracker row 12 |
| `What should I do today?` | Pipeline review: approvals, follow-ups, interviews |
| `Prep me for the interview at Acme` | Company brief, likely questions, stories from your real experience |
| `Raise my salary floor to 45,000` | Edits rules.md |
| `Add a profile for academic jobs` | A second search with its own rules |

## Resume Lab

Resume Lab is the resume-intelligence layer:

- **Resume Audit** — structure, parsing safety, positioning, evidence, bullet quality and clarity
- **Estimated ATS Compatibility** — transparent JD-specific alignment score; never presented as a universal ATS score
- **JD Match** — strong matches, underrepresented confirmed experience, real gaps, and a `DO NOT ADD` list
- **Resume Builder** — creates a resume from the candidate's confirmed truth profile
- **Variant Builder** — maintains a small set of master resumes for meaningfully different target families
- **Improvement Pass** — compares before/after alignment without keyword stuffing or fabricating capability

The candidate truth profile is always the ceiling. Resume Lab can improve wording and emphasis; it cannot manufacture skills, metrics, employers, qualifications or results.

## Scoring

Eight dimensions, weights adjustable per profile (they must total 100):

Role fit 25 · Skills fit 15 · Growth 15 · Compensation 15 · Company 10 · Reviews 10 · Work-life 5 · Location 5

80+ PRIORITY APPLY · 70–79 APPLY · 60–69 STRETCH / REVIEW · below 60 SKIP. Hard filters override scores. Full rubric: `skills/job-hunt/references/scoring.md`.

## Autonomy levels

| Level | Does | Default |
|---|---|---|
| `research-only` | Finds, researches, scores, logs | |
| `draft` | Also prepares tailored materials; you submit | ✓ |
| `assisted-apply` | Also fills forms in a browser for roles you approved, pausing before each submit | |

Several job boards, LinkedIn among them, prohibit automated applications in their terms and can restrict accounts that use them. Choose `assisted-apply` knowing that. Some things are never automated at any level: passwords, OTPs, ID numbers, bank details, payments, legal declarations, and voluntary demographic / equal-opportunity questions.

## Region packs

`skills/job-hunt/references/regions/` holds country notes: job boards, review sites, pay conventions, local red flags. v1.0.0 includes India, UK, US, Germany and a global fallback. **Adding your country is the easiest way to contribute.** See CONTRIBUTING.md.

## Repository layout

```
.claude-plugin/        Claude Code / Cowork: plugin.json + marketplace.json
.codex-plugin/         Codex manifest
plugin.json            ChatGPT (Agent Plugins 1.0) manifest
tools/                 package_skills.py for standalone skill zips
skills/
  setup/               onboarding and profile management, templates
  job-hunt/            batch engine, scoring rubric, region packs, tracker.py
  resume-lab/          resume audit, builder, JD match, estimated ATS compatibility
  tailor/              truthful role-specific resumes, cover letters, form answers
  follow-up/           pipeline review and next actions
```

## Roadmap
- Optional Google Sheets and Notion tracker sync
- Web UI / career command center
- Outcome analytics that learn which resume variants and role families earn responses
- More region packs and occupation notes (healthcare, academia, trades)
- Interview-prep skill with mock interviews

## Brand assets
`assets/` holds the icon (SVG plus PNGs from 512 to 32px) and a 1280×640 `social-preview.png` for the repository's social preview image, set under the repo's Settings on GitHub.

## Contributors
Maintained jointly by the project contributors. Public identities/handles can be added later in `CONTRIBUTORS.md`; Git history remains the canonical contribution record.

## Release
This is the first public source release, **v1.0.0**. See [CHANGELOG.md](CHANGELOG.md) for what is included and [RELEASE_NOTES.md](RELEASE_NOTES.md) for known limitations. The project is currently a skill-based agent, not a hosted web service or finished UI.

## License
MIT. See LICENSE.
