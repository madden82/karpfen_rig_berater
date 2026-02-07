import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen Rig Empfehlung", layout="wide")

# CSS für bessere Mobile-Bedienung
st.markdown("""
    <style>
    .stSlider { padding-bottom: 20px; }
    .stHeader { font-size: 1.5rem !important; }
    @media (max-width: 640px) {
        .main { padding: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Karpfen Rig Empfehlung")
st.caption("Einsatzplanung v4.3 | Mobile Optimierung & Bereinigte Texte")

# ==========================================
# 1. PHASE: GEWÄSSER & UMWELT
# ==========================================
st.header("📍 Schritt 1: Gewässer & Umwelt")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp wählen", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Aktuelle Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    tiefe_max = st.number_input("Maximale Tiefe des Gewässers (m)", 1.0, 50.0, 8.0, step=0.1)
    tiefe_spot = st.number_input("Tiefe an deinem Angelplatz (m)", 0.5, 40.0, 3.0, step=0.1)

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit wählen", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)"])
    hindernisse = st.multiselect("Hindernisse / Gefahren am Platz", [
        "Muschelbänke", "Totholz", "Kraut (leicht)", "Kraut-Dschungel", 
        "Fadenalgen", "Scharfe Kanten", "Krebse", "Schiffsverkehr"
    ], placeholder="Wählen...")

with c3:
    st.markdown("**Wind & Wasser**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Mittel", "Klar", "Glasklar"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leicht", "Mittel", "Stark"])
    # Klammern und Zusatztexte entfernt
    windrichtung = st.selectbox("Windrichtung zum Spot", ["Gegenwind", "Rückenwind", "Seitenwind"])
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)

# ==========================================
# 2. PHASE: TAKTIK & BESTAND
# ==========================================
st.header("🎯 Schritt 2: Taktik & Fischbestand")
t1, t2 = st.columns(2)

wurfweite = 0
taktik_typ = "Ablegen"

with t1:
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    if ausbringung == "Boot":
        boot_taktik = st.radio("Boot-Taktik:", ["Ablegen", "Werfen"], horizontal=True)
        if boot_taktik == "Werfen":
            taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 5, 100, 30)
    elif ausbringung == "Wurf vom Ufer":
        taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 10, 180, 70)

with t2:
    st.markdown("**Bestand (andere Fischarten)**")
    weissfisch = st.select_slider("Vorkommen anderer Weißfische (Brassen/Rotaugen/etc.)", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    aktivitaet = st.select_slider("Aktivität der Karpfen", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Max. erwartetes Karpfengewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE
# ==========================================

def berechne_pro_logic():
    setup = {
        "rig": "Haar-Rig (Hair Rig)",
        "haken": "4 bis 6",
        "blei": 95,
        "montage": "Safety Clip",
        "optimum": "Ummanteltes Geflecht (25lb)",
        "braid_alt": "Weiches Geflecht (20lb) + Anti-Tangle-Hülse",
        "begruendung": []
    }

    if windrichtung == "Gegenwind":
        setup["begruendung"].append("➔ **Wind:** Gegenwind drückt Nahrung und warmes Oberflächenwasser an dein Ufer. Top Spot!")
    
    if jahreszeit == "Winter" or temp < 6:
        setup["haken"] = "6 bis 10 (sehr fein)"
        setup["begruendung"].append("➔ **Kaltwasser:** Minimale Ködergröße und feinste Haken verwenden.")

    if weissfisch in ["Hoch", "Extrem"]:
        setup["begruendung"].append("➔ **Weißfisch-Druck:** Harte Köder und selektive Montagen wählen.")
        
    if any(h in str(hindernisse) for h in ["Muschel", "Totholz", "Kante"]):
        setup["haken"] = "2 bis 4 (Starkdrahtig)"
        setup["optimum"] = "Fluorocarbon-Schlagschnur + Snag-Link"
        setup["begruendung"].append("➔ **Schutz:** Hindernisse erfordern verstärktes Material.")

    return setup

ergebnis = berechne_pro_logic()

def berechne_futter():
    basis = 0.5 
    if jahreszeit == "Herbst": basis += 2.0
    elif jahreszeit == "Winter": basis = 0.1
    if temp > 20: basis += 1.0
    if weissfisch == "Extrem": basis += 2.5
    art = "Harte Boilies" if weissfisch in ["Hoch", "Extrem"] else "Mix (Boilies/Partikel)"
    return round(basis, 1), art

f_menge, f_art = berechne_futter()

# ==========================================
# 4. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup")

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Montage & Rig")
    st.metric("Blei", f"{ergebnis['blei']} g")
    st.success(f"**Rig-Typ:** {ergebnis['rig']}")
    st.write(f"**Haken:** Gr. {ergebnis['haken']}")

with o2:
    st.subheader("🪝 Vorfach-Material")
    st.success(f"**Optimum:** {ergebnis['optimum']}")
    st.info(f"**Geflecht-Alternative:** {ergebnis['braid_alt']}")

with o3:
    st.subheader("🥣 Futter am Spot")
    st.metric("Menge ca.", f"{f_menge} kg / Tag")
    st.write(f"**Empfehlung:** {f_art}")

st.divider()
st.subheader("💡 Taktische Analyse")
for punkt in ergebnis["begruendung"]:
    st.write(punkt)

# ==========================================
# 5. DISCLAIMER
# ==========================================
st.markdown("---")
st.caption("""
**Hinweis:** Die hier ausgegebenen Ergebnisse basieren auf fundierten Erfahrungswerten für bewährte Karpfen-Montagen. 
Jedes Gewässer hat seine eigenen Gesetze. Nutze diese Empfehlung als solide Basis und passe Details stets an die 
örtliche Situation an. Auch andere Rigs können unter speziellen Bedingungen gleichermaßen fängig sein.
""")
