import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Carp Tactical Commander Pro", layout="wide")

st.title("🎖️ Carp Tactical Commander Pro")
st.caption("Präzisions-Einsatzplanung für Profi-Karpfenangler")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL (Was finde ich vor?)
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See (natürlich)", "Baggersee", "Kanal", "Fluss", "Strom (starke Strömung)", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Spot (m)", 0.5, 40.0, 4.0)
    stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand/Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Modder (faulig/stinkend)", "Kraut/Algen"])
    hindernisse = st.multiselect("Hindernisse am Spot", ["Muschelbänke", "Totholz/Äste", "Scharfe Kanten", "Versunkene Bauten"])

with c3:
    st.markdown("**Wasserqualität & Sicht**")
    wasser_klarheit = st.select_slider("Sichttiefe", options=["Trüb (0-30cm)", "Medium (1m)", "Klar (3m+)", "Gin-Clear"])
    ph_algen = st.selectbox("Zustand/Algen", ["Normal", "Starke Algenblüte", "Hoher Sauerstoff (Wind/Zufluss)", "Sauerstoffarm (Hitze)"])

# ==========================================
# 2. PHASE: TAKTIK & AUSBRINGUNG (Wie fische ich?)
# ==========================================
st.header("🎯 Schritt 2: Taktik & Ausbringung")
t1, t2 = st.columns(2)

with t1:
    ausbringungs_methode = st.radio("Wie bringst du den Köder aus?", 
                                   ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    # Dynamische Unter-Logik für Boot
    wurfweite = 0
    taktik_typ = "Ablegen"
    
    if ausbringungs_methode == "Boot":
        boot_taktik = st.radio("Taktik vom Boot:", ["Vom Boot auslegen", "Vom Boot werfen"], horizontal=True)
        if boot_taktik == "Vom Boot werfen":
            taktik_typ = "Wurf"
            wurfweite = st.slider("Benötigte Wurfweite (m)", 5, 100, 30)
    elif ausbringungs_methode == "Wurf vom Ufer":
        taktik_typ = "Wurf"
        wurfweite = st.slider("Benötigte Wurfweite (m)", 10, 180, 70)
    else: # Futterboot
        taktik_typ = "Ablegen"

with t2:
    jahreszeit = st.selectbox("Saison", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    fisch_aktivitaet = st.select_slider("Aktivität der Fische", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-BERECHNUNG (Die Engine)
# ==========================================

def get_pro_setup():
    # Basis-Werte initialisieren
    res = {
        "rig_name": "Standard Hair Rig",
        "material": "Coated Braid (25lb)",
        "hook_size": 4,
        "lead_weight": 100,
        "lead_system": "Safety Clip",
        "bait_color": "Match the Hatch (Natur)",
        "length": 18
    }

    # A. Rig-Logik nach Boden & Wasserqualität
    if boden_struktur == "Kraut/Algen" or boden_struktur == "Modder (faulig/stinkend)":
        res["rig_name"] = "Chod Rig" if taktik_typ == "Wurf" else "Ronnie Rig (Heli)"
        res["bait_color"] = "Fluoro Pink/White" # Visueller Reiz über Dreck/Kraut
    elif wasser_klarheit == "Gin-Clear":
        res["rig_name"] = "D-Rig (Fluorocarbon)"
        res["material"] = "Fluorocarbon (0.40mm - unsichtbar)"
    
    # B. Material-Anpassung nach Hindernis
    if len(hindernisse) > 0 or ziel_gewicht > 20:
        res["hook_size"] = 2
        res["material"] = "Heavy Coated Braid (35lb) oder Snag-Material"
    
    # C. Längen-Logik (Physik)
    if boden_struktur == "Schlamm (weich)": res["length"] = 25
    if stromung in ["Mittel", "Stark"]: res["length"] = 12 # Kurz halten gegen Verheddern
    
    # D. Blei-Logik (Hydrodynamik)
    if taktik_typ == "Wurf":
        res["lead_weight"] = 115 if wurfweite > 80 else 90
        if wurfweite > 120: res["lead_system"] = "Helicopter System (Anti-Tangle)"
    if stromung == "Stark":
        res["lead_weight"] = 220
        res["lead_system"] = "Festblei / Inliner (Grippa-Form)"
        
    return res

setup = get_pro_setup()

# ==========================================
# 4. PHASE: DAS TAKTISCHE PROTOKOLL (Output)
# ==========================================
st.divider()
st.header("📋 Taktisches Einsatz-Protokoll")

col_out1, col_out2, col_out3 = st.columns(3)

with col_out1:
    st.subheader("🛠️ Montage & Hardware")
    st.metric("Empfohlenes Blei", f"{setup['lead_weight']} g")
    st.write(f"**Bleisystem:** {setup['lead_system']}")
    st.write(f"**Blei-Form:** {'Grippa' if stromung != 'Keiner' else 'Long Distance' if taktik_typ == 'Wurf' else 'Flat Pear'}")
    st.write(f"**Schlagschnur:** {'ERFORDERLICH (0.55mm)' if len(hindernisse) > 0 else 'Nicht zwingend'}")

with col_out2:
    st.subheader("🪝 Rig-Konfiguration")
    st.success(f"**Rig-Typ:** {setup['rig_name']}")
    st.write(f"**Vorfachmaterial:** {setup['material']}")
    st.write(f"**Länge:** {setup['length']} cm")
    st.write(f"**Hakengröße:** {setup['hook_size']} (stabile Ausführung)")

with col_out3:
    st.subheader("🍬 Köder-Präsentation")
    st.info(f"**Farbschema:** {setup['bait_color']}")
    if ph_algen == "Sauerstoffarm (Hitze)":
        st.warning("Tipp: Köder extrem stark flaven / auswaschen (Washed Out)")
    elif ph_algen == "Starke Algenblüte":
        st.warning("Tipp: Pop-Up hoch präsentieren (Algenteppich-Gefahr)")
    st.write(f"**Mechanik:** {'Aggressiv (Kurz)' if setup['length'] < 15 else 'Natürlich (Lang)'}")

# Dynamische Bauanleitung basierend auf dem Ergebnis
with st.expander("🛠️ Schritt-für-Schritt Bauanleitung"):
    st.write(f"1. Vorbereitung von {setup['length']}cm {setup['material']}.")
    st.write(f"2. Binden des {setup['rig_name']} mit einem Gr. {setup['hook_size']} Haken.")
    if setup['lead_system'] == "Helicopter System (Anti-Tangle)":
        st.write("3. **Spezial:** Perlen auf dem Leader so einstellen, dass das Rig beim Wurf nicht gegen das Blei schlägt.")
    st.write(f"4. Köder in {setup['bait_color']} montieren und mit {setup['lead_weight']}g Blei sichern.")
