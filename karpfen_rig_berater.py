import streamlit as st

# ==========================================
# KONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="Karpfen-Rig Kalkulator PRO", layout="wide")

st.title("🎣 Professioneller Karpfen-Rig Kalkulator")
st.markdown("---")

# ==========================================
# DATENBANKEN
# ==========================================
basis_blei_map = {1: 12, 3: 25, 5: 35, 10: 50, 15: 60, 20: 70, 25: 80, 30: 90, 35: 100, 40: 110}

rigs_datenbank = {
    "Line-Aligner": {"boden": ["hart", "mittel"], "fischverhalten": ["aktiv", "beide"], "max_wurf": 120, "strom_max": 0.85, "grund": "Haken kippt sofort. Ideal für Bodenköder."},
    "Snowman": {"boden": ["hart", "mittel", "weich"], "fischverhalten": ["aktiv", "beide"], "max_wurf": 100, "strom_max": 1.22, "grund": "Kombination aus sinkendem & schwimmendem Köder."},
    "D-Rig": {"boden": ["hart"], "fischverhalten": ["scheu", "beide"], "max_wurf": 150, "strom_max": 0.6, "grund": "Maximale Köderbeweglichkeit, sehr unauffällig."},
    "KD-Rig": {"boden": ["hart", "mittel", "weich"], "fischverhalten": ["aktiv", "scheu", "beide"], "max_wurf": 120, "strom_max": 1.05, "grund": "Aggressiver Winkel durch tief sitzendes Haar."},
    "Combi Pop-Up": {"boden": ["mittel", "weich", "hart"], "fischverhalten": ["aktiv", "beide"], "max_wurf": 200, "strom_max": 1.5, "grund": "Perfekt für Pop-Ups über leichtem Kraut/Schlamm."},
    "Helikopter": {"boden": ["weich", "mittel", "hart"], "fischverhalten": ["aktiv", "scheu", "beide"], "max_wurf": 200, "strom_max": 2.0, "grund": "Bestes Rig für weichen Boden und maximale Weite."}
}

# ==========================================
# SIDEBAR - BENUTZEREINGABEN
# ==========================================
st.sidebar.header("📋 Eingabedaten")

# Sektion 1: Gewässer
gew_typ = st.sidebar.selectbox("Gewässertyp", ["Seen/Teiche (Stillwasser)", "Flüsse/Kanäle (Fließwasser)"])
strom_option = "keine"
if "Fließwasser" in gew_typ:
    strom_option = st.sidebar.select_slider("Strömungsstärke", options=["leicht", "mittel", "stark"])

strom_m_s = {"keine": 0.0, "leicht": 0.2, "mittel": 0.6, "stark": 1.4}[strom_option]

# Sektion 2: Technik & Boden
angeltechnik = st.sidebar.radio("Technik", ["Wurf vom Ufer", "Boot / Futterboot"])
wurfweite = st.sidebar.slider("Wurfweite (m)", 0, 200, 50) if "Wurf" in angeltechnik else 0
boden = st.sidebar.selectbox("Bodenbeschaffenheit", ["hart", "mittel", "weich"])

# Sektion 3: Fisch & Umwelt
gewicht = st.sidebar.slider("Max. Karpfengewicht (kg)", 1, 40, 15)
fischverhalten = st.sidebar.selectbox("Karpfenverhalten", ["aktiv", "scheu", "beide"])
wasserqualitaet = st.sidebar.selectbox("Wasserqualität", ["klar", "leicht trüb", "trüb"])
season = st.sidebar.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
temperature = st.sidebar.slider("Wassertemperatur (°C)", 0, 30, 15)
hindernisse = st.sidebar.checkbox("Hindernisse am Spot?", value=False)

# ==========================================
# BERECHNUNGSLOGIK
# ==========================================
# Bleigewicht berechnen
basis = next((v for k, v in sorted(basis_blei_map.items()) if gewicht <= k), 110)
boden_f = {"weich": 0.9, "mittel": 1.0, "hart": 1.1}[boden]
strom_f = {"keine": 1.0, "leicht": 1.05, "mittel": 1.10, "stark": 1.20}[strom_option]
gewicht_effektiv = round(basis * boden_f * strom_f, 1)

# Vorfachlänge
vorfach_range = {"hart": (12, 20), "mittel": (18, 30), "weich": (25, 45)}
min_v, max_v = vorfach_range[boden]
vorfach_l = max_v if fischverhalten in ["scheu", "beide"] else (min_v + max_v) // 2

