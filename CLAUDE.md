# Spanish in the Present — project notes for Claude Code

## What this is
A lightweight Spanish study system for adult learners who already understand a fair amount of
spoken Spanish and want to close the gap fast: old-school textbook chapters paired with fast
drills, for people who have never studied from a textbook and find other apps too slow.
Latin American Spanish throughout.

> Private working notes — the roadmap, who is testing, and anything commercial — live in
> `NOTES.private.md`, which is deliberately **not** in version control. This file is public:
> keep it to how the code works.

## Status
- First version built in claude.ai, moved here as a git repo.
- **Live.** Public repo `svvollmer/spanish-in-the-present`; GitHub Pages serves `main` / root at
  <https://svvollmer.github.io/spanish-in-the-present/>
- Commits use the GitHub noreply address, so the public repo carries no personal email.
- A preview copy also exists as a claude.ai artifact; this repo is the source of truth.

## Architecture
Static site, no build step, no framework.
- `index.html` — everything: CSS, chapter HTML, and all JS (routing, verb sheet, drills, phrases). Hash routes: `#book`, `#verbs`, `#drill`, `#phrases`, and `#ch0`…`#ch12` for chapters.
- `verbs.json` — 128 verbs × 11 tenses. Loaded with `fetch`, so the site must be served over HTTP (`python3 -m http.server`), not opened as a file. Written one tense per line so a regeneration has a reviewable diff.
- `tools/verbs_list.py` — verb list + English glosses in rough frequency order.
- `tools/build_verbs.py` — regenerates `verbs.json` using the `verbecc` library (`pip install -r requirements.txt`; first run trains a small model, ~20 s).
- `requirements.txt` — pins **verbecc 2.1.0**. Verified 2026-11-20: on 2.1.0 the script reproduces the committed `verbs.json` byte for byte. Do not float this version; a different one can silently rewrite all 6,784 forms.

### Data shape (`verbs.json`)
`{inf, en, type: "regular"|"spelling"|"irregular", ger, part, t: {pres, pret, imp, fut, cond, perf, plus, subj, subjimp, cmd, neg}}`
Optional fields, set from `SKIP` / `DATIVE` / `NOTES` in `build_verbs.py`:
- `skip: ["cmd","neg"]` — tenses that exist on paper but nobody says. Hidden from the sheet and the cards, excluded from drills, the reverse index and distractors.
- `dative: true` — a backwards verb (`gustar`): only person indices 2 and 4 are shown or drilled, the rest render as "—".
- `note: "…"` — shown at the top of the verb's card.
- 5-person tenses are ordered `[yo, tú, él/ella/Ud., nosotros, ellos/Uds.]`. No vosotros (Latin American Spanish by design).
- `cmd` / `neg` are `[tú, usted, nosotros, ustedes]`.
- Stem-changing verbs are classed as `irregular`.

### Known data issues
verbecc has bugs, corrected in `build_verbs.py`:
- crashes on `pasar`, `resultar`, `suceder` → built from a model verb;
- wrong participles for `comprender`, `nacer`, `elegir`;
- `valer` tú command (`val` → `vale`); `ir` nosotros command (`vayamos` → `vamos`).
- `haber` present *él* came back as the impersonal `hay`; corrected to `ha` via `FORM_FIXES`, since the paradigm on the card is the auxiliary (`ha hablado`). `hay` is called out in haber's note.
- `haber` tú imperative came back as the archaic `hé`; haber and gustar both carry `skip: ["cmd","neg"]` instead.
Irregular verbs were hand-checked; not every one of the 128 verbs has been checked line by line. A 2026-11-20 audit confirmed 6,784 forms with no empty, missing or duplicate entries, hand-checked ~25 of the worst irregulars, and found `regularForms()` agreeing with the stored `type` on every verb. New corrections go in the FIXES dicts in `build_verbs.py`.

### Page features
- **Book:** 13 chapters (0 intro … 11 hearing real Spanish, 12 Latin America vs. Spain). Each `<article class="chapter" id="chN" data-title="…">`; the TOC is built from these. Each ends with a `<details>` check-yourself section and links that preselect a tense on the sheet/drill (`data-sheet`, `data-drill`, `data-mode`).
- **Verb sheet:** filter/search; forms that differ from the regular -ar/-er/-ir pattern are shown in red. This is computed in JS by `regularForms()`, not stored. Click a verb for a full card (`<dialog>`).
- **Drills:** *Produce* (type the form; accent buttons; lenient-accent option) and *Recognize* (see a form, pick verb · tense · person; keys 1–4). Recognition uses a reverse index `FORMIDX` so ambiguous forms (e.g. *hablamos* present/preterite) accept any valid answer, and no wrong option shows the same form. Commands are excluded from Recognize. Leitner spaced repetition (`INTERVALS`: 0, 2 min, 10 min, 1 d, 3 d, 7 d, 21 d), weighted toward misses. 60-second sprint mode with best score.
- **Phrases:** `PHRASES` array in the script (~65 phrases in 6 groups, including property/negotiation vocabulary) plus flashcards on the same SRS.
- **Audio:** browser `speechSynthesis`, no hosted files. `pickVoice()` prefers a Latin American voice (es-MX, es-US, es-419, …) and falls back to anything that isn't es-ES. If no Spanish voice exists the two audio options hide themselves. Recognize can play the form and, with "Listen only", hide the text until you answer — `R` replays, "Slower" plays at rate 0.6. Produce speaks the correct answer after you check. Verb-card forms and phrases are tap-to-hear.
- **Storage:** `localStorage` keys `esp.srs`, `esp.best`, `esp.days`, `esp.audio`, `esp.listen`, all in try/catch. Progress is per browser and does not sync. **Export / Import** on the drill page writes and reads `{app, version, exported, data:{srs,best,days}}`; import *merges* (per item, the copy with the higher `s` wins) and never replaces, so it is safe to import a file from another device. `esp.days` is capped at 400 entries.

