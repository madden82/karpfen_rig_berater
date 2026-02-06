import streamlit as st

# =========================
# Konfiguration
# =========================
st.set_page_config(
    page_title="🎣 Profi‑Karpfen Rig & Vorfach Berater",
    layout="centered"
)

st.title("🎣 Profi‑Karpfen Rig & Vorfach Berater")
st.caption("Detaillierte Baupläne für Carp Rigs — Profi‑tauglich und dynamisch angepasst")

# =========================
# Eingabebereich
# =========================

st.header("🌊 Gewässer & Umwelt")
gewaesser_typ = st.selectbox("Gewässertyp", ["Teich", "See", "Fluss", "Strom"])
st.caption("Teich/See: stehendes Wasser | Fluss/Strom: Strömung beachten")

fliessgeschwindigkeit = 0.0
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider(
        "Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1)
    st.caption("0 = kaum Strömung | 2 = starke Strömung (stabile Rigs nötig)")

jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
wasser_truebung = st.slider("Wassertrübung (0 = klar, 10 = trüb)", 0, 10, 3)
wassertemperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16)

st.header("🏞️ Boden & Pflanzen")
boden = st.selectbox("Bodenbeschaffenheit", ["hart", "weich", "schlammig"])
kraut = st.checkbox("Kraut vorhanden 🌿")
st.subheader("Hindernisse")
hindernisse_muscheln = st.checkbox("Muscheln / Steine")
hindernisse_aeste = st.checkbox("Äste / Unterholz")
hindernisse_grund = st.checkbox("Andere Hindernisse")
hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

st.header("🐟 Fisch & Angelbedingungen")
angeldruck = st.selectbox("Angeldruck", ["niedrig", "mittel", "hoch"])
vorsichtige_fische = angeldruck == "hoch"

weissfisch = st.slider("Weißfisch‑Anteil (%)", 0, 10, 4)
max_karpfen = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)

