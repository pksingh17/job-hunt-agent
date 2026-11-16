# Scoring rubric

Eight dimensions. Each profile sets its own weights in `rules.md` (they must sum to 100). The defaults suit most early and mid-career searches:

| Dimension | Default weight | Tracker column |
|---|---|---|
| Role & direction fit | 25 | `s_role` |
| Skills & experience fit | 15 | `s_skills` |
| Growth & exposure | 15 | `s_growth` |
| Compensation | 15 | `s_comp` |
| Company quality | 10 | `s_company` |
| Employee-review signals | 10 | `s_reviews` |
| Work-life, shift, work model | 5 | `s_worklife` |
| Location | 5 | `s_location` |

Score every dimension as a fraction of its weight using the anchors below, then round to an integer. The anchors are written as fractions so they work at any weight. A dimension weighted 20 scores 16 at the 0.8 anchor.

## Role & direction fit
How closely the actual day-to-day work matches where the user wants their career to go, judged from the JD's responsibilities rather than its title.
- 1.0: a priority role in `rules.md`, and the responsibilities match the title
- 0.8: a priority role with some off-direction duties, or a stretch role that clearly moves them forward
- 0.6: a stretch role with mixed duties
- 0.4: a low-priority role that rules allow, or a good title wrapping mostly off-direction work
- 0.2 or less: off-direction work

Retitled roles are common. A "Brand Strategist" posting that is 80% caption writing is a writing role.

## Skills & experience fit
Required skills and years, compared with confirmed facts in `profile.md`.
- 1.0: meets every must-have and most nice-to-haves, experience inside the asked range
- 0.7: meets the must-haves, experience at the low edge of the range
- 0.5: missing one must-have that is learnable fast, or experience one band below
- 0.3: missing several must-haves, or experience well below
- 0.0: missing a hard credential (licence, degree, clearance) the JD treats as mandatory

## Growth & exposure
What the role adds to the person in two years: scope, ownership, strategic exposure, mentorship, a brand name that opens doors, skills the market rewards.
- 1.0: clear step up in scope or ownership, with visible senior exposure
- 0.6: lateral move with meaningful new skills
- 0.3: same work, different logo
- 0.0: a step backwards

## Compensation
Use the bands in `rules.md`: `comp_floor`, `comp_target`, `comp_stretch`, all in the profile's currency and salary period. Convert the listing to that period first (annual ÷ 12 for monthly, and the reverse). When a range is posted, use its midpoint.
- Below floor: hard filter, no score
- At floor: 0.3
- Between floor and target: rise linearly from 0.3 to 0.8
- At target: 0.8
- At or above stretch: 1.0
- Undisclosed: 0.5, with "salary undisclosed" in Red Flags only if the rules treat it as an approval trigger

If the region pack lists typical market ranges and the user gave no bands, say the score is provisional.

## Company quality
Stability, reputation, funding or revenue health, how the company treats the function the user works in.
- 1.0: established or well-funded, strong reputation, the function is valued
- 0.6: unremarkable but stable
- 0.3: thin public footprint, unclear business, or recent layoffs in this function
- 0.0: signs of fraud, fake listings, or "pay to apply"

## Employee-review signals
See `review-research.md`. Score from patterns, never from single reviews.
- 1.0: consistently positive across sources, recent
- 0.7: mixed with no recurring red flags
- 0.5: neutral default when evidence is Thin or None
- 0.3: one recurring red flag
- 0.0: several recurring red flags (salary delays, misleading JDs, bonds, unpaid overtime)

## Work-life, shift, work model
Measured against the preferences in `rules.md`.
- 1.0: matches the preferred schedule and work model
- 0.5: acceptable with one compromise (one late overlap day, hybrid when remote preferred)
- 0.0: conflicts with a stated preference that is not a hard filter

## Location
- 1.0: first-choice location or remote where remote is preferred
- 0.6: an allowed second choice
- 0.2: allowed only with relocation the user has not yet approved
- 0.0: outside the allowed set (this is normally a hard filter instead)

## Decision thresholds
Defaults, overridable in `rules.md`:
- 80 and up: PRIORITY APPLY
- 70 to 79: APPLY
- 60 to 69: STRETCH / REVIEW
- below 60: SKIP

Hard filters override every score.

## Custom criteria
Profiles may define extra criteria in `rules.md` (for example "tenure-track", "NHS band", "union shop"). Fold each one into the closest existing dimension and say so in the review summary. The eight tracker columns stay fixed so every tracker remains comparable.
