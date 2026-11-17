# Contributors

Job Hunt Agent is maintained jointly by the project contributors.

Individual contributors are credited through the repository's Git history. Maintainers may add public GitHub handles here later if they choose.

## Contributors

- **Vivek Vankar** ([@vivek-vankar](https://github.com/vivek-vankar)): original job-hunt agent, public release and maintenance.
- **Prabhakar Singh**: Claude port, Resume Lab integration, the company-researcher and application-operator agents, candidate memory and voice, guided fill, ATS playbooks.

v1.1.0: agents, candidate memory and guided fill

Builds on v1.0.0. Every skill file in v1.0.0 matched the v0.3.0 base, so this applies cleanly. Existing profiles keep running exactly as before until the user opts in.

What's new

Two agents (Claude Code / Cowork)

company-researcher (Sonnet, web only): one per shortlisted company, run in parallel. Returns a company card with an identity check, evidence level, dated red flags, a scam check, same-function reviews, pay signals and suggested Company / Reviews scores.
application-operator (Sonnet, browser): fills one approved application on an employer's careers site or ATS. Observes each step before filling, re-reads the page when answers reveal new fields, reads back every value, and checks resume-parser pre-fills. Stops at every gate, leaves self-ID questions blank, sends free-text questions back for approval, and never presses submit.

ATS playbooks. The lead records each portal's route in the workspace's ats-playbooks/, so repeat applications on Workday, Greenhouse, Darwinbox and others go faster. No personal data is stored in them.

Modes. mode: full | lite in rules.md. Full uses the agents. Lite runs in a single thread, for free plans and skills-only hosts. Runs drop to lite automatically if agents can't start.

Candidate memory. A per-profile memory.md holds voice notes from the user's own confirmed writing, edits they made to past drafts, company history and screening questions they've seen. Tailor and follow-up write in that voice. profile.md stays the limit on what can be claimed.

Guided fill. When the agent can't or shouldn't fill a form (job-board apply flows, bot walls, no browser tool), the user fills it with the lead's help: a fill card with every value ready to paste, help on each field as it comes up, and a line-by-line check of the review screen before submit.

board_apply: guided | assist. Controls whether job-board-hosted forms are guided (the default) or filled by the agent after the user opens them. Setup states the account risk once. Profiles without the line keep their v1.0.0 behaviour.

Compatibility
A profile with no mode or board_apply line runs exactly as on v1.0.0.
tracker.py is unchanged, so no tracker self-checks are needed.
The truthfulness rule and the never-autonomous list are untouched. The new rules only add stops.
Skill text stays platform-neutral. Agent tool names live in agents/, which only Claude Code and Cowork read.
Files

New: agents/company-researcher.md, agents/application-operator.md, skills/job-hunt/references/roles.md, ats-playbooks.md, guided-fill.md, skills/setup/assets/templates/memory.md. Changed: the job-hunt, setup, tailor and follow-up skills, application-controls.md, the rules.md template, README, CHANGELOG, CONTRIBUTORS and all manifests (version bumped to 1.1.0).

## Contribution principle

Credit should follow meaningful project contributions while keeping private candidate data, personal resumes, tracker files, credentials, and other user-specific information out of the public repository.
