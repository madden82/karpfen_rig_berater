import streamlit as st

# =========================
# Seite konfigurieren
# =========================
st.set_page_config(
    page_title="🎣 Profi-Karpfen Rig Berater",
    layout="centered"
)

st.title("🎣 Profi-Karpfen Rig & Vorfach Berater")
st.caption("Optimiert für Fangquote & Sicherheit – mobil bedienbar")

# =========================
# Eingaben mit Tooltips und Erklärung
# =========================
st.header("📍 Gewässer & Bedingungen")

boden = st.selectbox(
    "Bodenbeschaffenheit 🏞️",
    ["hart", "weich", "schlammig"],
    help="Bodenart beeinflusst, welches Rig am besten aufliegt."
)

kraut = st.checkbox("Kraut vorhanden 🌿", help="Kraut am Grund kann Köder verdecken oder verfangen.")

st.subheader("Hindernisse ⛔")
hindernisse_muscheln = st.checkbox("Muscheln / Steine", help="Kann das Vorfach beschädigen")
hindernisse_aeste = st.checkbox("Äste / Unterholz", help="Hindernisse für den Köder")
hindernisse_grund = st.checkbox("Andere Hindernisse", help="Sonstige Hindernisse am Gewässergrund")

hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

angeldruck = st.selectbox(
    "Angeldruck 🎣",
    ["niedrig", "mittel", "hoch"],
    help="Je mehr Angelruten in der Nähe, desto vorsichtiger sind die Fische."
)
vorsichtige_fische = angeldruck == "hoch"

wasser_truebung = st.slider(
    "Wassertrübung (0=klar, 10=trüb) 💧",
    0, 10, 3,
    help="Beeinflusst Köderfarbe und Sichtbarkeit."
)

wassertemperatur = st.slider(
    "Wassertemperatur (°C) 🌡️",
    4, 30, 16,
    help="Wassertemperatur beeinflusst Aktivität und Fressverhalten der Karpfen."
)

gewaesser_typ = st.selectbox(
    "Gewässertyp 🌊",
    ["Teich", "See", "Fluss", "Strom"],
    help="Die Art des Gewässers beeinflusst Strömung und Köderwahl."
)
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider(
        "Fließgeschwindigkeit (m/s) 🌊",
        0.0, 2.0, 0.5, 0.1,
        help="Schnelle Strömung erfordert stabilere Rigs und Vorfächer."
    )
else:
    fliessgeschwindigkeit = 0

wurfweite = st.slider("Wurfweite (Meter) 🎯", 10, 120, 40)
max_karpfen = st.slider("Erwartetes Karpfengewicht (kg) 🐟", 5, 35, 15)
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)

jahreszeit = st.selectbox(
    "Jahreszeit 🍂",
    ["Frühling", "Sommer", "Herbst", "Winter"],
    help="Karpfen fressen je nach Jahreszeit unterschiedlich aktiv."
)

modus = st.radio(
    "Ziel",
    ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"],
    help="Maximale Fangquote = aggressiver, sichtbarer Köder. Maximale Sicherheit = vorsichtig & unauffällig."
)

# =========================
# Logik (wie zuvor, nur unverändert)
# =========================
def rig_empfehlung():
    if gewaesser_typ in ["Fluss", "Strom"] and fliessgeschwindigkeit > 1.0:
        rig_name = "Heavy Hair Rig"
        rig_aufbau = (
            "- Haarlänge: 1–2 cm\n"
            "- Schrumpfschlauch: ja\n"
            "- Wirbel: stabil, Anti-Twist\n"
            "- Haken: Größe 4 Wide Gape"
        )
        return rig_name, "Für stark fließendes Wasser optimiert", rig_aufbau

    if hindernisse and modus.startswith("🛡"):
        rig_name = "Hair Rig"
        rig_aufbau = (
            "- Haarlänge: 1–2 cm\n"
            "- Schrumpfschlauch: ja\n"
            "- Wirbel: kleiner Wirbel für Abrieb\n"
            "- Haken: Größe 4 Wide Gape"
        )
        return rig_name, "Maximale Sicherheit bei Hindernissen", rig_aufbau

    if kraut or boden in ["weich", "schlammig"]:
        rig_name = "Ronnie Rig"
        rig_aufbau = (
            "- Haarlänge: 1,5–2 cm\n"
            "- Schrumpfschlauch: optional\n"
            "- Wirbel: Standard\n"
            "- Haken: Größe 6 Wide Gape"
        )
        return rig_name, "Köder bleibt über Kraut & weichem Boden", rig_aufbau

    if vorsichtige_fische:
        rig_name = "D-Rig"
        rig_aufbau = (
            "- Haarlänge: 1 cm\n"
            "- Schrumpfschlauch: optional\n"
            "- Wirbel: Standard\n"
            "- Haken: Größe 6 Curve Shank"
        )
        return rig_name, "Sehr unauffällig für stark beangelte Fische", rig_aufbau

    rig_name = "Blowback Rig"
    rig_aufbau = (
        "- Haarlänge: 1–1,5 cm\n"
        "- Schrumpfschlauch: optional\n"
        "- Wirbel: Standard\n"
        "- Haken: Größe 6 Wide Gape"
    )
    return rig_name, "Allround-Rig mit hoher Hakeffizienz", rig_aufbau