modus = st.radio("Ziel", ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"])
wurfweite = st.slider("Wurfweite (Meter)", 10, 120, 40)

# =========================
# Köder‑Empfehlung
# =========================

def koeder_empfehlung():
    if wassertemperatur < 10 or jahreszeit == "Winter":
        return "Pop‑Up", 14, "Kaltwasser & Winter – auffällig"
    if weissfisch >= 6:
        return "Harter Boilie", 22, "Schützt vor Weißfisch"
    if vorsichtige_fische:
        return "Wafter", 18, "Unauffällig & effektiv"
    if wasser_truebung > 6:
        return "Leuchtender Pop‑Up", 16, "Trübes Wasser – auffällig"
    return "Boilie", 20, "Standardköder – bewährt"

# =========================
# Rig‑Bibliothek (ausgewählte Profi‑Rigs, 25+)
# =========================
# Jeder Rig: name, einsatz, vorfach (Material, Länge), aufbau (Schritte)

RIG_LIBRARY = [
    # Beispielrigs, können erweitert werden
    {
        "name": "Hair Rig",
        "einsatz": "Universell, besonders Bodenköder",
        "vorfach": ("Mono", 25),
        "aufbau": [
            "1. Vorfach auf gewünschte Länge zuschneiden (15–30 cm)",
            "2. Haken anbinden (Größe abhängig vom Karpfengewicht)",
            "3. Haar mit Boiliestopper ausrichten",
            "4. Köder auf Haar aufziehen"
        ]
    },
    {
        "name": "Blowback Rig",
        "einsatz": "Bodenköder, hoher Hakeffekt",
        "vorfach": ("Mono weich", 20),
        "aufbau": [
            "1. Vorfach auf etwa 15–20 cm zuschneiden",
            "2. Rig Ring über Hakenschenkel ziehen",
            "3. Haken anbinden",
            "4. Köder über Haar und Stopper fixieren"
        ]
    },
    {
        "name": "Ronnie Rig",
        "einsatz": "Pop‑Ups knapp über Grund",
        "vorfach": ("Stiff", 18),
        "aufbau": [
            "1. Vorfachmaterial auf 15–20 cm zuschneiden",
            "2. Haken anbinden (Wide Gape)",
            "3. Anti‑Tangle Sleeve/Schlauch positionieren",
            "4. Pop‑Up am Haar fixieren"
        ]
    },
    {
        "name": "D‑Rig",
        "einsatz": "Pop‑Ups direkt am Ring",
        "vorfach": ("Stiff", 20),
        "aufbau": [
            "1. Vorfach (Fluorocarbon oder stiff) zuschneiden (20 cm)",
            "2. Ringwirbel auffädeln",
            "3. Haken anbinden und Ring durch Öhr führen",
            "4. Vorfach verdicken (leicht erhitzen)",
            "5. Pop‑Up befestigen"
        ]
    },
    {
        "name": "Chod Rig",
        "einsatz": "Weicher Grund, Kraut",
        "vorfach": ("Stiff", 12),
        "aufbau": [
            "1. Leadermaterial ~90–110 cm",
            "2. Ringwirbel auffädeln",
            "3. Kurzes steifes Vorfach (~12–15 cm)",
            "4. Stopper fixieren Vorfachposition",
            "5. Haken anbinden und Köder anbringen"
        ]
    },
    {
        "name": "Helicopter Rig",
        "einsatz": "Verhedderungsfrei bei Hindernissen",
        "vorfach": ("Mono", 20),
        "aufbau": [
            "1. Leadcore/Mono als Hauptbasis",
            "2. Wirbel & Perlen auffädeln",
            "3. Kurzes Vorfach anbinden",
            "4. Haken anbinden und Köder platzieren"
        ]
    },
    {
        "name": "Bolt Rig",
        "einsatz": "Starkes Selbsthaken bei Strömung",
        "vorfach": ("Stiff", 25),
        "aufbau": [
            "1. Vorfach zuschneiden (~25 cm)",
            "2. Haken anbinden",
            "3. Blei direkt ans Vorfach",
            "4. Köder fixieren"
        ]
    },
    {
        "name": "Wafter Rig",
        "einsatz": "Unauffällig, mittig im Wasser",
        "vorfach": ("Stiff", 18),
        "aufbau": [
            "1. Kurzes Vorfach zuschneiden (15–18 cm)",
            "2. Haken anbinden",
            "3. Wafter fixieren (Köder balancieren)"
        ]
    },
 
    # — Allround / Bodenköder —
    {
        "name": "Hair Rig",
        "einsatz": "Universell, besonders für Boilies",
        "vorfach": ("Mono", 25),
        "aufbau": [
            "1. Vorfach (Mono) auf 15–30 cm zuschneiden",
            "2. Haken anbinden (angepasst an Karpfengewicht)",
            "3. Haar mit Boiliestopper ausrichten",
            "4. Köder auf Haar aufziehen"
        ]
    },
    {
        "name": "Blowback Rig",
        "einsatz": "Bodenköder, sehr sicherer Hakeffekt",
        "vorfach": ("Mono weich", 20),
        "aufbau": [
            "1. Vorfach auf ca. 15–20 cm zuschneiden",
            "2. Rig‑Ring über Hakenschenkel ziehen",
            "3. Haken anbinden",
            "4. Köder (Boilie/Pop‑Up) fixieren"
        ]
    },

    # — Pop‑Up / erhöhte Präsentation —
    {
        "name": "Ronnie Rig",
        "einsatz": "Pop‑Ups knapp über Grund",
        "vorfach": ("Stiff", 18),
        "aufbau": [
            "1. Vorfach material auf 15–20 cm zuschneiden",
            "2. Haken anbinden (Wide Gape)",
            "3. Anti‑Tangle Sleeve/Schlauch positionieren",
            "4. Pop‑Up am Haar fixieren"
        ]
    },
    {
        "name": "D‑Rig",
        "einsatz": "Pop‑Ups direkt am Rig‑Ring",
        "vorfach": ("Stiff", 20),
        "aufbau": [
            "1. Vorfach zuschneiden (20 cm)",
            "2. Ringwirbel auffädeln",
            "3. Haken anbinden und Ring durch Öhr führen",
            "4. Vorfachende leicht verdicken",
            "5. Pop‑Up befestigen"
        ]
    },
    {
        "name": "Slip‑D Rig",
        "einsatz": "Variation des D‑Rig mit gleitendem Ring",
        "vorfach": ("Stiff", 20),
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Ringwirbel auffädeln",
            "3. Haken anbinden und Ring durch Öhr führen",
            "4. Stopper sauber setzen"
        ]
    },
    {
        "name": "Wafter Rig",
        "einsatz": "Unauffällige Präsentation fast am Grund",
        "vorfach": ("Stiff", 18),
        "aufbau": [
            "1. Vorfach zuschneiden (15–18 cm)",
            "2. Haken anbinden",
            "3. Wafter fixieren (balanciert den Köder)"
        ]
    },

    # — Rigs für schwierige Bedingungen —
    {
        "name": "Chod Rig",
        "einsatz": "Weicher Grund / Kraut",
        "vorfach": ("Stiff short", 12),
        "aufbau": [
            "1. Leadermaterial ~90–110 cm",
            "2. Ringwirbel auffädeln",
            "3. Kurzes steifes Vorfach (~12–15 cm)",
            "4. Stopper fixieren Vorfachposition",
            "5. Haken anbinden & Köder anbringen"
        ]
    },
    {
        "name": "Helicopter Rig",
        "einsatz": "Verhedderungsfrei über Hindernissen",
        "vorfach": ("Mono", 20),
        "aufbau": [
            "1. Leadcore/Mono als Basis",
            "2. Wirbel & Perlen auffädeln",
            "3. Kurzes Vorfach anbinden",
            "4. Haken anbinden & Köder platzieren"
        ]
    },
    {
        "name": "Beehive Rig",
        "einsatz": "Fester Sitz am Boden unter Hindernissen",
        "vorfach": ("Mono", 18),
        "aufbau": [
            "1. Vorfach kürzer zuschneiden (ca. 18 cm)",
            "2. Haken anbinden",
            "3. Kleine Perle preventiert Durchrutschen",
            "4. Köder auf Haar fixieren"
        ]
    },

    # — Strömungsbetonte Rigs —
    {
        "name": "Bolt Rig",
        "einsatz": "Starker Selbsthakeffekt bei Strömung",
        "vorfach": ("Stiff", 25),
        "aufbau": [
            "1. Vorfach zuschneiden (~25 cm)",
            "2. Haken anbinden",
            "3. Direktes Blei ans Vorfach",
            "4. Köder fixieren"
        ]
    },
    {
        "name": "Linguine Rig",
        "einsatz": "Strömung + Slacker Ground",
        "vorfach": ("Fluorocarbon", 22),
        "aufbau": [
            "1. Vorfach zuschneiden (20–22 cm)",
            "2. Haken anbinden",
            "3. Vorfach durch Strömungslinie ausrichten"
        ]
    },

    # — Grund‑ & Spezialmontagen —
    {
        "name": "Method Feeder Rig",
        "einsatz": "Futterplatz‑Fischen",
        "vorfach": ("Stiff", 20),
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Haken anbinden",
            "3. Rig am Method Feeder befestigen"
        ]
    },
    {
        "name": "KD Rig (Kenny Dorset)",
        "einsatz": "Universell & einfach",
        "vorfach": ("Fluorocarbon", 20),
        "aufbau": [
            "1. Vorfach zuschneiden (~20 cm)",
            "2. Haken anbinden (Curve Shank)",
            "3. Perle als Stopper nutzen",
            "4. Köder auf Haar aufziehen"
        ]
    },
    {
        "name": "Line‑Aligner Rig",
        "einsatz": "Perfekte Hakenausrichtung",
        "vorfach": ("Fluorocarbon", 20),
        "aufbau": [
            "1. Line Aligner über Hakenöhr schieben",
            "2. Vorfach anbinden",
            "3. Köder auf Haar platzieren"
        ]
    },
    {
        "name": "Teller Rig",
        "einsatz": "Stabil bei Grundstrukturen",
        "vorfach": ("Mono", 20),
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Teller‑Perle positionieren",
            "3. Haken anbinden",
            "4. Köder auf Haar fixieren"
        ]
    },

    # — Oberflächen‑ bzw. Spezial‑Rigs —
    {
        "name": "Zig Rig",
        "einsatz": "Köder in Wassersäule",
        "vorfach": ("Fluorocarbon", 40),
        "aufbau": [
            "1. Langes Vorfach zuschneiden (30–50 cm)",
            "2. Haken anbinden",
            "3. Poser‑Rigs oder leichte Pop‑Ups nutzen"
        ]
    },
    {
        "name": "Surface Rig",
        "einsatz": "Direkt unter der Oberfläche",
        "vorfach": ("Fluorocarbon", 40),
        "aufbau": [
            "1. Sehr langes Vorfach zuschneiden",
            "2. Haken anbinden",
            "3. Poser oder flotte Pop‑Ups nutzen"
        ]
    },

    # — Ergänzende Varianten —
    {
        "name": "Multi Rig / Twin Rig",
        "einsatz": "Zwei Köder gleichzeitig",
        "vorfach": ("Stiff", 30),
        "aufbau": [
            "1. Zwei Vorfachenden zuschneiden",
            "2. Beide Haken anbinden",
            "3. Beide Köder fixieren"
        ]
    },
    {
        "name": "Offset Rig",
        "einsatz": "Bodenköder, Anti‑Ausspucken",
        "vorfach": ("Mono", 25),
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Offset‑Haken anbinden",
            "3. Köder fixieren"
        ]
    }
]



