# Privacy

Job Hunt Agent does not operate its own server, user accounts or telemetry. It is a set of instructions plus a local tracker script; the AI platform or services a user connects may have their own data processing and retention terms.

**Where your data is stored:** your profile, rules, resumes, tailored drafts, batch reports and tracker live in the `job-hunt/` workspace created during setup. The workspace may be on your own machine or in storage provided by your AI host or connected app.

**External processing:** web searches, page reads and any email/calendar/browser/Drive connectors are handled by the host and services you choose. Review those providers' privacy terms, access controls and retention policies before uploading personal information.

**Keep your workspace out of git.** The repository's `.gitignore` excludes generated workspaces, profiles, applications, run reports, spreadsheets, environment files and common secret files so a clone used as a working folder is less likely to commit personal data. If you keep your workspace somewhere else, keep it private.

**Public-repo rule:** the project repository must contain no real candidate profile, resume, tracker, contact details, private sheet/database IDs, login data, or application history. Examples should be fictional or generic.

**What the agent never stores or submits on its own:** passwords, OTPs, government ID numbers, bank or payment details. Contact details you put in `profile.md` are used only when filling an application you approved.

## Resume Lab

Resume audits and JD-match reports can contain sensitive career history. Store them only inside the user workspace (for example `profiles/<slug>/resume-lab/`) and keep them out of the public repository.
