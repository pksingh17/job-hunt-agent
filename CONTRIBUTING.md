# Contributing

Thanks for helping. The most useful contributions, in order:

1. **Region packs.** Copy `skills/job-hunt/references/regions/_template.md` to `<country>.md`, fill it from first-hand experience, keep it under 80 lines, and open a pull request. Name job boards and review sites you have actually used. Avoid figures that go stale fast (visa salary thresholds, tax rates); point to the official source instead.
2. **Bug reports from real batches.** What you asked, what happened, what you expected. Remove personal data first.
3. **Occupation notes.** Fields with their own norms (healthcare bands, academic ranks, union trades) can add guidance to `scoring.md` under Custom criteria.
4. **Resume Lab test cases.** Contribute fictional/anonymized resumes and JDs that expose parsing, truthfulness, or scoring edge cases. Never submit a real person's documents without explicit permission and full de-identification.

Ground rules for any change:
- Nothing may weaken the truthfulness rule or the never-autonomous list in `application-controls.md`.
- Keep tracker columns stable. If a change touches `tracker.py`, run its self-checks (`init`, `add` with a duplicate, a same-role-different-location row, an invalid score and a text value starting with `=`; `update` including clearing a field; `list`) and include the output in the PR.
- Keep skill text platform-neutral. Say "web search", "a browser" or "the workspace folder", never a specific product. Platform details belong in the manifests and the README.
- Never commit a real person's profile, resume, Resume Lab report, application material, or tracker.
