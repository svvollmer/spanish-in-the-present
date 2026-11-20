# Spanish in the Present — project notes for Claude Code

## What this is
A lightweight Spanish study system for adult learners who already understand ~30–50% of spoken Spanish and want to close the gap fast. Owner: Steve. Collaborators testing and developing: Steph and Miles. Learners "live in the present" with their Spanish (real conversations, Latin America), find other apps too slow, and have never studied from a textbook, so the site combines old-school textbook chapters with fast drills.

## Status
- First version built in claude.ai, moved here as a git repo.
- **Live.** Public repo `svvollmer/spanish-in-the-present`; GitHub Pages serves `main` / root at
  <https://svvollmer.github.io/spanish-in-the-present/>
- Current commit: the original `ea26f0e` re-authored as `047f9d2` (identical tree). Author and committer are
  `Steve Vollmer <34316017+svvollmer@users.noreply.github.com>` — the GitHub noreply address, deliberately,
  so a public repo does not carry a personal email. Repo-local `user.name`/`user.email` are set to match.
- A preview copy also exists as a claude.ai artifact; this repo is the source of truth.

## Setup status (2026-11-20)
Done:
1. Commit re-authored; repo-local git identity set.
2. Public repo created, `main` pushed.
3. GitHub Pages enabled from `main` / root. First build succeeded; `index.html` and `verbs.json` both serve 200.
4. Stray `../spanish-in-the-present.tar.gz` and `tools/__pycache__/` removed — the tarball was first verified
   byte-identical to the repo (its only commit was the pre-amend `ea26f0e`, same tree), so nothing was lost.

Remaining:
5. **Add Steph and Miles as collaborators — their GitHub usernames are still unknown. Ask Steve.**
6. Workflow: branches + pull requests so others can test before changes go live. There is no CI and no branch
   protection yet, and Pages deploys straight off `main`, so a bad push breaks the live site for all three.

## Architecture
Static site, no build step, no framework.
- `index.html` — everything: CSS, chapter HTML, and all JS (routing, verb sheet, drills, phrases). Hash routes: `#book`, `#verbs`, `#drill`, `#phrases`, and `#ch0`…`#ch12` for chapters.
- `verbs.json` — 127 verbs × 11 tenses. Loaded with `fetch`, so the site must be served over HTTP (`python3 -m http.server`), not opened as a file.
- `tools/verbs_list.py` — verb list + English glosses in rough frequency order.
- `tools/build_verbs.py` — regenerates `verbs.json` using the `verbecc` library (`pip install verbecc`; first run trains a small model, ~20 s). It reproduces the current `verbs.json` exactly.

### Data shape (`verbs.json`)
`{inf, en, type: "regular"|"spelling"|"irregular", ger, part, t: {pres, pret, imp, fut, cond, perf, plus, subj, subjimp, cmd, neg}}`
- 5-person tenses are ordered `[yo, tú, él/ella/Ud., nosotros, ellos/Uds.]`. No vosotros (Latin American Spanish by design).
- `cmd` / `neg` are `[tú, usted, nosotros, ustedes]`.
- Stem-changing verbs are classed as `irregular`.

### Known data issues
verbecc has bugs, corrected in `build_verbs.py`:
- crashes on `pasar`, `resultar`, `suceder` → built from a model verb;
- wrong participles for `comprender`, `nacer`, `elegir`;
- `valer` tú command (`val` → `vale`); `ir` nosotros command (`vayamos` → `vamos`).
Irregular verbs were hand-checked; not every one of the 127 verbs has been checked line by line. New corrections go in the FIXES dicts in `build_verbs.py`.

### Page features
- **Book:** 13 chapters (0 intro … 11 hearing real Spanish, 12 Latin America vs. Spain). Each `<article class="chapter" id="chN" data-title="…">`; the TOC is built from these. Each ends with a `<details>` check-yourself section and links that preselect a tense on the sheet/drill (`data-sheet`, `data-drill`, `data-mode`).
- **Verb sheet:** filter/search; forms that differ from the regular -ar/-er/-ir pattern are shown in red. This is computed in JS by `regularForms()`, not stored. Click a verb for a full card (`<dialog>`).
- **Drills:** *Produce* (type the form; accent buttons; lenient-accent option) and *Recognize* (see a form, pick verb · tense · person; keys 1–4). Recognition uses a reverse index `FORMIDX` so ambiguous forms (e.g. *hablamos* present/preterite) accept any valid answer, and no wrong option shows the same form. Commands are excluded from Recognize. Leitner spaced repetition (`INTERVALS`: 0, 2 min, 10 min, 1 d, 3 d, 7 d, 21 d), weighted toward misses. 60-second sprint mode with best score.
- **Phrases:** `PHRASES` array in the script (~65 phrases in 6 groups, including property/negotiation vocabulary) plus flashcards on the same SRS.
- **Storage:** `localStorage` keys `esp.srs`, `esp.best`, `esp.days`, all in try/catch. Progress is per browser and does not sync.