### Design conventions
Mid-century grammar-textbook look: ink-blue on cool paper, ochre structural rules, red used *only* for irregular forms. Fonts: Libre Caslon Text (body/display), IBM Plex Sans Condensed (UI/tables). Colors are CSS tokens in `:root` with dark-mode overrides (`prefers-color-scheme` and `[data-theme]`). Must work on phones (~390 px), and the verb sheet prints in landscape.

### Language conventions
Latin American Spanish: `ustedes` for all plural "you", no vosotros production (chapter 12 teaches recognition only). Regional notes cover Panama and Peru. Keep explanations in plain English for the learner.

## Code review of 2026-11-20 — all findings fixed
Fixed in the same pass; kept here so the reasoning isn't lost.

1. **Streak counted UTC days.** `renderStats()` used `new Date().toISOString().slice(0,10)`, which rolls
   over at 7–8pm US Eastern, so an evening session was filed under tomorrow. Now a local-calendar
   `ymd()` helper, used for both the day stamp and the streak walk. Verified at UTC−5: 20 Nov 11:30pm
   local gave `2026-11-21` the old way, `2026-11-20` now.
2. **One answer, three verdicts.** In Produce with lenient accents off, an accent-only error incremented
   the on-screen score but was graded *wrong* in the SRS while the feedback printed red. `counted` is now
   the single verdict for score, streak and SRS. Verified both ways: lenient off → `0/0`, red, `w:1`;
   lenient on → `1/1`, green, `b:1`.
3. **`gustar` was drilled as an ordinary verb** ("yo gusto"). It now carries `dative: true`: only the
   él/ella and ellos forms appear or get drilled, the rest render "—", the card explains the pattern,
   and Produce shows a "backwards verb" hint.
4. **`haber` was missing.** Added (frequency-ranked after `estar`), with the `hay`→`ha` correction and a
   note. Its imperative and gustar's are suppressed via `skip`.
5. **`lang`.** `<html lang="en">` is correct — the book is in English — but the 209 `.es` spans and every
   JS-rendered Spanish string now carry `lang="es"`, so screen readers and `speechSynthesis` pick a
   Spanish voice rather than reading Spanish with English phonemes.
6. **`esp.days` grew without bound.** Capped at 400 entries.

Also in that pass: a dead `ks` variable in `showRecog()` was computed and never used; cross-tense
distractors now draw from it, so they stay inside the tenses the learner selected.

### Added at the same time
- **Audio** (see Page features) — the site's stated goal is understanding spoken Spanish, and until now
  Recognize printed the form it described as "what you just heard".
- **Progress export / import** — localStorage was the only copy of months of SRS history.
- **Pinned verbecc + one-tense-per-line `verbs.json`** — regeneration is now reproducible and reviewable.

### Deliberately not done (prototype stage)
CI, branch protection, a golden-file test over all 6,784 forms, splitting `index.html`, and a LICENSE.
The shape of the thing is still moving; tests would pin down data that is about to change, and the
single no-build-step file is an asset while iterating. Revisit when the content settles.

## Public/private boundary — read before writing anything down
The repo **and** the site are public. Two rules follow:
- Anything about people (who is testing, their level), the roadmap, or anything commercial goes in
  `NOTES.private.md`, which `.gitignore` excludes via `*.private.md`. Never move that content into a
  tracked file "for convenience".
- Never put an API key, token or credential anywhere in this repo. The site is static with no backend,
  so there is no safe place for one; the planned translator needs a small server precisely for this.

The site carries `<meta name="robots" content="noindex, nofollow">` and a `robots.txt` that disallows
all crawling — deliberate while it is a prototype. Do not remove either without being asked.

No licence file, deliberately: public on GitHub grants no reuse rights, so the default is
all-rights-reserved. Do not add MIT/Apache on tidiness grounds; it is a product decision.

`verbs.json`'s provenance is an open licensing question (verbecc's Spanish data is GPL-licensed) —
see "Where `verbs.json` comes from" in the README before the data ships in anything commercial.