# =========================
# Gewichtetes Punktesystem
# =========================
def score_rig(rig, koeder):
    score = 0
    name = rig["name"].lower()

    # Gewichtungen
    gewichtungen = {
        "pop_up": 10,
        "kraut": 8,
        "stroemung": 7,
        "vorsicht": 6,
        "boden_weich": 4,
        "allrounder": 3
    }

    # Pop-Up Köder
    if "pop‑up" in koeder.lower() and name in ["ronnie rig", "d‑rig", "chod rig"]:
        score += gewichtungen["pop_up"]

    # Kraut
    if kraut and name in ["chod rig", "helicopter rig"]:
        score += gewichtungen["kraut"]

    # Strömung
    if fliessgeschwindigkeit > 0.8 and name in ["bolt rig", "blowback rig"]:
        score += gewichtungen["stroemung"]

    # Vorsichtige Fische
    if vorsichtige_fische and name in ["d‑rig", "wafter rig", "slip‑d rig"]:
        score += gewichtungen["vorsicht"]

    # Boden weich
    if boden in ["weich", "schlammig"] and name in ["ronnie rig", "chod rig"]:
        score += gewichtungen["boden_weich"]

    # Allrounder
    if name in ["hair rig", "blowback rig"]:
        score += gewichtungen["allrounder"]

    return score

