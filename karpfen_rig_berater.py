import streamlit as st

# =========================
# Setup
# =========================
st.set_page_config(page_title="Carp Tactical Commander Pro", layout="wide")

st.title("🎖️ Carp Tactical Commander Pro")
st.caption("Präzisions-Einsatzplanung | Version 2.3 (Dual Material Logic)")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Spot (m)", 0.5, 40.0, 4.0)
    
    stromung = "Keiner"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand/Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Modder (faulig)", "Kraut/Algen"])
    hindernisse = st.multiselect("Hindernisse am Spot", ["Muschelbänke", "Totholz/Äste", "Scharfe Kanten"])

with c3:
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Medium", "Klar", "Gin-Clear"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leichte Brise", "Mäßiger Wind", "Starker Wind"])

# ==========================================
# 2. PHASE: TAKTIK
# ==========================================
st.header("🎯 Schritt 2: Taktik & Ausbringung")
t1, t2 = st.columns(2)

with t1:
    ausbringungs_methode = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    taktik_typ = "Ablegen"
    wurfweite = 0
    
    if ausbringungs_methode == "Boot":
        boot_taktik = st.radio("Taktik vom Boot:", ["Vom Boot ablegen", "Vom Boot werfen"], horizontal=True)
        if boot_taktik == "Vom Boot werfen":
            taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 5, 100, 30)
    elif ausbringungs_methode == "Wurf vom Ufer":
        taktik_typ = "Wurf"; wurfweite = st.slider("Wurfweite (m)", 10, 180, 70)

with t2:
    ziel_gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität", options=["Vorsichtig", "Normal", "Aggressiv"])

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE (Dual Logic)
# ==========================================

def get_pro_setup():
    # Basis-Setup
    setup = {
        "rig_name": "Standard Hair Rig",
        "hook_range": "4 - 6",
        "lead_weight": 90,
        "length": 18,
        "optimum": "Fluorocarbon (0.40mm) für Unsichtbarkeit",
        "braid_alt": "Coated Braid (25lb) - Ummantelung fast komplett dran lassen",
        "tuning": "Kein spezielles Tuning nötig"
    }

    # Sichtbarkeit & Strömung steuern Material
    if wasser_klarheit in ["Klar", "Gin-Clear"]:
        setup["optimum"] = "Fluorocarbon (0.45mm) - Steifigkeit verhindert Ausspucken"
        setup["braid_alt"] = "Dark Coated Braid (20lb) - Farbe dem Boden anpassen"
        setup["rig_name"] = "D-Rig / Slip-D"
    
    if stromung in ["Mittel", "Stark"]:
        setup["lead_weight"] = 180 if stromung == "Mittel" else 240
        setup["length"] = 12
        setup["optimum"] = "Dicke Mono / Hard-Mono (0.50mm)"
        setup["braid_alt"] = "Heavy Coated Braid (35lb) - Ummantelung NICHT entfernen"
    
    if boden_struktur in ["Kraut/Algen", "Modder (faulig)"]:
        setup["rig_name"] = "Ronnie Rig (Heli-System)"
        setup["optimum"] = "Stiff-Rig Filament (Mouthtrap)"
        setup["braid_alt"] = "Stiff Coated Braid (letzte 2cm abmanteln)"

    # Haken-Anpassung
    if ziel_gewicht > 20 or len(hindernisse) > 0:
        setup["hook_range"] = "2 - 4 (Strong Shank)"
    
    return setup

res = get_pro_setup()

# ==========================================
# 4. PHASE: OUTPUT (Duale Material-Anzeige)
# ==========================================
st.divider()
st.header("📋 Taktisches Einsatz-Protokoll")

c_out1, c_out2, c_out3 = st.columns(3)

with c_out1:
    st.subheader("📦 Hardware")
    st.metric("Blei", f"{res['lead_weight']} g")
    st.write(f"**Haken-Range:** Gr. {res['hook_range']}")
    if taktik_typ == "Wurf" and wurfweite > 100:
        st.warning("⚠️ Nutze Helicopter-System!")

with c_out2:
    st.subheader("🪝 Vorfach-Material (Deine Wahl)")
    st.success(f"**Top Empfehlung:**\n{res['optimum']}")
    st.info(f"**Geflecht-Alternative:**\n{res['braid_alt']}")
    st.write(f"**Länge:** {res['length']} cm")

with c_out3:
    st.subheader("🛠️ Rig-Setup")
    st.write(f"**Typ:** {res['rig_name']}")
    if "Modder" in boden_struktur:
        st.warning("Tipp: Nutze Pop-Up oder Wafter!")
    if windstärke == "Starker Wind":
        st.write("⚓ **Wind-Taktik:** Backleads verwenden!")

# Detail-Anleitung
with st.expander("📝 Bauanleitung für beide Materialien"):
    st.write(f"**1. Vorbereitung:** Schneide ca. 30cm von deinem gewählten Material ab (Ziel: {res['length']}cm Endlänge).")
    st.write(f"**2. Mechanik:** Binde einen Haken der Größe {res['hook_range']} mit dem Knotless-Knot.")
    st.write(f"**3. Besonderheit (Geflecht):** Wenn du Coated Braid nutzt, {'entferne die Ummantelung nur am Haar' if res['length'] < 15 else 'entferne die Ummantelung auf den letzten 2cm vor dem Haken'}.")
    st.write(f"**4. Besonderheit (Mono/Fluoro):** Nutze einen Schrumpfschlauch oder einen Kicker, um den Haken aggressiver nach unten klappen zu lassen.")
