# -*- coding: utf-8 -*-
import json

# Handkuratierter Latein-Grundwortschatz (klassisches Latein, Standard-Zitierformen).
# 'it'-Feld = Latein (generischer Feldname aus der bestehenden App-Familie beibehalten,
# damit main.py/JS unveraendert funktionieren).
data = []

def add(kategorie, pairs):
    for it, de in pairs:
        data.append({"it": it, "de": de, "kategorie": kategorie})

add("Grundlagen", [
    ("salve", "Hallo (zu einer Person)"),
    ("salvete", "Hallo (zu mehreren)"),
    ("vale", "Auf Wiedersehen (zu einer Person)"),
    ("valete", "Auf Wiedersehen (zu mehreren)"),
    ("quaeso", "bitte"),
    ("gratias tibi ago", "danke"),
    ("ita", "ja"),
    ("minime", "nein"),
    ("amabo te", "bitte (dringende Bitte)"),
    ("quid agis", "wie geht es dir"),
    ("bene", "gut"),
    ("male", "schlecht"),
    ("fortasse", "vielleicht"),
    ("et", "und"),
    ("sed", "aber"),
    ("si", "wenn"),
    ("quia", "weil"),
    ("nunc", "jetzt"),
])

add("Zahlen", [
    ("unus", "eins"),
    ("duo", "zwei"),
    ("tres", "drei"),
    ("quattuor", "vier"),
    ("quinque", "fünf"),
    ("sex", "sechs"),
    ("septem", "sieben"),
    ("octo", "acht"),
    ("novem", "neun"),
    ("decem", "zehn"),
    ("centum", "hundert"),
    ("mille", "tausend"),
])

add("Farben", [
    ("albus", "weiß"),
    ("niger", "schwarz"),
    ("ruber", "rot"),
    ("viridis", "grün"),
    ("caeruleus", "blau"),
    ("flavus", "gelb"),
    ("purpureus", "purpurn"),
    ("fuscus", "braun"),
])

add("Familie", [
    ("pater", "Vater"),
    ("mater", "Mutter"),
    ("filius", "Sohn"),
    ("filia", "Tochter"),
    ("frater", "Bruder"),
    ("soror", "Schwester"),
    ("avus", "Großvater"),
    ("avia", "Großmutter"),
    ("puer", "Junge"),
    ("puella", "Mädchen"),
    ("vir", "Mann"),
    ("femina", "Frau"),
])

add("Natur", [
    ("aqua", "Wasser"),
    ("terra", "Erde"),
    ("caelum", "Himmel"),
    ("sol", "Sonne"),
    ("luna", "Mond"),
    ("stella", "Stern"),
    ("mons", "Berg"),
    ("silva", "Wald"),
    ("flumen", "Fluss"),
    ("mare", "Meer"),
    ("ventus", "Wind"),
    ("ignis", "Feuer"),
    ("arbor", "Baum"),
    ("flos", "Blume"),
])

add("Essen", [
    ("panis", "Brot"),
    ("vinum", "Wein"),
    ("lac", "Milch"),
    ("caro", "Fleisch"),
    ("piscis", "Fisch"),
    ("mel", "Honig"),
    ("pomum", "Frucht"),
    ("oleum", "Öl"),
    ("sal", "Salz"),
    ("cibus", "Speise"),
])

add("Zeit", [
    ("dies", "Tag"),
    ("nox", "Nacht"),
    ("hora", "Stunde"),
    ("annus", "Jahr"),
    ("mensis", "Monat"),
    ("hodie", "heute"),
    ("heri", "gestern"),
    ("cras", "morgen"),
    ("semper", "immer"),
    ("numquam", "nie"),
    ("saepe", "oft"),
])

add("Schule", [
    ("schola", "Schule"),
    ("magister", "Lehrer"),
    ("discipulus", "Schüler"),
    ("liber", "Buch"),
    ("littera", "Buchstabe"),
    ("verbum", "Wort"),
    ("lingua", "Sprache"),
    ("charta", "Papier"),
    ("stilus", "Schreibgriffel"),
])

add("Körper", [
    ("caput", "Kopf"),
    ("oculus", "Auge"),
    ("manus", "Hand"),
    ("pes", "Fuß"),
    ("cor", "Herz"),
    ("os", "Mund"),
    ("auris", "Ohr"),
    ("nasus", "Nase"),
])

add("Tiere", [
    ("canis", "Hund"),
    ("felis", "Katze"),
    ("equus", "Pferd"),
    ("avis", "Vogel"),
    ("leo", "Löwe"),
    ("ursus", "Bär"),
    ("serpens", "Schlange"),
    ("bos", "Rind"),
])

add("Adjektive", [
    ("magnus", "groß"),
    ("parvus", "klein"),
    ("bonus", "gut"),
    ("malus", "schlecht"),
    ("novus", "neu"),
    ("longus", "lang"),
    ("altus", "hoch"),
    ("multus", "viel"),
    ("omnis", "jeder"),
    ("pulcher", "schön"),
])

add("Personalpronomen", [
    ("ego", "ich"),
    ("tu", "du"),
    ("is", "er"),
    ("ea", "sie"),
    ("id", "es"),
    ("nos", "wir"),
    ("vos", "ihr"),
    ("ei", "sie (Plural)"),
])

add("Verben", [
    ("esse", "sein"),
    ("habere", "haben"),
    ("amare", "lieben"),
    ("videre", "sehen"),
    ("audire", "hören"),
    ("dicere", "sagen"),
    ("facere", "machen"),
    ("venire", "kommen"),
    ("ire", "gehen"),
    ("dare", "geben"),
    ("legere", "lesen"),
    ("scribere", "schreiben"),
    ("vocare", "rufen"),
    ("laudare", "loben"),
    ("pugnare", "kämpfen"),
    ("currere", "laufen"),
    ("sedere", "sitzen"),
    ("stare", "stehen"),
    ("dormire", "schlafen"),
    ("edere", "essen"),
    ("bibere", "trinken"),
    ("scire", "wissen"),
    ("putare", "glauben"),
    ("vivere", "leben"),
    ("mori", "sterben"),
])

for i, v in enumerate(data, start=1):
    v["id"] = i
    # Reihenfolge wie in den Bestandsapps: id, kategorie, it, de
    ordered = {"id": v["id"], "kategorie": v["kategorie"], "it": v["it"], "de": v["de"]}
    data[i-1] = ordered

print("Gesamt:", len(data))
cats = {}
for v in data:
    cats[v["kategorie"]] = cats.get(v["kategorie"], 0) + 1
for k, n in cats.items():
    print(f"  {k}: {n}")

with open(r"C:\Users\Klaus\VokabeltrainerLA\vokabeln.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
