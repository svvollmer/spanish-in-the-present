"""Regenerate verbs.json from tools/verbs_list.py.

    pip install verbecc
    python tools/build_verbs.py

Conjugations come from the verbecc library, then a few known library errors are corrected
below (FIXES). If you spot a wrong form on the site, add a correction here and rerun.
"""
import json, logging, os, re, sys
logging.disable(logging.CRITICAL)
from verbecc import CompleteConjugator
sys.path.insert(0, os.path.dirname(__file__))
from verbs_list import VERBS

TENSES = [("pres","indicativo","presente"),("pret","indicativo","pretérito-perfecto-simple"),
("imp","indicativo","pretérito-imperfecto"),("fut","indicativo","futuro"),("cond","condicional","presente"),
("perf","indicativo","pretérito-perfecto-compuesto"),("plus","indicativo","pretérito-pluscuamperfecto"),
("subj","subjuntivo","presente"),("subjimp","subjuntivo","pretérito-imperfecto-1")]
P5 = ["yo","tú","él","nosotros","ellos"]
P4 = ["tú","usted","nosotros","ustedes"]
REGULAR = {"cort:ar","deb:er","viv:ir","(regular)","compren:der"}
SPELLING = {"pag:ar","sa:car","ca:zar","cre:er","act:uar","gu:iar","adstrin:gir"}
# Corrections to library output: participles, and commands where the library gives a rarer form
PARTICIPLE_FIXES = {"comprender":"comprendido","nacer":"nacido","elegir":"elegido"}
COMMAND_FIXES = {("valer",0):"vale", ("ir",2):"vamos"}
# verbecc returns the impersonal "hay" for haber's él form; as an auxiliary it is "ha" (ha hablado).
FORM_FIXES = {("haber","pres",2): "ha"}

from verb_uses import USES, EXTRA_FORMS   # noqa: E402  (hand-authored, like the fixes above)
# Tenses a grammar lists but nobody uses: not shown on the sheet, not drilled.
# haber's imperative is archaic ("hé"); gustar's is not used (you'd say "que te guste").
SKIP = {"haber": ["cmd","neg"], "gustar": ["cmd","neg"]}
# Backwards verbs: the thing liked is the subject, so only the él/ellos forms get drilled.
DATIVE = {"gustar"}
NOTES = {
    "haber": "Auxiliary only: he hablado, había llegado. For \"there is / there are\" use the "
             "impersonal hay — había, hubo, habrá — never ha.",
    "gustar": "Works backwards: the thing liked is the subject. Me gusta el café, me gustan los "
              "libros. Only the él/ella and ellos forms are drilled.",
}

c = CompleteConjugator(lang="es")

def conjugate(inf):
    try:
        return json.loads(c.conjugate(inf).to_json())
    except Exception:
        # verbecc crashes on a few regular verbs (pasar, resultar, suceder): build from a model verb
        model, stem = {"ar":("hablar","habl"),"er":("comer","com"),"ir":("vivir","viv")}[inf[-2:]]
        d = json.loads(c.conjugate(model).to_json())
        def fix(o):
            if isinstance(o, dict): return {k: fix(v) for k, v in o.items()}
            if isinstance(o, list): return [fix(x) for x in o]
            if isinstance(o, str):
                return " ".join(inf[:-2] + w[len(stem):] if w.startswith(stem) else w for w in o.split(" "))
            return o
        d = fix(d); d["verb"]["template"] = "(regular)"
        return d

def strip(form, pr):
    return form[len(pr)+1:] if form.startswith(pr + " ") else form

def first(x):
    x = x[0]
    return x["c"][0] if isinstance(x, dict) else x

out = []
for inf, en in VERBS:
    d = conjugate(inf); m = d["moods"]; tpl = d["verb"]["template"]
    v = {"inf": inf, "en": en, "t": {}}
    for key, mood, t in TENSES:
        rows = {r["pr"]: r["c"][0] for r in m[mood][t]}
        v["t"][key] = [strip(rows[p], p) for p in P5]
    for key, t in (("cmd","afirmativo"),("neg","negativo")):
        rows = {r.get("pr"): r["c"][0] for r in m["imperativo"][t]}
        v["t"][key] = [rows.get(p, "") for p in P4]
    v["ger"] = first(m["gerundio"]["gerundio"])
    v["part"] = first(m["participo"]["participo"])
    if inf in PARTICIPLE_FIXES:
        old, new = v["part"], PARTICIPLE_FIXES[inf]; v["part"] = new
        for k in ("perf","plus"): v["t"][k] = [f.replace(old, new) for f in v["t"][k]]
    for (verb, i), form in COMMAND_FIXES.items():
        if verb == inf: v["t"]["cmd"][i] = form
    for (verb, key, i), form in FORM_FIXES.items():
        if verb == inf: v["t"][key][i] = form
    if inf in SKIP: v["skip"] = SKIP[inf]
    if inf in DATIVE: v["dative"] = True
    if inf in NOTES: v["note"] = NOTES[inf]
    if inf in USES:
        v["uses"] = [{"u": u, "ex": ex, "en": en} for u, ex, en in USES[inf]]
    v["type"] = "regular" if tpl in REGULAR else ("spelling" if tpl in SPELLING else "irregular")
    out.append(v)

