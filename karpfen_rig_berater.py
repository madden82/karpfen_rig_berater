import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Carp Rig Master Pro", layout="wide", page_icon="🎣")

st.title("🎣 Carp Rig Master Pro")
st.markdown("---")

# =========================
# Datenbank: Die 12 wichtigsten Rig-Architekturen
# =========================
# types: 1=Boden, 2=Wafter, 3=PopUp | speed: 1=langsam/träge, 2=allround, 3=aggressiv
RIGS = [
    {"name": "Ronnie Rig", "types": [3], "cast": 140, "weed": True, "stiff": True, "desc": "Das ultimative Pop-Up Rig für aggressive Hakeigenschaften."},
    {"name": "Chod Rig", "types": [3], "cast": 120, "weed": True, "stiff": True, "desc": "Präsentiert den Köder sicher über Kraut oder tiefem Schlamm."},
    {"name": "Hinged Stiff Rig", "types": [3], "cast": 140, "weed": True, "stiff": True, "desc": "Großfisch-Rig für Pop-Ups, sehr schwer auszuspucken."},
    {"name": "Blowback Rig", "types": [1, 2], "cast": 160, "weed": False, "stiff": False, "desc": "Klassische Ring-Präsentation für maximale Köderbeweglichkeit."},
    {"name": "German Rig", "types": [1, 2], "cast": 130, "weed": False, "stiff": True, "desc": "Sehr sauber am Boden liegend, perfekt für Wafter."},
    {"name": "KD Rig", "types": [1, 2], "cast": 150, "weed": False, "stiff": False, "desc": "Phänomenaler Kipp-Effekt des Hakens durch den austretenden Haarpunkt."},
    {"name": "Slip D Rig", "types": [2, 3], "cast": 140, "weed": True, "stiff": False, "desc": "Sehr feine Präsentation, ideal für scheue Fische am Rand des Krauts."},
    {"name": "Multi Rig", "types": [3], "cast": 150, "weed": True, "stiff": True, "desc": "Ermöglicht extrem schnellen Hakenwechsel ohne neues Binden."},
    {"name": "D-Rig (Fluoro)", "types": [1, 2], "cast": 150, "weed": False, "stiff": True, "desc": "Steife Präsentation, fast unsichtbar, ideal für klaren Kies."},
    {"name": "Combi Rig", "types": [1, 2], "cast": 140, "weed": True, "stiff": False, "desc": "Vereint Steifheit (Anti-Tangle) mit extremer Beweglichkeit am Haken."},
    {"name": "Zig Rig", "types": [3], "cast": 150, "weed": False, "stiff": False, "desc": "Spezial-Rig für Fische im Mittelwasser oder an der Oberfläche."},
    {"name": "Simple Hair Rig", "types": [1], "cast": 180, "weed": False, "stiff": False, "desc": "Der bewährte Standard für weite Würfe und Bodenköder."}
]

# =========================
# Eingabemasken (Säulen-Layout)
# =========================
with st.sidebar:
    st.header("📋 Szenario-Parameter")
    distanz = st.slider("Entfernung (m)", 0, 200, 70)
    methode = st.selectbox("Ausbringung", ["Wurf", "Futterboot", "Ablegen (Boot)"])
    
    st.subheader("🌊 Gewässer")
    boden = st.selectbox("Untergrund", ["Kies/Sand (Hart)", "Schlamm (Weich)", "Kraut (Dicht)", "Fadenalgen (Leicht)"])
    hindernisse = st.multiselect("Hindernisse", ["Muscheln", "Totholz", "Steine", "Keine"])
    
    st.subheader("🐟 Zielfisch & Biologie")
    aktivitat = st.select_slider("Fisch-Aktivität", ["Träge (Winter)", "Vorsichtig", "Normal", "Aggressiv (Sommer)"])
    gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)
    
# =========================
# Experten-Logik
# =========================

# 1. Köder-Logik
def determine_bait():
    if boden == "Kraut (Dicht)": return "Pop-Up (Fluo)", 3, "Muss über das Kraut gehoben werden."
    if boden == "Schlamm (Weich)": return "Wafter (Schwerelos)", 2, "Sinkt nicht in den Schlamm ein."
    if aktivitat == "Vorsichtig": return "Kleiner Wafter / Balanced", 2, "Minimaler Widerstand beim Einsaugen."
    if aktivitat == "Träge (Winter)": return "Einzelner kleiner Pop-Up", 3, "Hoher visueller Reiz bei wenig Hunger."
    return "Standard Boilie / Snowman", 1, "Bewährte Präsentation für aktive Fische."

