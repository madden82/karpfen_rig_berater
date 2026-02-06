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
# 1️⃣ Gewässertyp & Umwelt
# =========================
st.header("🌊 Gewässer & Umwelt")

gewaesser_typ = st.selectbox("Gewässertyp", ["Teich", "See", "Fluss", "Strom"])
fliessgeschwindigkeit = 0
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider(
        "Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1
    )

jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
wasser_truebung = st.slider("Wassertrübung (0=klar, 10=trüb)", 0, 10, 3)
wassertemperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16)

# =========================
# 2️⃣ Boden & Pflanzen
# =========================
st.header("🏞️ Boden & Pflanzen")

boden = st.selectbox("Bodenbeschaffenheit", ["hart", "weich", "schlammig"])
kraut = st.checkbox("Kraut vorhanden 🌿")
st.subheader("Hindernisse ⛔")
hindernisse_muscheln = st.checkbox("Muscheln / Steine")
hindernisse_aeste = st.checkbox("Äste / Unterholz")
hindernisse_grund = st.checkbox("Andere Hindernisse")
hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

# =========================
# 3️⃣ Fisch & Angelbedingungen
# =========================
st.header("🐟 Fisch & Angelbedingungen")

angeldruck = st.selectbox("Angeldruck", ["niedrig", "mittel", "hoch"])
vorsichtige_fische = angeldruck == "hoch"
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)
max_karpfen = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)
modus = st.radio("Ziel", ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"])
wurfweite = st.slider("Wurfweite (Meter)", 10, 120, 40)

# =========================
# 4️⃣ Rig-Logik & Empfehlungen
# =========================
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

def rig_empfehlung(koeder):
    rigs = []

    # Hair Rig
    if koeder not in ["Pop-Up", "Leuchtender Pop-Up"] and not hindernisse and modus.startswith("🛡"):
        rigs.append({
            "name": "Hair Rig",
            "grund": "Allround, sicher für klare Wasserbedingungen",
            "aufbau": [
                "Haarlänge: 1–2 cm",
                "Schrumpfschlauch: optional (bei weichem Boden)",
                "Wirbel: nur bei Strömung >0.8 m/s",
                "Haken: Größe 6 Wide Gape"
            ],
            "video": "https://www.youtube.com/watch?v=HLWYQkm1GSo"
        })

    # Ronnie Rig
    if kraut or boden in ["weich", "schlammig"] or koeder in ["Pop-Up", "Leuchtender Pop-Up"]:
        rigs.append({
            "name": "Ronnie Rig",
            "grund": "Optimal für Kraut und Pop-Up",
            "aufbau": [
                "Haarlänge: 1,5–2 cm",
                "Schrumpfschlauch: nur bei Kraut oder weichem Boden",
                "Wirbel: klein für Abriebschutz",
                "Haken: Größe 6 Wide Gape",
                "Zusatzblei: 20 g bei Pop-Up"
            ],
            "video": "https://www.youtube.com/watch?v=cT3JHYmAvCc"
        })

    # D-Rig
    if vorsichtige_fische and koeder not in ["Pop-Up", "Leuchtender Pop-Up"]:
        rigs.append({
            "name": "D-Rig",
            "grund": "Unauffällig für vorsichtige Fische",
            "aufbau": [
                "Haarlänge: 1 cm",
                "Schrumpfschlauch: optional",
                "Wirbel: nicht nötig",
                "Haken: Größe 6 Curve Shank"
            ],
            "video": "https://www.youtube.com/watch?v=HLWYQkm1GSo"
        })

    # Blowback Rig
    if not rigs:
        rigs.append({
            "name": "Blowback Rig",
            "grund": "Allround-Rig mit hoher Hakeffizienz",
            "aufbau": [
                "Haarlänge: 1–1,5 cm",
                "Schrumpfschlauch: optional",
                "Wirbel: nicht nötig",
                "Haken: Größe 6 Wide Gape"
            ],
            "video": "https://www.youtube.com/watch?v=R8ZytVFI-mw"
        })

    # Weitere Profi-Rigs
    rigs += [
        {"name": "Chod Rig", "grund": "Ideal für weiche Böden oder Kraut", "aufbau":["Haar: 1,5–2 cm", "Schlauch: optional", "Wirbel: nur bei starker Strömung"], "video":"https://www.youtube.com/watch?v=HLWYQkm1GSo"},
        {"name": "Hinged Stiff Rig", "grund": "Köder stabil über Grund", "aufbau":["Haar: 1–1,5 cm", "Schlauch: optional", "Wirbel: optional"], "video":"https://www.youtube.com/watch?v=HLWYQkm1GSo"},
        {"name": "Helicopter Rig", "grund": "Geringes Verheddern bei Hindernissen", "aufbau":["Haar: 1,5 cm", "Wirbel: erforderlich", "Schrumpfschlauch: optional"], "video":"https://www.youtube.com/watch?v=HqNrPDiOKYU"},
        {"name": "Bolt Rig", "grund": "Stabil bei starken Strömungen", "aufbau":["Haar: 1–2 cm", "Wirbel: stabil", "Schlauch: optional"], "video":"https://www.youtube.co
