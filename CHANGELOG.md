# Changelog

## [1.0.0] — First public release

The first publicly versioned release of Job Hunt Agent. This release packages the existing open-source agent capabilities under a consistent 1.0.0 version across ChatGPT, Codex and Claude plugin manifests. It does not introduce a new web UI or hosted service.

### Included
- **Setup:** guided onboarding, candidate verification, reusable profile and job-search rules.
- **Job Hunt:** discovery guidance, deduplication, hard filters, job/company research, employee-review evidence, transparent scoring and ranked tracking.
- **Resume Lab:** resume health audits, transparent **Estimated ATS Compatibility**, JD matching, truthful resume creation and improvement passes.
- **Tailor:** role-specific resume drafts, cover letters, recruiter messages and application answers grounded in the confirmed profile.
- **Follow-up:** application tracking, recruiter response follow-up, interview preparation and next actions.
- **Regional guidance:** India, UK, US, Germany and a global fallback.
- **Cross-platform packaging:** Agent Plugins 1.0, Codex, Claude Code/Cowork and a script for standalone skills.
- **Privacy and safety:** user workspaces kept separate from public source; assisted-apply controls, human verification and no fabricated claims.

### Known limitations
- There is no built-in hosted UI, job-feed backend or automatic cloud synchronization.
- Job discovery, browser form filling and review-site access depend on the AI host, available integrations and the policies of third-party sites.
- ATS compatibility is a transparent estimate, **not** a score returned by an employer's applicant-tracking system.
- Job submissions are not guaranteed and must be confirmed before the tracker is marked applied.

### Upgrade note
The public release starts at **1.0.0**. Earlier internal prototypes are not published as separate public releases.
