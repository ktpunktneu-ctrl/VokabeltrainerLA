# -*- coding: utf-8 -*-
import json

VOK_PATH = r"C:\Users\Klaus\VokabeltrainerLA\vokabeln.json"

# ---------------------------------------------------------------------------
# Grammatik-Metadaten: genus/deklination/genitiv je Substantiv.
# Genitiv wird explizit hinterlegt (nicht aus dem Nominativ abgeleitet) --
# das faengt genau die Faelle ab, die sich nicht durch eine Regel vorhersagen
# lassen (z.B. magister -> magistri, liber -> libri: 'e' faellt weg;
# puer -> pueri: 'e' bleibt). 4./5. Deklination und morphologisch unregelmaessige
# Woerter (dies, manus, bos) werden bewusst ausgeklammert (Stufe 3).
NOMEN_META = {
    # Familie
    "pater": ("m", 3, "patris"),
    "mater": ("f", 3, "matris"),
    "filius": ("m", 2, "filii"),
    "filia": ("f", 1, "filiae"),
    "frater": ("m", 3, "fratris"),
    "soror": ("f", 3, "sororis"),
    "avus": ("m", 2, "avi"),
    "avia": ("f", 1, "aviae"),
    "puer": ("m", 2, "pueri"),
    "puella": ("f", 1, "puellae"),
    "vir": ("m", 2, "viri"),
    "femina": ("f", 1, "feminae"),
    # Natur
    "aqua": ("f", 1, "aquae"),
    "terra": ("f", 1, "terrae"),
    "caelum": ("n", 2, "caeli"),
    "sol": ("m", 3, "solis"),
    "luna": ("f", 1, "lunae"),
    "stella": ("f", 1, "stellae"),
    "mons": ("m", 3, "montis"),
    "silva": ("f", 1, "silvae"),
    "flumen": ("n", 3, "fluminis"),
    "mare": ("n", 3, "maris"),   # i-Stamm: Abl.Sg. mari (Sonderfall, s.u.)
    "ventus": ("m", 2, "venti"),
    "ignis": ("m", 3, "ignis"),
    "arbor": ("f", 3, "arboris"),
    "flos": ("m", 3, "floris"),
    # Essen
    "panis": ("m", 3, "panis"),
    "vinum": ("n", 2, "vini"),
    "lac": ("n", 3, "lactis"),
    "caro": ("f", 3, "carnis"),
    "piscis": ("m", 3, "piscis"),
    "mel": ("n", 3, "mellis"),
    "pomum": ("n", 2, "pomi"),
    "oleum": ("n", 2, "olei"),
    "sal": ("m", 3, "salis"),
    "cibus": ("m", 2, "cibi"),
    # Zeit (nur die echten Substantive; dies = 5. Dekl., bleibt aussen vor)
    "nox": ("f", 3, "noctis"),
    "hora": ("f", 1, "horae"),
    "annus": ("m", 2, "anni"),
    "mensis": ("m", 3, "mensis"),
    # Schule
    "schola": ("f", 1, "scholae"),
    "magister": ("m", 2, "magistri"),
    "discipulus": ("m", 2, "discipuli"),
    "liber": ("m", 2, "libri"),
    "littera": ("f", 1, "litterae"),
    "verbum": ("n", 2, "verbi"),
    "lingua": ("f", 1, "linguae"),
    "charta": ("f", 1, "chartae"),
    "stilus": ("m", 2, "stili"),
    # Koerper (manus = 4. Dekl., bleibt aussen vor)
    "caput": ("n", 3, "capitis"),
    "oculus": ("m", 2, "oculi"),
    "pes": ("m", 3, "pedis"),
    "cor": ("n", 3, "cordis"),
    "os": ("n", 3, "oris"),
    "auris": ("f", 3, "auris"),
    "nasus": ("m", 2, "nasi"),
    # Tiere (bos = unregelmaessig, bleibt aussen vor)
    "canis": ("m", 3, "canis"),
    "felis": ("f", 3, "felis"),
    "equus": ("m", 2, "equi"),
    "avis": ("f", 3, "avis"),
    "leo": ("m", 3, "leonis"),
    "ursus": ("m", 2, "ursi"),
    "serpens": ("f", 3, "serpentis"),
}

