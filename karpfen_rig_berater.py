import streamlit as st

# ==========================================
# PROFESSOR CARP - TACTICAL SETUP ENGINE
# ==========================================

st.set_page_config(page_title="Carp Tactical Engine v2.0", layout="wide")

# Datenbank mit technischen Spezifikationen (Auszug der Top-Architekturen)
RIG_TECH_DB = {
    "Ronnie Rig": {
        "base_material": "Stiff Fluorocarbon (0.45mm) oder Boom-Material",
        "hook_type": "Curved Shank (Gr. 4)",
        "mechanics": "360-Grad Rotation für maximale Hakeffizienz bei Pop-Ups",
        "optimal_height": "2-4cm über Grund",
        "suitability": {"low_temp": 1.0, "weed": 1.0, "current": 0.3}
    },
    "Hinged Stiff Rig": {
        "base_material": "Mouthtrap (25lb) / Chod Filament",
        "hook_type": "Chod Hook (Out-turned Eye)",
        "mechanics": "Zweiteiliges System für maximale Steifigkeit und Reset-Fähigkeit",
        "optimal_height": "5-8cm",
        "suitability": {"low_temp": 0.8, "weed": 0.9, "current": 0.2}
    },
    "Blowback Rig": {
        "base_material": "Coated Braid (20-30lb)",
        "hook_type": "Wide Gape oder Long Shank",
        "mechanics": "Verschiebbarer Ring am Schenkel verhindert das Ausspucken",
        "optimal_height": "Bündig am Grund",
        "suitability": {"low_temp": 0.6, "weed": 0.2, "current": 0.8}
    }
    # ... weitere Rigs folgen der Logik unten
}

# ==========================================
# 1. USER INTERFACE: DER SPOT-SCAN
# ==========================================
st.title("🎖️ Carp Tactical Intelligence")
st.write("Präzisions-Analyse basierend auf biologischen und physikalischen Daten.")