# Rig-Filterung
passende_rigs = [
    (name, info["grund"]) for name, info in rigs_datenbank.items()
    if boden in info["boden"] and (fischverhalten == "beide" or fischverhalten in info["fischverhalten"])
    and wurfweite <= info["max_wurf"] and strom_m_s <= info["strom_max"]
]

# ==========================================
# AUSGABE - HAUPTBEREICH
# ==========================================
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🛠️ Setup-Empfehlung")
    st.success(f"**Optimales Blei:** {gewicht_effektiv} g")
    st.info(f"**Vorfachlänge:** {vorfach_l} cm")
    
    st.subheader("💡 Empfohlene Rigs")
    if passende_rigs:
        for name, grund in passende_rigs[:2]:
            st.markdown(f"✅ **{name}**: {grund}")
    else:
        st.warning("Kein spezielles Rig unter diesen Bedingungen – Helikopter-Rig empfohlen!")

with col2:
    st.header("🌊 Konditionen")
    st.write(f"**Boden:** {boden.capitalize()}")
    st.write(f"**Strömung:** {strom_option.capitalize()}")
    st.write(f"**Wassertemperatur:** {temperature} °C")
    st.write(f"**Sicht:** {wasserqualitaet}")

st.markdown("---")

# ==========================================
# NEU: STRATEGISCHE SPOTWAHL (FINALE INFO)
# ==========================================
st.header("🎯 Strategische Spotwahl & Taktik")

def generiere_spotwahl():
    tipps = []
    
    # Thermik & Tiefe
    if temperature < 10:
        tipps.append("🌡️ **Tiefe suchen:** Das Wasser ist kalt. Suche die tiefsten Bereiche des Sees oder Bereiche mit absterbendem Kraut, die noch Restwärme speichern.")
    elif 10 <= temperature <= 20:
        tipps.append("🌡️ **Flachwasser-Check:** Optimale Fress-Temperatur. Die Fische ziehen oft in flachere Uferzonen, besonders dort, wo der Wind auf das Ufer drückt (Sauerstoff!).")
    else:
        tipps.append("🌡️ **Schatten & Tiefe:** Bei Hitze stehen die Fische oft im Schatten von Bäumen oder in tieferen, sauerstoffreicheren Schichten.")

    # Boden-Taktik
    if boden == "weich":
        tipps.append(f"💩 **Schlamm-Taktik:** Da dein Blei ({gewicht_effektiv}g) einsinken könnte, nutze ein Helikopter-Rig oder verlängere das Haar, damit der Köder nicht im Schlamm verschwindet.")
    elif boden == "hart":
        tipps.append("💎 **Präzision:** Auf hartem Boden fressen Karpfen oft aggressiv. Dein kurzes Vorfach ({vorfach_l}cm) wird hier perfekt haken.")

    # Sicherheit & Hindernisse
    if hindernisse:
        tipps.append("⚠️ **Hindernis-Gefahr:** Da Hindernisse vorhanden sind, solltest du 'Snag-Ears' verwenden und die Bremse fast geschlossen halten. Nutze ein Safety-Clip System.")

    # Visuelle Strategie
    if wasserqualitaet == "klar":
        tipps.append("👓 **Tarnung:** In klarem Wasser solltest du Fluorocarbon-Vorfächer nutzen und auf große Futterwolken verzichten (Misstrauen!).")
    else:
        tipps.append("👃 **Lockstoff:** Bei trübem Wasser spielt die Optik eine kleine Rolle. Nutze stark aromatisierte Köder (Dips/Liquids).")

    return tipps

# Anzeige der finalen Info-Box
with st.expander("KLICKE HIER FÜR DEINE INDIVIDUELLE TAKTIK", expanded=True):
    for tipp in generiere_spotwahl():
        st.write(tipp)
    
    st.markdown(f"**Zusammenfassung:** Du angelst im **{season}** bei **{temperature}°C**. Dein Setup mit dem **{passende_rigs[0][0] if passende_rigs else 'Allround-Rig'}** ist optimal auf den **{boden}en** Boden abgestimmt. Konzentriere dich auf Stellen, an denen du Fischaktivität (Blasen, Springen) siehst!")

st.caption("Karpfen-Rig Kalkulator 2026 | Entwickelt für Streamlit")