# 3.-Deklination-Neutra, die als i-Stamm den Ablativ Singular auf -i statt -e
# bilden (Nom.Sg. endet auf -e/-al/-ar -> i-Stamm-Regel).
ISTAMM_NEUTER_ABL_I = {"mare"}

# Verben: Konjugationsklasse + die vier Stammformen (Praesens 1.Sg., Infinitiv,
# Perfekt 1.Sg., PPP/Supin). PPP leer lassen, wo unsicher (z.B. bibere), statt
# zu raten. esse/ire sind unregelmaessig und werden separat komplett fest
# hinterlegt; mori (Deponens) bleibt in Stufe 2 unangetastet.
VERB_META = {
    "habere": ("2", "habeo", "habui", "habitum"),
    "amare": ("1", "amo", "amavi", "amatum"),
    "videre": ("2", "video", "vidi", "visum"),
    "audire": ("4", "audio", "audivi", "auditum"),
    "dicere": ("3", "dico", "dixi", "dictum"),
    "facere": ("3io", "facio", "feci", "factum"),
    "venire": ("4", "venio", "veni", "ventum"),
    "dare": ("1", "do", "dedi", "datum"),
    "legere": ("3", "lego", "legi", "lectum"),
    "scribere": ("3", "scribo", "scripsi", "scriptum"),
    "vocare": ("1", "voco", "vocavi", "vocatum"),
    "laudare": ("1", "laudo", "laudavi", "laudatum"),
    "pugnare": ("1", "pugno", "pugnavi", "pugnatum"),
    "currere": ("3", "curro", "cucurri", "cursum"),
    "sedere": ("2", "sedeo", "sedi", "sessum"),
    "stare": ("1", "sto", "steti", "statum"),
    "dormire": ("4", "dormio", "dormivi", "dormitum"),
    "edere": ("3", "edo", "edi", "esum"),
    "bibere": ("3", "bibo", "bibi", None),
    "scire": ("4", "scio", "scivi", "scitum"),
    "putare": ("1", "puto", "putavi", "putatum"),
    "vivere": ("3", "vivo", "vixi", "victum"),
}

CONJ_ENDINGS = {
    "1": ["o", "as", "at", "amus", "atis", "ant"],
    "2": ["eo", "es", "et", "emus", "etis", "ent"],
    "3": ["o", "is", "it", "imus", "itis", "unt"],
    "3io": ["io", "is", "it", "imus", "itis", "iunt"],
    "4": ["io", "is", "it", "imus", "itis", "iunt"],
}
CONJ_STEM_CUT = {"1": "are", "2": "ere", "3": "ere", "3io": "ere", "4": "ire"}
PERSONEN_LA = ["ego", "tu", "is", "nos", "vos", "ei"]

IRREGULAR_PRAESENS = {
    "esse": ["sum", "es", "est", "sumus", "estis", "sunt"],
    "ire": ["eo", "is", "it", "imus", "itis", "eunt"],
}
IRREGULAR_PARTS = {
    "esse": {"praesens": "sum", "perfekt": "fui", "supin": None},
    "ire": {"praesens": "eo", "perfekt": "ii", "supin": "itum"},
}


