# Job Hunt Agent v1.0.0 — GitHub Release

**Release date:** 2026-11-16
**Git tag:** `v1.0.0`
**License:** MIT
**Status:** Initial repository release

## What is Job Hunt Agent?

An open-source, skills-based career agent for candidates in different industries and regions. It helps a user set up a verified profile, find and research jobs, assess fit, audit and tailor resumes truthfully, prepare applications, and track follow-ups.

## Highlights

1. **Candidate Setup** — personal constraints, targets and confirmed experience become reusable workspace files.
2. **Job Discovery and Research** — role filtering, transparent scores, employer-review research and ranked queues.
3. **Resume Lab** — resume audits, JD comparisons, resume drafting and Estimated ATS Compatibility with clear limitations.
4. **Application Assistance** — tailored truthful materials, explicit autonomy rules and human approval at sensitive steps.
5. **Pipeline Tracking** — spreadsheet tracker, follow-up workflow, recruiter replies and interview preparation.
6. **Platform Support** — manifests for ChatGPT, Codex, Claude Code/Cowork, plus a standalone-skill packaging script.

## Getting started

Read [README.md](README.md) for platform-specific installation. Start with `Set me up.` and confirm facts extracted from your resume before searching or tailoring.

For a downloadable standalone skill package, run:

```bash
python tools/package_skills.py
```

The tracker helper requires Python 3 and `openpyxl` (`pip install openpyxl`).

## Current limitations

- **No UI yet:** this release consists of plugin/skill instructions, reference files and a tracker script; a web dashboard is planned.
- **Not an autonomous job-board scraper:** search, live review-site access and form filling depend on the host environment and applicable site rules.
- **No universal ATS score:** the score is an explainable estimate based on the resume and job description.
- **No guaranteed applications or interviews:** verify submission status from the target site before marking applications as sent.
- **No bundled personal data:** user profiles, resumes, credentials and trackers must remain outside the repository.

## Planned next steps

Structured storage/API contracts, optional integrations, product UI, and outcome analytics are planned future work, not part of v1.0.0.

## Publication checklist

- [ ] Upload the repository contents to GitHub
- [ ] Tag the commit as `v1.0.0`
- [ ] Create a GitHub Release named **Job Hunt Agent v1.0.0 — GitHub Release**
- [ ] Confirm no user data, secrets or private workspace files are in the committed history
- [ ] Configure GitHub repository social preview using `assets/social-preview.png` (optional)