### Design conventions
Mid-century grammar-textbook look: ink-blue on cool paper, ochre structural rules, red used *only* for irregular forms. Fonts: Libre Caslon Text (body/display), IBM Plex Sans Condensed (UI/tables). Colors are CSS tokens in `:root` with dark-mode overrides (`prefers-color-scheme` and `[data-theme]`). Must work on phones (~390 px), and the verb sheet prints in landscape.

### Language conventions
Latin American Spanish: `ustedes` for all plural "you", no vosotros production (chapter 12 teaches recognition only). Regional notes cover Panama and Peru. Keep explanations in plain English for the learner.

## Open bugs (code review, 2026-11-20)
Found by reading the code; none are fixed yet. Data was audited at the same time and is in good shape:
6,477 forms with no empty/missing/duplicate entries, ~25 of the worst irregulars hand-checked correct, and
`regularForms()` agrees with the stored `type` on all 127 verbs (0 contradictions in either direction).

1. **Streak uses UTC, not local time** — `index.html`, `renderStats()`: `new Date().toISOString().slice(0,10)`.
   Rolls over at 7–8pm US Eastern, so evening sessions are filed under the next day and the streak is wrong.
2. **One answer, three verdicts** — `index.html`, `showProd()` submit handler. With lenient accents off, an
   accent-only error increments `S.ok`/`S.streak` (header says correct) but `counted` is false, so `grade()`
   files it wrong in the SRS while the feedback prints red. Pick one meaning and use it in all three places.
3. **`gustar` is drilled as an ordinary verb** — prompt "to be pleasing (to like)" + person "I" expects
   `gusto`. Grammatical but it trains the exact error English speakers make. Same issue for the whole
   `gustar` class if more are added.
4. **`haber` is missing** — a top-5 verb. Every card's `perf`/`plus` is built from `he/has/ha/hemos/han`, but
   there is no `haber` entry to drill, and `hay` is taught in ch2 without a sheet entry.
5. **`<html lang="en">`** with a book full of Spanish, and no `lang="es"` on Spanish spans. Matters more once
   listening practice lands, since `speechSynthesis` picks its voice from `lang`.
6. **`esp.days` grows without bound** — one date string per study day, never pruned. The only unbounded store.

### Project-hygiene gaps
- **No tests.** The three checks worth automating: `verbs.json` schema/arity, a golden file of hand-verified
  forms, and the `regularForms()`-vs-`type` invariant (it holds today, so it can be locked in).
- **Regeneration is not reproducible and its diffs are unreadable.** `pip install verbecc` is unpinned (no
  `requirements.txt`), and `build_verbs.py` writes `verbs.json` minified via `separators=(",",":")`, so any
  regeneration shows up as one 107 KB line. Pin the version and pretty-print the JSON before trusting a rerun.
- No CI, no branch protection, no LICENSE. Google Fonts load from a CDN, which breaks offline use.
- The 65 phrases are hardcoded in `index.html` while verbs live in JSON.
- **No audio anywhere**, though ch11 is "Hearing real Spanish" and Recognize is framed "as if you just heard
  it". Roadmap item 2 is where this gets fixed.

## Roadmap (Steve's priorities)
1. **Sync progress across devices and per person** (Steve, Steph, Miles). Today it is localStorage only.
2. **More content:** further chapters at the levels people find hardest; more verbs; vocabulary-gap test over the ~2,000–3,000 most frequent words; listening at native speed (audio clip → reveal transcript).
3. **Live translator (separate app, same repo, e.g. `translator/`).** Goal: genuinely real-time two-way translation on iPhone/Android that both people *read* on one phone (split screen, the other half upside down for the person across the table).
   - Current products are too slow mainly because they wait for the end of a sentence and then speak the translation. Design choices: **text only, no TTS**; stream partial transcripts word by word; handle translation "flicker" with stable streaming.
   - Benchmark streaming engines on real Spanish conversation before committing (candidates include DeepL Voice, Gemini Live Translate preview, OpenAI realtime translation, Deepgram/AssemblyAI streaming STT + LLM translation).
   - Learning hook: show the Spanish first and translate only the words the user taps; tapped words plus their sentence go into the drill deck. This merges the translator with the study system.
   - Needs mic streaming + API keys → a PWA or native app with a small backend for keys. Don't put API keys in the static site.