bait_name, bait_type, bait_reason = determine_bait()

# 2. Rig-Scoring
def get_best_rigs():
    scored = []
    for r in RIGS:
        score = 0
        if methode == "Wurf" and distanz > r["cast"]: continue
        if boden == "Kraut (Dicht)" and not r["weed"]: continue
        
        # Match Typ
        if bait_type in r["types"]: score += 60
        
        # Match Bodenhärte
        if boden == "Kies/Sand (Hart)" and r["stiff"]: score += 20
        if boden == "Schlamm (Weich)" and not r["stiff"]: score += 15
        
        # Match Aktivität
        if aktivitat == "Vorsichtig" and "Slip D" in r["name"]: score += 20
        if aktivitat == "Aggressiv (Sommer)" and r["name"] == "Ronnie Rig": score += 20
        
        scored.append((score, r))
    return sorted(scored, key=lambda x: x[0], reverse=True)

# 3. Material-Tuning (Die "Feinheiten")
def get_fine_tuning(rig_name):
    # Standardwerte
    hook_size = 4
    material = "Coated Braid (25lb)"
    length = "15-20 cm"
    lead_system = "Safety Clip"
    
    # Situative Anpassung
    if gewicht > 20 or "Muscheln" in hindernisse or "Totholz" in hindernisse:
        hook_size = 2
        material = "Stiff Mono / Snag Leader"
        
    if aktivitat == "Träge (Winter)":
        hook_size = 6
        length = "10-12 cm (Kurze Wege)"
        material = "Soft Braid (geschmeidig)"
        
    if "Chod Rig" in rig_name:
        length = "5-8 cm"
        lead_system = "Helicopter (Naked Chod)"
        material = "Rigid Mouthtrap (Mono)"
        
    if distanz > 100 and "Chod" not in rig_name:
        lead_system = "Helicopter (Anti-Tangle)"
        
    if boden == "Schlamm (Weich)" and "Chod" not in rig_name:
        length = "25-30 cm (Verhindert Einsinken)"
        
    return hook_size, material, length, lead_system

# =========================
# UI Ausgabe
# =========================
st.header("🎯 Dein Profi-Setup")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💡 Köder-Strategie")
    st.info(f"**Empfehlung:** {bait_name}")
    st.caption(f"Grund: {bait_reason}")

top_results = get_best_rigs()
if top_results:
    best_rig = top_results[0][1]
    h_size, m_type, r_len, l_sys = get_fine_tuning(best_rig["name"])
    
    with col2:
        st.subheader("🏗️ Rig-Architektur")
        st.success(f"**Primär-Rig:** {best_rig['name']}")
        st.write(best_rig["desc"])
        
    with col3:
        st.subheader("🛠️ Material-Feintuning")
        st.markdown(f"""
        - **Hakengröße:** {h_size}
        - **Vorfachmaterial:** {m_type}
        - **Vorfachlänge:** {r_len}
        - **Bleisystem:** {l_sys}
        """)

st.markdown("---")
st.subheader("📋 Alternative Rigs für dieses Szenario")
cols = st.columns(len(top_results[1:4]))
for i, (score, r) in enumerate(top_results[1:4]):
    with cols[i]:
        st.metric(label=f"Platz {i+2}", value=r["name"])
        st.caption(r["desc"])

st.markdown("---")
# Profi-Checkliste
with st.expander("✅ Profi-Checkliste vor dem Auswerfen"):
    st.write("""
    1. **Schärfe-Test:** Haken über den Fingernagel ziehen. Er muss hängen bleiben!
    2. **Köder-Check:** Prüfe im Uferwasser, ob das Rig genau so steht, wie du es willst.
    3. **Anti-Tangle:** Nutze PVA-Nuggets oder Anti-Tangle-Sleeves bei weiten Würfen.
    4. **Sicherheit:** Läuft das Blei im Falle eines Schnurbruchs frei vom Leader ab?
    """)
