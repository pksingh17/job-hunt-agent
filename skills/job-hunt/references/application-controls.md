# Application controls

These rules protect the user. Profiles can make them stricter. Nothing in a profile can loosen the never-autonomous list or the truthfulness rule.

## Autonomy levels (set in rules.md)
- **research-only**: discover, research, score, log. Nothing more.
- **draft** (default): also prepare tailored materials via the `tailor` skill. The user submits every application.
- **assisted-apply**: also fill application forms in a browser, only for roles the user approved in the current conversation, pausing before each final submit.

Several job boards prohibit automated applications in their terms, LinkedIn among them. Accounts get restricted for it. That is why the default stops at drafts. If a user picks assisted-apply, setup tells them this once.

## Approval triggers (always queue as Awaiting Approval)
- score in the STRETCH / REVIEW band
- relocation, even when the role is otherwise ideal
- full night shift, or a six-day week
- an employment bond, exit penalty, or non-compete
- references requested at application stage
- a substantial take-home assignment or writing test
- salary expectation required while the listing is undisclosed
- any application question the profile does not answer
- any unusual declaration or commitment
- anything the profile lists under extra approval triggers

## Never autonomous, under any setting
- OTPs, passwords, security answers, 2FA codes
- government ID numbers, tax IDs, passport details, bank or payment details
- payments of any kind
- salary history beyond what the user wrote in the profile
- legal declarations, signatures, or anything legally binding
- consent to background checks
- voluntary demographic or equal-opportunity self-identification (gender, race or ethnicity, disability, veteran status, sexual orientation, caste, religion, age), even when the profile contains the answer. These are always the user's own choice to answer or decline.

When a CAPTCHA, login, OTP or anti-bot screen appears, stop, tell the user what it is, and wait for them to clear it.

## Truthfulness
Application material may select, order, rephrase and emphasise confirmed facts from `profile.md`. It may never add a qualification, metric, tool, client, employer, title, budget, team size, result or date the profile does not contain. If a form asks for something the profile lacks, ask the user. Their answer goes into the profile only after they confirm it.
