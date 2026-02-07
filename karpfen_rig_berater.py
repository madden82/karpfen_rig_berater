import streamlit as st

# =========================
# Setup
# =========================
st.set_page_config(page_title="Carp Tactical Commander Pro", layout="wide")

st.title("🎖️ Carp Tactical Commander Pro")
st.caption("Präzisions-Einsatzplanung | Version 2.2 (Dynamic Environment Logic)")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL (Statisch & Dynamisch)
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Spot (m)", 0.5, 40.0, 4.0)
    
    # Strömung nur bei Fließgewässern einblenden
    stromung = "Keiner"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand/Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Modder (faulig)", "Kraut/Algen"])
    hindernisse = st.multiselect("Hindernisse am Spot", ["Muschelbänke", "Totholz/Äste", "Scharfe Kanten", "Versunkene Bauten"])

with c3:
    st.markdown("**Atmosphäre & Wasser**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Medium", "Klar", "Gin-Clear"])
    
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leichte Brise", "Mäßiger Wind", "Starker Wind / Sturm"])
    windrichtung = st.selectbox("Windrichtung (relativ zum Spot)", ["Auflandig (Wind ins Gesicht)", "Ablandig (Rückenwind)", "Seitenwind"])

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
        "hook_range": "4 - 6",
        "lead_weight": 90,
        "lead_system": "Safety Clip",
        "bait_style": "Standard (Unauffällig)",
        "length": 18,
        "taktik_hinweis": ""
    }

    # A. Wind- & Temperatur-Logik (Umwälzung)
    if windstärke in ["Mäßiger Wind", "Starker Wind / Sturm"]:
        if windrichtung == "Auflandig (Wind ins Gesicht)":
            res["taktik_hinweis"] = "Top-Bedingungen! Sauerstoff und Nahrung werden an dein Ufer gedrückt."
            res["bait_style"] = "Hohe Attraktivität (viele wasserlösliche Stoffe)"
        res["lead_weight"] += 30 # Mehr Gewicht gegen Schnurbogen durch Wind
        
    # B. Strömung & Wasserqualität
    if stromung in ["Mittel", "Stark"]:
        res["lead_weight"] = 180 if stromung == "Mittel" else 250
        res["length"] = 12 # Kurzes Vorfach gegen Verwicklungen im Strom
        res["material"] = "Fluorocarbon oder steifes Coated Braid"
        
    if wasser_klarheit in ["Klar", "Gin-Clear"]:
        res["material"] = "Fluorocarbon (0.40mm+)"
        res["rig_name"] = "D-Rig / Slip-D"

    # C. Boden & Rig
    if boden_struktur in ["Kraut", "Modder (faulig)"]:
        res["rig_name"] = "Ronnie-Rig oder Chod-Rig"
        res["length"] = 6 if "Chod" in res["rig_name"] else 20

    # D. Haken-Range
    if ziel_gewicht > 20 or len(hindernisse) > 0:
        res["hook_range"] = "2 - 4"
    elif fisch_aktivitaet == "Vorsichtig":
        res["hook_range"] = "6 - 8"

    return res

setup = get_pro_setup()

# ==========================================
# 4. PHASE: OUTPUT
# ==========================================
st.divider()
st.header("📋 Taktisches Einsatz-Protokoll")

col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.subheader("📦 Hardware & Montage")
    st.metric("Bleigewicht", f"{setup['lead_weight']} g")
    st.write(f"**Bleisystem:** {setup['lead_system']}")
    if windstärke == "Starker Wind / Sturm":
        st.warning("⚓ Starker Winddruck: Schnur gut absenken (Backleads)!")

with col_out2:
    st.subheader("🪝 Rig-Details")
    st.success(f"**Rig:** {setup['rig_name']}")
    st.write(f"**Haken-Range:** Größe {setup['hook_range']}")
    st.write(f"**Vorfach:** {setup['material']} ({setup['length']} cm)")

with col_out3:
    st.subheader("💡 Strategie-Hinweise")
    if setup["taktik_hinweis"]:
        st.info(setup["taktik_hinweis"])
    st.write(f"**Köder-Stil:** {setup['bait_style']}")
    if jahreszeit == "Frühjahr" and windrichtung == "Auflandig (Wind ins Gesicht)":
        st.write("🔥 *Bonus:* Der warme Wind im Frühjahr kann die Fische extrem schnell in dein Ufer locken.")

# Profi-Info
st.divider()
with st.expander("🛠️ Zusätzliche technische Details"):
    st.write(f"- **Vorfach-Steifigkeit:** {'Hoch (Stiff)' if stromung != 'Keiner' or wasser_klarheit == 'Gin-Clear' else 'Medium'}")
    st.write(f"- **Hakenform:** {'Curve Shank' if 'Ronnie' in setup['rig_name'] else 'Wide Gape'}")
    st.write(f"- **Sicherheit:** {'Inliner' if stromung == 'Stark' else 'Safety Clip'} ermöglicht sicheres Auslösen des Bleis.")
