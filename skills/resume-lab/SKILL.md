---
name: resume-lab
description: "Audit, score, build and improve truthful resumes for a job seeker using their confirmed job-hunt-agent profile. Use for resume/CV reviews, estimated ATS compatibility, JD matching, resume health checks, resume building from scratch, variant creation, gap analysis, keyword alignment, or before the tailor skill prepares a role-specific application."
---

# Resume Lab — truthful resume intelligence

Resume Lab improves a candidate's presentation without changing the underlying truth.

Its factual ceiling is always the active profile's `profile.md`. If a resume contains a claim that is not confirmed in `profile.md`, flag it for confirmation instead of silently treating it as true. If the user confirms a new fact, route it through the normal profile-update flow before using it in generated material.

## Modes

Choose the smallest mode that satisfies the request.

### 1. Resume Audit
Use when the user asks whether a resume is good, wants a resume review, or uploads a resume without a specific JD.

Evaluate:
- parsing safety and section structure
- chronology and consistency
- role/title clarity
- bullet quality and specificity
- evidence and measurable impact
- relevance of skills
- duplication and filler
- readability and concision
- weak, unsupported, or ambiguous claims
- formatting patterns that may break common ATS parsers

Return a `Resume Health` score out of 100 using `references/resume-health.md`, plus prioritized fixes: Critical, High impact, Nice to have.

Do not claim that a high health score guarantees interviews or ATS acceptance.

### 2. JD Match / Estimated ATS Compatibility
Use when a job description is available.

Compare the selected resume variant and the full JD. Score using `references/ats-compatibility.md`.

Always label the output **Estimated ATS Compatibility**, never "the ATS score". There is no universal ATS scoring algorithm and different employers configure systems differently.

Return:
- total estimated compatibility /100
- component scores
- confirmed strong matches
- confirmed experience that is underrepresented in the resume
- requirements that are genuinely missing
- exact terms from the JD that can be safely mirrored because they describe confirmed experience
- a **DO NOT ADD** section for requirements the candidate does not possess or has not confirmed
- the five highest-impact truthful changes

Never reward keyword repetition for its own sake. Contextual, evidenced use beats keyword stuffing.

### 3. Resume Builder
Use when the user has no usable resume or asks to create a new one.

Build from confirmed `profile.md` facts only. Ask only for material gaps that prevent a coherent resume; do not re-ask facts already in the profile.

Default structure unless the user's field calls for another convention:
1. Name and contact block
2. Targeted professional summary when useful
3. Experience
4. Projects / selected work when relevant
5. Skills
6. Education
7. Certifications / publications / licenses where relevant

Do not invent metrics to make bullets look stronger. If a bullet would materially improve with a missing number, write the truthful qualitative version and separately ask whether the user can verify a metric.

### 4. Variant Builder
Use when the candidate targets meaningfully different role families.

Create a small set of named master variants rather than one resume per job. Each variant changes emphasis, ordering, summary, skills prominence, and bullet selection while preserving dates, employers, titles, qualifications, and confirmed facts.

Examples of variant logic, not fixed categories:
- execution / specialist
- strategy / leadership
- industry A / industry B
- academic / industry

Store approved variants under the profile's `resumes/` directory with descriptive names.

### 5. Improvement Pass
Use after a resume has been tailored for a JD.

Re-run the compatibility analysis and report:
- before score
- after score
- what changed
- which gaps remain because they are real capability gaps rather than resume problems

The goal is not to force a target score. Stop improving when further gains would require distortion, repetition, or unsupported claims.

## Truth ledger

Classify every proposed addition into one of four buckets:

1. **Confirmed and present** — already supported and represented.
2. **Confirmed but underrepresented** — safe to add or strengthen.
3. **Plausible but unconfirmed** — ask the user before using.
4. **Not possessed / contradicted** — never add; place in `DO NOT ADD` when relevant.

A synonym is safe only when it truthfully describes the same work. For example, changing "keyword research" to "SEO keyword research" is fine when supported; changing "wrote campaign copy" to "owned paid acquisition" is not.

## Resume files

When editing or generating an actual resume file, preserve the source format when practical. Use the platform's document/PDF tools when available and follow their formatting instructions.

Keep ATS-safe defaults unless the user explicitly chooses a design-heavy version:
- one main text column for core content
- standard headings
- selectable text
- conventional date formatting
- no important information only in headers/footers, images, icons, or charts
- avoid decorative tables/text boxes for core experience in ATS-oriented versions

A visually designed resume can be a separate human-facing variant; do not imply it is automatically ATS-safe.

## Handoff to Tailor

Resume Lab diagnoses and builds the resume system. `tailor` prepares the final role-specific application.

For a shortlisted role, preferred flow:
1. Resume Lab: run JD match on the best master variant.
2. Resume Lab: identify safe changes and real gaps.
3. Tailor: produce the role-specific resume/cover letter/form answers.
4. Resume Lab: optional final compatibility and truth audit.

## Saving analyses

When the workspace is writable, save durable analyses under:

`profiles/<slug>/resume-lab/`

Suggested names:
- `baseline-audit.md`
- `<company>-<role>-match.md`
- `<variant>-audit.md`

Do not write a user's resume, profile, or analysis into the plugin's own source directory.

## References

Read as needed:
- `references/resume-health.md`
- `references/ats-compatibility.md`
- `references/output-template.md`