def rig_empfehlung(koeder):
    scored = [(score_rig(rig, koeder), rig) for rig in RIG_LIBRARY]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:2]]  # zwei beste Rigs

# =========================
# Ausgabe
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    koeder, groesse, koeder_text = koeder_empfehlung()
    rigs = rig_empfehlung(koeder)

    # Dynamische Hakenwahl
    if max_karpfen >= 25:
        haken = "Größe 4 Wide Gape"
    else:
        haken = "Größe 6 Wide Gape"

    st.success("✅ Deine persönliche Empfehlung")

    st.subheader("📋 Übersicht")
    rig_namen = ", ".join([r["name"] for r in rigs])
    st.write(f"**Rig:** {rig_namen}")
    st.write(f"**Haken:** {haken}")
    st.write(f"**Vorfachmaterial:** {', '.join([v[0] for v in [r['vorfach'] for r in rigs]])}")
    st.write(f"**Vorfachlänge:** {', '.join([str(v[1])+' cm' for v in [r['vorfach'] for r in rigs]])}")

    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {groesse} mm")
    st.caption(koeder_text)

    st.subheader("🪝 Empfohlene Rigs (Bauplan)")
    for rig in rigs:
        st.write(f"**{rig['name']}** ({rig['einsatz']})")
        for schritt in rig["aufbau"]:
            st.write(schritt)

    st.subheader("⚖️ Blei")
    blei = 80
    form = "Inline"
    if wurfweite > 60:
        blei += 20
        form = "Distance"
    if "muscheln/steine" in hindernisse:
        blei += 10
    if fliessgeschwindigkeit > 0.8:
        blei += 20
    st.write(f"{blei} g – {form}")
    st.caption("Blei hilft bei Stabilität und Wurfweite")
