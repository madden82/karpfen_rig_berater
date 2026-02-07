import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-Taktik Berater Pro", layout="wide")

st.title("🎖️ Karpfen-Taktik Berater Pro")
st.caption("Einsatzplanung v4.0 | Präzisions-Tiefen & Spot-Analyse")

# ==========================================
# 1. PHASE: GEWÄSSER & UMWELT
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp wählen", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Aktuelle Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    # Jetzt mit 0.1m Schritten für maximale Präzision
    tiefe_max = st.number_input("Maximale Tiefe des Gewässers (m)", 1.0, 50.0, 8.0, step=0.1)
    tiefe_spot = st.number_input("Tiefe an deinem Angelplatz (m)", 0.5, 40.0, 3.0, step=0.1)

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit wählen", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)"])
    hindernisse = st.multiselect("Hindernisse am Platz", [
        "Muschelbänke", "Totholz", "Kraut (leicht)", "Kraut-Dschungel", 
        "Fadenalgen", "Scharfe Kanten", "Krebse", "Schiffsverkehr"
    ], placeholder="Wählen Sie Hindernisse...")

with c3:
    st.markdown("**Wind & Wasser**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Mittel", "Klar", "Glasklar"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leicht", "Mittel", "Sturm"])
    windrichtung = st.selectbox("Windrichtung zum Spot", ["Auflandig (Wind drauf)", "Ablandig (Rückenwind)", "Seitenwind"])
    temp = st.slider("Wassertemperatur (°C)", 2, 30, 15)

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
    weissfisch = st.select_slider("Weißfisch-Aufkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    aktivitaet = st.select_slider("Fisch-Aktivität", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    # Optimierte Bezeichnung
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
        "spot_tipp": "",
        "begruendung": []
    }

    # --- SPOT-GUIDING ---
    if jahreszeit == "Frühjahr":
        setup["spot_tipp"] = "Flachwasser-Zonen (0.5m - 2m) befischen. Auflandiger Wind bringt hier Wärme & Nahrung."
    elif jahreszeit == "Sommer":
        if tiefe_max > 6:
            setup["spot_tipp"] = "Sprungschicht beachten! Fische oft im Mittelwasser oder an Kanten zwischen 3m und 5m."
        else:
            setup["spot_tipp"] = "Sauerstoffreiche Bereiche (Einläufe, Windkanten) suchen."
    elif jahreszeit == "Herbst":
        setup["spot_tipp"] = "Plateaus und Muschelbänke in 3m - 6m Tiefe. Die Fische fressen für den Winter."
    elif jahreszeit == "Winter":
        setup["spot_tipp"] = "Tiefste Bereiche oder geschützte Standplätze suchen. Minimale Bewegung im Wasser."

    # --- HARDWARE-LOGIK ---
    if any("Kraut" in h for h in hindernisse):
        setup["rig"] = "Ronnie-Rig / Chod-Rig"
    
    if ziel_gewicht > 20 or any(h in str(hindernisse) for h in ["Muschel", "Totholz", "Kante"]):
        setup["haken"] = "2 bis 4 (Starkdrahtig)"
        setup["optimum"] = "Fluorocarbon-Schlagschnur + Snag-Link"
        setup["begruendung"].append("➔ **Schutz:** Hohes Fischgewicht & Hindernisse erfordern verstärktes Material.")

    if taktik_typ == "Wurf" and wurfweite > 100:
        setup["blei"] = 115
        setup["montage"] = "Helicopter-System"
        setup["begruendung"].append("➔ **Wurf:** Helicopter verhindert Verwicklungen bei Gewaltwürfen.")

    return setup

ergebnis = berechne_pro_logic()

# --- FUTTER-LOGIK ---
def berechne_futter():
    basis = 0.5 
    if jahreszeit == "Herbst": basis += 2.0
    elif jahreszeit == "Winter": basis = 0.1
    if aktivitaet == "Aggressiv": basis *= 1.5
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
    st.caption("Die Anti-Tangle-Hülse verhindert Verwicklungen beim Wurf.")

with o3:
    st.subheader("🥣 Futter & Spot")
    st.metric("Menge ca.", f"{f_menge} kg / Tag")
    st.write(f"**Spot-Tipp:** {ergebnis['spot_tipp']}")

st.divider()
st.subheader("💡 Taktische Analyse (Warum?)")
for punkt in ergebnis["begruendung"]:
    st.write(punkt)

# ==========================================
# 5. DISCLAIMER
# ==========================================
st.markdown("---")
st.caption("""
**Hinweis:** Die hier ausgegebenen Ergebnisse basieren auf fundierten Erfahrungswerten für bewährte Karpfen-Montagen. 
Jedes Gewässer hat seine eigenen Gesetze. Nutze diese Empfehlung als solide Basis und passe Details wie Haarlänge oder 
die exakte Position von Tungsten-Weights stets an die örtliche Situation an. Andere Rigs können unter speziellen 
Bedingungen ebenso zum Erfolg führen.
""")
