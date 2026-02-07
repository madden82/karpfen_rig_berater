import streamlit as st

# ==========================================
# 1. SETUP & THEME
# ==========================================
st.set_page_config(page_title="Carp Tactical AI", layout="wide")

st.title("⚡ Carp Tactical AI: Dynamic Rig Builder")
st.caption("Präzisions-Anleitungen basierend auf Echtzeit-Spotdaten")

# ==========================================
# 2. INPUTS: DER SPOT-CHECK
# ==========================================
with st.sidebar:
    st.header("📍 Spot-Parameter")
    # Reihenfolge so, wie man am Spot ankommt:
    gewaesser = st.selectbox("Gewässer", ["See/Weiher", "Fluss (langsam)", "Strom (schnell)", "Baggersee (tief)"])
    grund = st.selectbox("Boden", ["Sand/Kies", "Leichter Schlamm", "Tiefer Modder", "Kraut", "Steine/Muscheln"])
    
    st.header("🎣 Taktik")
    distanz = st.slider("Distanz (m)", 10, 180, 70)
    methode = st.radio("Ausbringung", ["Wurf", "Boot/Futterboot"])
    
    st.header("🐟 Biologie")
    temp = st.slider("Wassertemperatur (°C)", 2, 30, 15)
    fisch_size = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)
    weissfisch = st.checkbox("Viel Weißfisch/Krebse?")

# ==========================================
# 3. DIE DYNAMISCHE LOGIK (Das Gehirn)
# ==========================================

def generate_dynamic_setup():
    # A. Dynamische Materialwahl
    material = "Coated Braid (20lb)"
    if grund == "Steine/Muscheln" or fisch_size > 20:
        material = "Armadillo / Snag-Leader Material (35lb+)"
    elif temp < 8:
        material = "Supersoft Braid (15lb) für maximale Beweglichkeit"
    
    # B. Dynamische Vorfachlänge
    laenge = 18
    if grund == "Tiefer Modder": laenge = 30
    if gewaesser == "Strom (schnell)": laenge = 12
    
    # C. Dynamische Hakengröße
    haken = 6
    if fisch_size > 15: haken = 4
    if fisch_size > 22 or gewaesser == "Strom (schnell)": haken = 2
    
    # D. Bleigewicht & Form
    blei_gewicht = 85
    if distanz > 100: blei_gewicht = 115
    if gewaesser == "Strom (schnell)": blei_gewicht = 180
    
    blei_form = "Flat Pear" if gewaesser != "See/Weiher" else "Distance"
    if grund == "Tiefer Modder": blei_form = "Leichtes Tri-Lobe"

    return {
        "mat": material,
        "len": laenge,
        "hook": haken,
        "lead_w": blei_gewicht,
        "lead_f": blei_form
    }

spec = generate_dynamic_setup()

# ==========================================
# 4. RIG-SELECTION (Logik-Matrix)
# ==========================================
def select_rig():
    if grund == "Kraut" or grund == "Tiefer Modder":
        return "Ronnie Rig (Heli-System)", [
            f"1. Schneide {spec['len']}cm {spec['mat']} zu.",
            "2. Befestige einen Quick-Change-Wirbel am Hakenöhr (Gr. {spec['hook']}).",
            "3. Ziehe einen Schrumpfschlauch über das Öhr, um den Winkel zu fixieren.",
            f"4. Montiere das Rig an einem Helicopter-System, damit es über dem {grund} arbeitet.",
            f"5. Nutze ein {spec['lead_w']}g {spec['lead_f']} Blei als Kontergewicht."
        ]
    elif weissfisch:
        return "D-Rig (Anti-Eject)", [
            f"1. Nutze {spec['len']}cm steifes Fluorocarbon.",
            f"2. Binde einen {spec['hook']}er Haken mit dem Knotless-Knot.",
            "3. Forme ein 'D' am Schenkel für maximale Köderfreiheit.",
            "4. Ideal gegen Weißfisch: Das Haar kann sich nicht verwickeln.",
            f"5. Blei: {spec['lead_w']}g an einem Safety Clip."
        ]
    else:
        return "Standard Hair-Rig (Optimiert)", [
            f"1. {spec['len']}cm {spec['mat']} vorbereiten.",
            f"2. Haken Gr. {spec['hook']} (Wide Gape) binden.",
            "3. Das Haar exakt so lang lassen, dass der Köder 1cm Spiel zum Bogen hat.",
            f"4. {spec['lead_w']}g Blei für maximalen Selbsthakeffekt.",
            "5. Nutze ein Anti-Tangle Sleeve, um Verhedderungen beim Wurf zu vermeiden."
        ]

rig_name, anleitung = select_rig()

# ==========================================
# 5. OUTPUT: DAS DASHBOARD
# ==========================================
col_main, col_side = st.columns([2, 1])

with col_main:
    st.header(f"🏆 Empfehlung: {rig_name}")
    st.subheader("🛠️ Schritt-für-Schritt Bauanleitung")
    for schritt in anleitung:
        st.write(schritt)
    
    st.info(f"**Taktischer Hinweis:** Bei {temp}°C Wassertemperatur und {grund}-Boden ist dies die effizienteste Mechanik.")

with col_side:
    st.header("📊 Spezifikationen")
    st.metric("Bleigewicht", f"{spec['lead_w']} g")
    st.metric("Hakengröße", f"Gr. {spec['hook']}")
    st.metric("Vorfachlänge", f"{spec['len']} cm")
    
    st.subheader("Komponenten")
    st.code(f"Material: {spec['mat']}\nForm: {spec['lead_f']}\nLeader: {'Schlagschnur nötig' if spec['hook'] == 2 else 'Leadcore'}")

# ==========================================
# 6. FEEDBACK-LOOP
# ==========================================
st.divider()
if st.button("Checkliste für den Auswurf drucken"):
    st.write("✅ Haken ist extrem scharf?")
    st.write("✅ Köder ist perfekt ausbalanciert?")
    st.write("✅ Bremse/Freilauf ist eingestellt?")
