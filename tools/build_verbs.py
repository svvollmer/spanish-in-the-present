"""Regenerate verbs.json from tools/verbs_list.py.

    pip install verbecc
    python tools/build_verbs.py

Conjugations come from the verbecc library, then a few known library errors are corrected
below (FIXES). If you spot a wrong form on the site, add a correction here and rerun.
"""
import json, logging, sys, os
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
    v["type"] = "regular" if tpl in REGULAR else ("spelling" if tpl in SPELLING else "irregular")
    out.append(v)

path = os.path.join(os.path.dirname(__file__), "..", "verbs.json")
json.dump(out, open(path, "w"), ensure_ascii=False, separators=(",",":"))
print(f"wrote {len(out)} verbs to verbs.json")
