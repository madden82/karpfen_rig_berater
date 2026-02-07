import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-Taktik Berater Pro", layout="wide")

st.title("🎖️ Karpfen-Taktik Berater Pro")
st.caption("Einsatzplanung v3.8 | Spot-Guiding & Jahreszeiten-Logik")

# ==========================================
# 1. PHASE: GEWÄSSER & UMWELT
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp wählen", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Aktuelle Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    tiefe_max = st.number_input("Maximale Tiefe des Gewässers (m)", 1.0, 50.0, 8.0)
    tiefe_spot = st.number_input("Tiefe an deinem gewählten Spot (m)", 0.5, 40.0, 3.0)

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit wählen", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)"])
    hindernisse = st.multiselect("Hindernisse am Platz", [
        "Muschelbänke", "Totholz", "Kraut (leicht)", "Kraut-Dschungel", 
        "Fadenalgen", "Scharfe Kanten", "Krebse", "Schiffsverkehr"
    ], placeholder="Wählen...")

with c3:
    st.markdown("**Wind & Wasser**")
    wasser_klarheit = st.select_slider("Sichttiefe", options=["Trüb", "Mittel", "Klar", "Glasklar"])
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
    ausbringung = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    if ausbringung == "Boot":
        boot_taktik = st.radio("Boot-Taktik:", ["Ablegen", "Werfen"], horizontal=True)
        if boot_taktik == "Werfen":
            taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 5, 100, 30)
    elif ausbringung == "Wurf vom Ufer":
        taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 10, 180, 70)

with t2:
    weissfisch = st.select_slider("Weißfisch-Aufkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    aktivitaet = st.select_slider("Fisch-Aktivität", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE (Logik & Spot-Tipps)
# ==========================================

def berechne_full_logic():
    setup = {
        "rig": "Haar-Rig (Hair Rig)",
        "haken": "4 bis 6",
        "blei": 95,
        "montage": "Safety Clip",
        "optimum": "Ummanteltes Geflecht (25lb)",
        "braid_alt": "Weiches Geflecht (20lb) + Hülse",
        "spot_tipp": "",
        "begruendung": []
    }

    # --- SPOT-GUIDING LOGIK ---
    if jahreszeit == "Frühjahr":
        setup["spot_tipp"] = "Suche flache, sonnige Buchten (0.5m - 2m). Dort erwärmt sich das Wasser zuerst."
        if windrichtung == "Auflandig (Wind drauf)":
            setup["spot_tipp"] += " Der warme Oberflächenwind drückt das warme Wasser genau in dein Ufer!"
    elif jahreszeit == "Sommer":
        setup["spot_tipp"] = "Fische an Kanten zum Tiefen oder in sauerstoffreichen Bereichen (Windkante/Zufluss)."
        if temp > 22: setup["spot_tipp"] = "Sauerstoffmangel droht: Suche schattige Plätze oder springende Fische im Freiwasser."
    elif jahreszeit == "Herbst":
        setup["spot_tipp"] = "Große Fressphase! Suche Plateaus in mittlerer Tiefe oder Muschelbänke."
    elif jahreszeit == "Winter":
        setup["spot_tipp"] = "Tiefe, ruhige Bereiche. Minimale Bewegung. Die Fische stehen oft gestapelt am tiefsten Punkt."

    # --- RIG & MATERIAL LOGIK (Auszug) ---
    if any("Kraut" in h for h in hindernisse):
        setup["rig"] = "Ronnie- oder Chod-Rig"
        setup["begruendung"].append("➔ **Rig:** Pop-Up gewählt, um über dem Kraut zu fischen.")
    
    if jahreszeit == "Winter" or aktivitaet == "Vorsichtig":
        setup["haken"] = "6 bis 8"
        setup["begruendung"].append("➔ **Winter-Modus:** Kleinere Haken und feineres Besteck erhöhen die Chance bei trägen Fischen.")

    return setup

ergebnis = berechne_full_logic()

# --- FUTTER-LOGIK ---
def berechne_futter():
    basis = 0.5 
    if jahreszeit == "Herbst": basis += 2.0 # Volles Futter im Herbst
    elif jahreszeit == "Winter": basis = 0.1 # Nur winzige Mengen
    if aktivitaet == "Aggressiv": basis *= 1.5
    if weissfisch == "Extrem": basis += 2.0
    art = "Harte Boilies" if weissfisch in ["Hoch", "Extrem"] else "Mix (Partikel/Boilies)"
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
    st.info(f"**Alternative:** {ergebnis['braid_alt']}")

with o3:
    st.subheader("🥣 Futter & Spot")
    st.metric("Menge", f"{f_menge} kg / Tag")
    st.write(f"**Empfehlung:** {f_art}")

st.divider()
c_anal1, c_anal2 = st.columns(2)
with c_anal1:
    st.subheader("🗺️ Strategischer Spot-Tipp")
    st.info(ergebnis["spot_tipp"])
with c_anal2:
    st.subheader("💡 Taktische Analyse")
    for punkt in ergebnis["begruendung"]:
        st.write(punkt)
    if jahreszeit == "Winter":
        st.error("❄️ Winter-Warnung: Stoffwechsel ist extrem niedrig. Füttere fast gar nicht!")