def render(verbs):
    """One tense per line, so a regenerated file has a reviewable diff.

    The old one-line output made any change to the data a single 107 KB diff hunk.
    """
    j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":"))
    chunks = []
    for v in verbs:
        lines = [' {', f'  "inf":{j(v["inf"])}, "en":{j(v["en"])}, "type":{j(v["type"])},',
                 f'  "ger":{j(v["ger"])}, "part":{j(v["part"])},']
        for k in ("dative", "skip", "note"):
            if k in v: lines.append(f'  {j(k)}:{j(v[k])},')
        if "uses" in v:
            lines.append('  "uses":[')
            for n, u in enumerate(v["uses"]):
                lines.append(f'   {j(u)}' + ("," if n < len(v["uses"]) - 1 else ""))
            lines.append('  ],')
        lines.append('  "t":{')
        ks = list(v["t"])
        for n, k in enumerate(ks):
            lines.append(f'   {j(k)}:{j(v["t"][k])}' + ("," if n < len(ks) - 1 else ""))
        lines += ['  }', ' }']
        chunks.append("\n".join(lines))
    return "[\n" + ",\n".join(chunks) + "\n]\n"


def check_uses(verbs):
    """Every use sentence must contain a real form of the verb it is filed under.

    Cheap to check and worth checking: a sentence pasted under the wrong verb, or one that only
    mentions the verb in its English translation, would teach the wrong thing and nothing else
    would notice.
    """
    import unicodedata as _ud

    def fold(x):
        return "".join(c for c in _ud.normalize("NFD", x.lower())
                       if _ud.category(c) != "Mn")

    problems = []
    index = {v["inf"]: v for v in verbs}

    for inf, uses in USES.items():
        if inf not in index:
            problems.append("%s: not in verbs_list.py, so its uses would be dropped silently" % inf)
            continue
        v = index[inf]
        forms = {fold(v["inf"]), fold(v["ger"]), fold(v["part"])}
        for row in v["t"].values():
            for f in row:
                for tok in fold(f).split():
                    if tok:
                        forms.add(tok)
        for extra in EXTRA_FORMS.get(inf, []):
            forms.add(fold(extra))
        # Forms also appear with pronouns stuck on the end: déjame, cuéntame, ponte, dímelo.
        # Match the suffix against the actual clitics rather than guessing by length -- a length
        # rule rejects the two-letter imperatives (di, ve, da, sé) that are the commonest of all.
        clitics = ("me", "te", "se", "lo", "la", "le", "nos", "os", "los", "las", "les")

        def is_clitic_tail(tail):
            while tail:
                for c in sorted(clitics, key=len, reverse=True):
                    if tail.startswith(c):
                        tail = tail[len(c):]
                        break
                else:
                    return False
            return True

        for u, ex, en in uses:
            words = [w for w in re.findall(r"[\w\u00c0-\u024f]+", fold(ex)) if w]
            hit = any(w in forms or any(w.startswith(f) and is_clitic_tail(w[len(f):])
                                        for f in forms if f)
                      for w in words)
            if not hit:
                problems.append("%s: %r contains no form of the verb" % (inf, ex))
            if not u.strip() or not en.strip():
                problems.append("%s: %r has an empty label or translation" % (inf, ex))
    return problems


_problems = check_uses(out)
if _problems:
    print("verb_uses.py has %d problem(s):" % len(_problems), file=sys.stderr)
    for _p in _problems:
        print("  - " + _p, file=sys.stderr)
    sys.exit(1)

text = render(out)
assert json.loads(text) == out, "pretty-printer changed the data"
path = os.path.join(os.path.dirname(__file__), "..", "verbs.json")
with open(path, "w", encoding="utf-8") as f: f.write(text)
print(f"wrote {len(out)} verbs to verbs.json ({text.count(chr(10))+1} lines)")