with st.expander("🌍 UMGEBUNG & HYDROLOGIE", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        jahreszeit = st.selectbox("Saison", ["Frühjahr (steigend)", "Sommer (Peak)", "Herbst (Fressphase)", "Winter (Lethargie)"])
        temp = st.slider("Wassertemperatur (°C)", 2, 30, 12)
    with c2:
        grund = st.selectbox("Bodenstruktur", ["Fels/Stein", "Kies/Sand", "Lehm/Ton", "Schlamm (fest)", "Modder (faulig)", "Kraut (leicht)", "Kraut (Dschungel)"])
        truebung = st.select_slider("Sichtweite", options=["0-20cm (Null)", "20-100cm (Trüb)", "1-3m (Klar)", ">3m (Gin-Clear)"])
    with c3:
        stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht (Kanal)", "Mittel (Fluss)", "Stark (Strom)"])
        hindernisse = st.multiselect("Gefahrenquellen", ["Muschelbänke", "Totholz", "Scharfe Kanten", "Krautwände"])
    with c4:
        tiefe = st.number_input("Tiefe (m)", 0.5, 25.0, 4.0)
        distanz = st.number_input("Distanz (m)", 5, 200, 80)

with st.expander("🐟 BIOLOGISCHE FAKTOREN"):
    b1, b2, b3 = st.columns(3)
    with b1:
        besatz = st.selectbox("Gewässertyp", ["Low Stock (Großfisch)", "Medium Stock", "High Stock (Paylake)"])
    with b2:
        aktivitat = st.select_slider("Fraßanzeichen", options=["Null", "Vereinzelt Blasen", "Springende Fische", "Fressrausch"])
    with b3:
        beissdruck = st.select_slider("Angeldruck", options=["Niedrig", "Mittel", "Extrem hoch"])

# ==========================================
# 2. EXPERTEN-LOGIK: DIE BERECHNUNG
# ==========================================

# A. Bleigewicht-Physik (Berechnung nach Distanz & Strömung)
def calculate_lead_physics():
    base = 85
    if distanz > 100: base = 115
    if distanz > 140: base = 135
    
    # Strömungs-Vektor hinzufügen
    flow_map = {"Keiner": 0, "Leicht (Kanal)": 20, "Mittel (Fluss)": 60, "Stark (Strom)": 110}
    final_weight = base + flow_map[stromung]
    
    # Form-Empfehlung
    shape = "Flat Pear" if stromung != "Keiner" else "Distance Casting"
    if grund == "Schlamm (fest)": shape = "Grippa oder Trilobe"
    
    return final_weight, shape

# B. Rig & Material-Spezifikation
def get_detailed_setup():
    setup = {}
    
    # 1. Köder-Präsentation (Zentrale Entscheidung)
    if "Kraut" in grund or grund == "Modder (faulig)":
        setup["rig"] = "Chod Rig" if distanz < 100 else "Ronnie Rig (am Heli-System)"
        setup["bait_type"] = "Pop-Up (high buoyancy)"
        setup["color"] = "Fluoro White/Pink" if truebung in ["0-20cm (Null)", "20-100cm (Trüb)"] else "Washed Out Pink"
    elif jahreszeit == "Winter (Lethargie)":
        setup["rig"] = "Slip D-Rig"
        setup["bait_type"] = "Kleine Wafter (12-14mm)"
        setup["color"] = "Gelb (optischer Reiz)"
    else:
        setup["rig"] = "Blowback Rig (Kombi-Vorfach)"
        setup["bait_type"] = "Snowman / Bodenköder"
        setup["color"] = "Matching (Boilie-Farbe)"

    # 2. Material-Spezifikationen (Die Profi-Details)
    if stromung in ["Mittel (Fluss)", "Stark (Strom)"]:
        setup["link_material"] = "Fluorocarbon 30lb (steif)"
        setup["link_length"] = "12-15cm (kurz gegen Verheddern)"
    elif grund == "Modder (faulig)":
        setup["link_material"] = "Uncoated Braid (weich/sinkend)"
        setup["link_length"] = "25-35cm (lang gegen Versinken)"
    else:
        setup["link_material"] = "Coated Braid (25lb) - letzte 2cm abgemantelt"
        setup["link_length"] = "18-22cm"

    # 3. Haken-Spezifikation
    if "Muschelbänke" in hindernisse or fisch_groesse := 20: # Simulierter Wert
        setup["hook"] = "Gr. 2 Wide Gape (Heavy Duty)"
    else:
        setup["hook"] = "Gr. 4-6 Curved Shank"
        
    return setup

# ==========================================
# 3. OUTPUT: DAS TACTICAL PROTOCOL
# ==========================================
st.divider()
final_setup = get_detailed_setup()
lead_w, lead_s = calculate_lead_physics()

st.header("📋 Taktisches Einsatzprotokoll")

col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.subheader("🏗️ Endtackle & Montage")
    st.metric("Bleigewicht", f"{lead_w} g", delta=f"Form: {lead_s}", delta_color="normal")
    st.write(f"**Leader:** {'Quicksilver Gold (35lb)' if len(hindernisse) > 0 else 'Leadcore / Leadfree 45lb'}")
    st.write(f"**Bleisystem:** {'Helicopter (Naked)' if 'Schlamm' in grund else 'Safety Clip (Heavy Duty)'}")

with col_res2:
    st.subheader("🪝 Rig-Spezifikation")
    st.success(f"**Typ:** {final_setup['rig']}")
    st.write(f"**Material:** {final_setup['link_material']}")
    st.write(f"**Länge:** {final_setup['link_length']}")
    st.write(f"**Haken:** {final_setup['hook']}")
    st.info(f"**Knoten:** {'D-Loop / Krimpen' if 'Fluoro' in final_setup['link_material'] else 'No-Knot + Shrink Tube'}")

with col_res3:
    st.subheader("🍱 Köder-Konfiguration")
    st.warning(f"**Präsentation:** {final_setup['bait_type']}")
    st.write(f"**Farbschema:** {final_setup['color']}")
    st.write(f"**Attraktion:** {'Alkohol-basiert (Flavor)' if temp < 8 else 'Öl-basiert (Lachs/Fisch)'}")

# Strategie-Text
st.divider()
st.subheader("🧠 Taktische Begründung")
st.write(f"""
Basierend auf der **{jahreszeit}** und dem Untergrund **({grund})** wurde ein Setup gewählt, das die **{final_setup['rig']}**-Mechanik nutzt. 
Da die Trübung bei **{truebung}** liegt, setzen wir auf **{final_setup['color']}**, um den Fisch visuell zum Spot zu führen. 
Das Bleigewicht von **{lead_w}g** stellt sicher, dass der Selbsthakeffekt auch bei **{stromung}** Strömung und einer Distanz von **{distanz}m** unmittelbar eintritt.
""")

if len(hindernisse) > 0:
    st.error(f"⚠️ **GEFAHRENHINWEIS:** Aufgrund von {', '.join(hindernisse)} ist 