def deklinieren(wort, genus, dekl, genitiv):
    if dekl == 1:
        stamm = genitiv[:-2]  # '...ae' -> stamm
        sg = {"nom": wort, "gen": stamm + "ae", "dat": stamm + "ae", "akk": stamm + "am", "abl": stamm + "a"}
        pl = {"nom": stamm + "ae", "gen": stamm + "arum", "dat": stamm + "is", "akk": stamm + "as", "abl": stamm + "is"}
        return {"sg": sg, "pl": pl}
    if dekl == 2:
        stamm = genitiv[:-1]  # '...i' -> stamm
        if genus == "n":
            sg = {"nom": wort, "gen": stamm + "i", "dat": stamm + "o", "akk": wort, "abl": stamm + "o"}
            pl = {"nom": stamm + "a", "gen": stamm + "orum", "dat": stamm + "is", "akk": stamm + "a", "abl": stamm + "is"}
        else:
            sg = {"nom": wort, "gen": stamm + "i", "dat": stamm + "o", "akk": stamm + "um", "abl": stamm + "o"}
            pl = {"nom": stamm + "i", "gen": stamm + "orum", "dat": stamm + "is", "akk": stamm + "os", "abl": stamm + "is"}
        return {"sg": sg, "pl": pl}
    if dekl == 3:
        stamm = genitiv[:-2]  # '...is' -> stamm
        abl = stamm + "i" if wort in ISTAMM_NEUTER_ABL_I else stamm + "e"
        akk = wort if genus == "n" else stamm + "em"
        sg = {"nom": wort, "gen": stamm + "is", "dat": stamm + "i", "akk": akk, "abl": abl}
        return {"sg": sg}  # bewusst kein Plural (i-Stamm-Risiko)
    raise ValueError(f"Deklination {dekl} nicht unterstuetzt: {wort}")


def konjugieren_praesens(infinitiv, klasse):
    cut = CONJ_STEM_CUT[klasse]
    assert infinitiv.endswith(cut), f"{infinitiv} passt nicht zu Klasse {klasse}"
    stamm = infinitiv[: -len(cut)]
    formen = [stamm + e for e in CONJ_ENDINGS[klasse]]
    return dict(zip(PERSONEN_LA, formen))


def main():
    with open(VOK_PATH, "r", encoding="utf-8") as f:
        vok = json.load(f)

    n_nomen = n_verb = n_skip = 0
    for v in vok:
        wort = v["it"]
        if wort in NOMEN_META:
            genus, dekl, genitiv = NOMEN_META[wort]
            dek = deklinieren(wort, genus, dekl, genitiv)
            v["wortart"] = "nomen"
            v["genus"] = genus
            v["deklination"] = dekl
            v["genitiv"] = genitiv
            v["formen"] = dek
            n_nomen += 1
        elif wort in IRREGULAR_PRAESENS:
            v["wortart"] = "verb"
            v["konjugation"] = "irregular"
            v["praesens"] = dict(zip(PERSONEN_LA, IRREGULAR_PRAESENS[wort]))
            v["stammformen"] = IRREGULAR_PARTS[wort]
            v["formen"] = v["praesens"]
            n_verb += 1
        elif wort in VERB_META:
            klasse, praes1, perf1, ppp = VERB_META[wort]
            praesens = konjugieren_praesens(wort, klasse)
            assert praesens["ego"] == praes1, f"{wort}: erwartet {praes1}, berechnet {praesens['ego']}"
            v["wortart"] = "verb"
            v["konjugation"] = klasse
            v["praesens"] = praesens
            v["stammformen"] = {"praesens": praes1, "infinitiv": wort, "perfekt": perf1, "supin": ppp}
            v["formen"] = praesens
            n_verb += 1
        else:
            v["wortart"] = "vokabel"
            n_skip += 1

    with open(VOK_PATH, "w", encoding="utf-8") as f:
        json.dump(vok, f, ensure_ascii=False, indent=2)

    print(f"Nomen dekliniert: {n_nomen}, Verben konjugiert: {n_verb}, unveraendert: {n_skip}, gesamt: {len(vok)}")

    # Stichproben zur Kontrolle
    by_it = {v["it"]: v for v in vok}
    for w in ["mare", "magister", "liber", "puer", "dare", "stare", "facere", "esse", "ire"]:
        print(w, "=>", by_it[w].get("formen"))


if __name__ == "__main__":
    main()
