import streamlit as st

# =========================
# Setup
# =========================
st.set_page_config(page_title="Carp Tactical Commander Pro", layout="wide")

st.title("🎖️ Carp Tactical Commander Pro")
st.caption("Präzisions-Einsatzplanung | Version 2.1 (Refined Hook & Bait Logic)")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    # Gewässer unabhängig von der Tiefe
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Spot (m)", 0.5, 40.0, 4.0)
    stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand/Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Modder (faulig/stinkend)", "Kraut/Algen"])
    hindernisse = st.multiselect("Hindernisse am Spot", ["Muschelbänke", "Totholz/Äste", "Scharfe Kanten", "Versunkene Bauten"])

with c3:
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb (0-30cm)", "Medium (1m)", "Klar (3m+)", "Gin-Clear"])
    ph_algen = st.selectbox("Zustand/Algen", ["Normal", "Starke Algenblüte", "Hoher Sauerstoff (Wind/Zufluss)", "Sauerstoffarm (Hitze)"])

# ==========================================
# 2. PHASE: TAKTIK & AUSBRINGUNG
# ==========================================
st.header("🎯 Schritt 2: Taktik & Ausbringung")
t1, t2 = st.columns(2)

with t1:
    ausbringungs_methode = st.radio("Wie bringst du den Köder aus?", 
                                   ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    taktik_typ = "Ablegen"
    wurfweite = 0
    
    # Logik-Kette: Wurfweite erscheint NUR bei Wurf-Szenarien
    if ausbringungs_methode == "Boot":
        boot_taktik = st.radio("Taktik vom Boot:", ["Vom Boot ablegen", "Vom Boot werfen"], horizontal=True)
        if boot_taktik == "Vom Boot werfen":
            taktik_typ = "Wurf"
            wurfweite = st.slider("Benötigte Wurfweite (m)", 5, 100, 30)
    elif ausbringungs_methode == "Wurf vom Ufer":
        taktik_typ = "Wurf"
        wurfweite = st.slider("Benötigte Wurfweite (m)", 10, 180, 70)

with t2:
    jahreszeit = st.selectbox("Saison", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE
# ==========================================

def get_pro_setup():
    res = {
        "rig_name": "Standard Hair Rig",
        "material": "Coated Braid (25lb)",
        "hook_range": "4 - 6", # Default Range
        "lead_weight": 100,
        "lead_system": "Safety Clip",
        "bait_style": "Standard (Unauffällig)",
        "length": 18
    }

    # A. Köder- & Rig-Logik nach Wasserqualität
    if wasser_klarheit in ["Klar (3m+)", "Gin-Clear"]:
        res["bait_style"] = "Dezente Präsentation (Unauffällige Farben)"
        res["rig_name"] = "D-Rig oder Slip-D"
        res["material"] = "Fluorocarbon (0.40mm)"
    elif wasser_klarheit == "Trüb (0-30cm)":
        res["bait_style"] = "Optischer Reiz (Fluoro-Farben / Kontrast)"
    
    if boden_struktur == "Kraut/Algen":
        res["rig_name"] = "Ronnie- oder Chod-Rig"

    # B. Hakengrößen-Range (Dynamisch nach Fisch & Hindernis)
    if ziel_gewicht < 12:
        res["hook_range"] = "6 - 8"
    elif 12 <= ziel_gewicht <= 20:
        res["hook_range"] = "4 - 6"
    else: # Großfisch
        res["hook_range"] = "2 - 4"
        
    if len(hindernisse) > 0 or stromung == "Stark":
        res["hook_range"] = "2 - 4 (Dickdrahtig)"

    # C. Blei-Physik
    if taktik_typ == "Wurf":
        res["lead_weight"] = 120 if wurfweite > 90 else 90
        if wurfweite > 110: res["lead_system"] = "Helicopter (Anti-Tangle)"
    if stromung == "Stark":
        res["lead_weight"] = 200
        res["lead_system"] = "Festblei / Inliner (Grippa)"
        
    return res

setup = get_pro_setup()

# ==========================================
# 4. PHASE: OUTPUT
# ==========================================
st.divider()
st.header("📋 Taktisches Einsatz-Protokoll")

col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.subheader("📦 Hardware")
    st.metric("Bleigewicht", f"{setup['lead_weight']} g")
    st.write(f"**Bleisystem:** {setup['lead_system']}")
    if taktik_typ == "Wurf" and wurfweite > 100:
        st.warning("⚠️ Helicopter-Montage für Wurfstabilität!")

with col_out2:
    st.subheader("🪝 Rig-Konfiguration")
    st.success(f"**Empfohlen:** {setup['rig_name']}")
    st.write(f"**Material:** {setup['material']}")
    # Haken-Range statt Einzelwert
    st.info(f"**Haken-Range:** Größe {setup['hook_range']}")
    st.write(f"**Vorfachlänge:** {setup['length']} cm")

with col_out3:
    st.subheader("🍬 Präsentation")
    st.write(f"**Optik:** {setup['bait_style']}")
    if ph_algen == "Sauerstoffarm (Hitze)":
        st.error("Gefahr: Fische fressen kaum. Nutze hochattraktive Einzeltäter-Köder!")

# Dynamischer Bauer-Tipp
st.info(f"**Profi-Tipp:** Wähle die Hakengröße innerhalb der Range {setup['hook_range']} passend zur Ködergröße. "
        f"Bei einem 20mm Boilie eher zur Gr. 4, bei einem 24mm oder doppelten Köder zur Gr. 2 greifen.")
