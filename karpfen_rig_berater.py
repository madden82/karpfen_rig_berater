import streamlit as st

# =========================
# Setup & Theme
# =========================
st.set_page_config(page_title="Carp Tactical Intelligence", layout="wide")

st.title("🎖️ Carp Tactical Intelligence Pro")
st.caption("Einsatzplanung v3.0 | Erweiterte Rig-Matrix & Dual-Material Engine")

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
    st.markdown("**Atmosphäre & Wasserqualität**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Medium", "Klar", "Gin-Clear"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leichte Brise", "Mäßiger Wind", "Starker Wind"])
    temp = st.slider("Wassertemperatur (°C)", 2, 30, 15)

# ==========================================
# 2. PHASE: TAKTIK & AUSBRINGUNG
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
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    koeder_typ = st.selectbox("Geplanter Köder", ["Bodenköder / Boilie", "Wafter (ausbalanciert)", "Pop-Up (schwimmend)", "Zigs (Schaumstoff)"])

# ==========================================
# 3. PHASE: DIE ERWEITERTE RIG-ENGINE
# ==========================================

def get_advanced_setup():
    # Standard-Werte
    setup = {
        "rig": "Hair Rig",
        "hook_range": "4 - 6",
        "lead_w": 95,
        "lead_sys": "Safety Clip",
        "optimum": "Coated Braid (25lb)",
        "braid_alt": "Soft Braid (20lb) + Anti Tangle Sleeve",
        "length": 18,
        "desc": "Klassische Allround-Präsentation."
    }

    # --- SPEZIAL-LOGIK: ZIG RIG ---
    if koeder_typ == "Zigs (Schaumstoff)":
        setup["rig"] = "Zig Rig"
        setup["optimum"] = "Monofilament (0.28mm - 0.30mm)"
        setup["braid_alt"] = "Nicht empfohlen für Zigs!"
        setup["length"] = int(tiefe * 0.75 * 100) # 75% der Wassertiefe
        setup["lead_sys"] = "Blei-Freigabe-System (Adjustable)"
        setup["desc"] = "Präsentation im Mittelwasser. Ideal bei Hitze oder extremem Wind."
        return setup

    # --- SPEZIAL-LOGIK: POP-UPS ---
    if koeder_typ == "Pop-Up (schwimmend)":
        if boden_struktur in ["Kies/Sand (hart)", "Lehm (fest)"]:
            setup["rig"] = "Ronnie Rig"
            setup["optimum"] = "Stiff Mono / Boom (0.50mm)"
            setup["braid_alt"] = "Stiff Coated Braid (35lb)"
            setup["desc"] = "Aggressives Pop-Up Rig für sauberen Boden."
        elif boden_struktur in ["Schlamm (weich)", "Kraut/Algen"]:
            setup["rig"] = "Chod Rig"
            setup["optimum"] = "Rigid Mouthtrap (0.50mm)"
            setup["braid_alt"] = "Short Stiff Coated Braid"
            setup["length"] = 6
            setup["lead_sys"] = "Helicopter (Naked)"
            setup["desc"] = "Die beste Wahl über Kraut und Schlamm."
        else: # Modder
            setup["rig"] = "Stiff Hinged Rig"
            setup["optimum"] = "D-Rig Fluorocarbon + Boom"
            setup["braid_alt"] = "Combi-Link (Fluoro + Braid)"
            setup["desc"] = "Großfisch-Rig für Pop-Ups auf unsicherem Grund."

    # --- SPEZIAL-LOGIK: WAFTER ---
    elif koeder_typ == "Wafter (ausbalanciert)":
        if wasser_klarheit in ["Klar", "Gin-Clear"]:
            setup["rig"] = "Slip-D Rig"
            setup["optimum"] = "Fluorocarbon (0.40mm)"
            setup["braid_alt"] = "Skinny Coated Braid (15lb)"
            setup["desc"] = "Maximale Tarnung für argwöhnische Fische."
        else:
            setup["rig"] = "German Rig"
            setup["optimum"] = "Semi-Stiff Fluorocarbon"
            setup["braid_alt"] = "Coated Braid (ummantelt lassen)"
            setup["desc"] = "Saubere Bodenpräsentation mit exzellenter Hakeigenschaft."

    # --- SPEZIAL-LOGIK: BODENKÖDER & FLUSS ---
    else:
        if stromung != "Keiner":
            setup["rig"] = "Combi-Rig (Stiff Section)"
            setup["optimum"] = "Hard Mono + Soft Braid Spitze"
            setup["braid_alt"] = "Heavy Coated Braid (stripped 2cm)"
            setup["length"] = 12
            setup["desc"] = "Verhedderungsfrei in der Strömung."
        elif len(hindernisse) > 0:
            setup["rig"] = "Snag-Blowback-Rig"
            setup["optimum"] = "Snag Leader Material (35lb)"
            setup["braid_alt"] = "Kevlar-Braid (Abriebfest)"
            setup["desc"] = "Extrem robust für harte Bedingungen."

    # --- FEINTUNING BLEI & HAKEN ---
    if taktik_typ == "Wurf":
        setup["lead_w"] = 115 if wurfweite > 90 else 85
        if wurfweite > 115: setup["lead_sys"] = "Helicopter"
    if stromung == "Stark":
        setup["lead_w"] = 220; setup["lead_sys"] = "Grippa-Inliner"

    if ziel_gewicht > 20: setup["hook_range"] = "2 - 4"
    elif temp < 10: setup["hook_range"] = "6 - 8"

    return setup

res = get_pro_setup()

# ==========================================
# 4. PHASE: DAS OUTPUT-TERMINAL
# ==========================================
st.divider()
st.header("🏁 Dein Taktisches Setup")

c_out1, c_out2, c_out3 = st.columns(3)

with c_out1:
    st.subheader("📦 Hardware")
    st.metric("Blei", f"{res['lead_w']} g")
    st.write(f"**Montage:** {res['lead_sys']}")
    st.write(f"**Haken-Range:** Gr. {res['hook_range']}")
    if windstärke == "Starker Wind":
        st.warning("Schnur absenken (Backleads)!")

with c_out2:
    st.subheader("🪝 Rig & Material")
    st.success(f"**Architektur:** {res['rig']}")
    st.write(f"**Optimum:** {res['optimum']}")
    st.info(f"**Alternative:** {res['braid_alt']}")
    st.write(f"**Vorfachlänge:** {res['length']} cm")

with c_out3:
    st.subheader("🧠 Experten-Analyse")
    st.write(f"**Warum dieses Rig?** {res['desc']}")
    if temp < 10:
        st.error("Kaltwasser-Tipp: Kleine Köder, extrem feine Präsentation!")
    if "Kraut" in boden_struktur:
        st.write("🌿 Kraut-Taktik: Blei beim Biss abwerfen (Drop-Off) empfohlen.")

# Dynamische Bauanleitung
with st.expander("🛠️ Schritt-für-Schritt Bauanleitung"):
    st.write(f"1. **Basis:** Vorbereitung von {res['length'] + 5}cm {res['optimum']} (bzw. Alternative).")
    st.write(f"2. **Mechanik:** Binde einen Haken der Größe {res['hook_range']} mit dem {'Knotless-Knot' if 'Zig' not in res['rig'] else 'Palomar-Knoten am Wirbel'}.")
    if "Ronnie" in res['rig']:
        st.write("3. **Special:** Befestige den Haken an einem Spinner-Wirbel und sichere ihn mit Schrumpfschlauch.")
    elif "Combi" in res['rig']:
        st.write("3. **Special:** Verbinde den steifen Teil mit dem weichen Teil via Albright-Knoten oder kleiner Schlaufe.")
    st.write(f"4. **Finish:** Montage am {res['lead_sys']}-System mit {res['lead_w']}g Blei.")