def vorfach_empfehlung(rig):
    if fliessgeschwindigkeit > 0.8:
        return "Stiff + heavier", 25, 25, "Strömungsbeständiges Vorfach"
    if hindernisse:
        return "Kombi-Vorfach (coated braid + stiff)", 20, 25, "Abriebschutz & Kontrolle"
    if vorsichtige_fische and wasser_truebung < 4:
        return "Fluorocarbon", 30, 15, "Nahezu unsichtbar im klaren Wasser"
    if rig in ["Ronnie Rig", "D-Rig"]:
        return "Stiff", 25, 20, "Stabile Köderführung"
    return "Mono", 25, 15, "Unkompliziert & zuverlässig"

def haken_empfehlung():
    if max_karpfen >= 20:
        return "Größe 4 Wide Gape (starker Draht)", "Für große & kampfstarke Karpfen"
    if vorsichtige_fische:
        return "Größe 6 Curve Shank", "Verbessert Hookups bei vorsichtigen Fischen"
    return "Größe 6 Wide Gape", "Allround-Haken"

def blei_empfehlung():
    gewicht = 80
    form = "Inline"
    if wurfweite > 60:
        gewicht += 20
        form = "Distance"
    if "muscheln/steine" in hindernisse:
        gewicht += 10
    if fliessgeschwindigkeit > 0.8:
        gewicht += 20
    return gewicht, form

def koeder_empfehlung():
    if wassertemperatur < 10 or jahreszeit == "Winter":
        return "Pop-Up", 14, "Kaltwasser / Winter – leicht & auffällig"
    if weissfisch >= 6:
        return "Harter Boilie", 22, "Schützt vor Weißfisch"
    if vorsichtige_fische:
        return "Wafter", 18, "Unauffällig & effektiv"
    if wasser_truebung > 6:
        return "Leuchtender Pop-Up", 16, "Trübes Wasser – auffälliger Köder"
    return "Boilie", 20, "Bewährter Standardköder"

# =========================
# Ausgabe mit Profi-Layout
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    rig, rig_grund, rig_aufbau = rig_empfehlung()
    vorfach, laenge, staerke, vorfach_grund = vorfach_empfehlung(rig)
    haken, haken_grund = haken_empfehlung()
    blei, blei_form = blei_empfehlung()
    koeder, groesse, koeder_grund = koeder_empfehlung()

    st.success("✅ Deine persönliche Empfehlung")

    st.subheader("🪝 Rig")
    st.write(f"**{rig}**")
    st.caption(rig_grund)
    st.text(rig_aufbau)

    st.subheader("🧵 Vorfach")
    st.write(f"{vorfach}, {laenge} cm, {staerke} lb")
    st.caption(vorfach_grund)

    st.subheader("🎣 Haken")
    st.write(haken)
    st.caption(haken_grund)

    st.subheader("⚖️ Blei")
    st.write(f"{blei} g – {blei_form}")

    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {groesse} mm")
    st.caption(koeder_grund)

    st.info("🎯 Tipp: Passe Rig & Vorfach regelmäßig an Gewässer, Jahreszeit und Fischverhalten an.")
