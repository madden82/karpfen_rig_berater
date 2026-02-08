import streamlit as st
import datetime

# Setup
st.set_page_config(page_title="Karpfen-Taktik Pro v3.0", layout="wide")

# Custom CSS für bessere Optik
st.markdown("""
<style>
.result-box { background-color: #f8f9fa; border-left: 5px solid #2e7d32; padding: 15px; margin: 10px 0; border-radius: 5px; }
.reason-text { font-size: 0.9rem; color: #555; font-style: italic; }
.header-style { color: #1b5e20; font-weight: bold; border-bottom: 2px solid #2e7d32; }
</style>
""", unsafe_allow_html=True)

st.title("🎣 Karpfen-Taktik Pro v3.0")

# ============================
# EINGABESEKTIERUNG
# ============================
with st.sidebar:
    st.header("📍 Spot-Parameter")
    gewaesser = st.selectbox("Gewässer", ["See", "Fluss/Kanal", "Strom"])
    tiefe = st.number_input("Tiefe (m)", 0.5, 30.0, 4.0)
    boden = st.selectbox("Bodenbeschaffenheit", ["Sand/Kies", "Lehm", "Weicher Schlamm", "Faulschlamm/Moder"])
    hindernisse = st.multiselect("Hindernisse", ["Muscheln", "Totholz", "Kraut", "Krebse"])
    
    st.header("🌤️ Umwelt & Biologie")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    angeldruck = st.select_slider("Angeldruck", ["Gering", "Mittel", "Hoch", "Extrem"])
    fischgroesse = st.number_input("Zielfisch-Gewicht (kg)", 1, 50, 15)
    weissfisch = st.select_slider("Weißfisch-Dichte", ["Niedrig", "Mittel", "Hoch"])

# ============================
# LOGIK-ENGINE (Deep Linking)
# ============================
def generiere_taktik():
    # Initialisierung des Taktik-Objekts
    taktik = {
        "haken": {"typ": "Wide Gape", "gr": 6, "grund": ""},
        "vorfach": {"mat": "Coated Braid", "len": 20, "grund": ""},
        "blei": {"gewicht": 100, "typ": "Safety Clip", "form": "Birne", "grund": ""},
        "koeder": {"art": "Boilie", "gr": 20, "grund": ""}
    }

    # --- 1. HAKEN-LOGIK (Verknüpfung: Ködergröße + Angeldruck + Hindernisse) ---
    # Grundgröße basierend auf Fischgewicht
    h_gr = 6
    if fischgroesse > 20: h_gr = 4
    if fischgroesse < 10: h_gr = 8
    
    # Korrektur durch Angeldruck (Vorsichtige Fische = kleinere Haken)
    if angeldruck in ["Hoch", "Extrem"]:
        h_gr += 2 
    
    # Korrektur durch Hindernisse (Starker Halt nötig = größerer Haken)
    if any(x in hindernisse for x in ["Totholz", "Muscheln"]):
        h_gr = max(2, h_gr - 2)
        taktik["haken"]["typ"] = "Curve Shank (stärkerer Halt)"
    
    taktik["haken"]["gr"] = min(10, max(2, h_gr))
    taktik["haken"]["grund"] = f"Größe {taktik['haken']['gr']} gewählt, da bei {angeldruck}em Angeldruck und {fischgroesse}kg Fischen die Balance zwischen Tarnung und Hakeffekt stimmen muss."

    # --- 2. VORFACH-LOGIK (Verknüpfung: Boden + Hindernisse + Temperatur) ---
    if boden == "Weicher Schlamm":
        taktik["vorfach"]["len"] = 30
        taktik["vorfach"]["mat"] = "Soft Braid"
        taktik["vorfach"]["grund"] = "Langes, weiches Vorfach, damit der Köder nicht im Schlamm versinkt, wenn das Blei einsinkt."
    elif boden == "Faulschlamm/Moder":
        taktik["vorfach"]["len"] = 15
        taktik["vorfach"]["mat"] = "Chod Rig / Mono"
        taktik["vorfach"]["grund"] = "Pop-Up Montage (Chod), um den Köder über dem stinkenden Moder zu präsentieren."
    elif any(x in hindernisse for x in ["Muscheln", "Totholz"]):
        taktik["vorfach"]["mat"] = "Mantel-Vorfach (steil) oder Fluorocarbon"
        taktik["vorfach"]["grund"] = "Abriebfestes Material zwingend erforderlich wegen {', '.join(hindernisse)}."
    else:
        taktik["vorfach"]["grund"] = "Standard Coated Braid für saubere Präsentation auf hartem Boden."

    # --- 3. BLEI-LOGIK (Verknüpfung: Gewässer + Tiefe + Boden) ---
    gewicht = 100
    if gewaesser == "Strom":
        taktik["blei"]["form"] = "Grippa"
        gewicht = 180
    elif tiefe > 10:
        gewicht += 30
        taktik["blei"]["grund"] = "Erhöhtes Gewicht für bessere Köderkontrolle und Selbsthakeffekt in großer Tiefe."
    
    if boden in ["Weicher Schlamm", "Faulschlamm/Moder"]:
        taktik["blei"]["typ"] = "Helikopter-System"
        taktik["blei"]["grund"] += " Helikopter-Montage verhindert, dass das Vorfach mit dem Blei in den Boden gezogen wird."
    
    taktik["blei"]["gewicht"] = gewicht

    # --- 4. KÖDER-LOGIK (Verknüpfung: Temperatur + Weißfisch + Krebse) ---
    if "Krebse" in hindernisse or weissfisch == "Hoch":
        taktik["koeder"]["art"] = "Duo-Hartholz oder gesalzene Boilies"
        taktik["koeder"]["gr"] = 24
        taktik["koeder"]["grund"] = "Großer, harter Köder notwendig, um Krebsattacken und Weißfisch-Aktivität zu überstehen."
    elif temp < 10:
        taktik["koeder"]["art"] = "Auffälliger Pop-Up oder Wafter"
        taktik["koeder"]["gr"] = 14
        taktik["koeder"]["grund"] = "Kleinerer, hochattraktiver Köder, da der Stoffwechsel der Fische bei 10°C reduziert ist."
    else:
        taktik["koeder"]["grund"] = "Standard-Boilie (20mm) für ausgewogenes Fressverhalten."

    return taktik

# ============================
# AUSGABE
# ============================
if st.button("TAKTIK-ANALYSE STARTEN"):
    res = generiere_taktik()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎣 Montage-Details")
        st.markdown(f"""
        <div class="result-box">
            <b>Haken:</b> {res['haken']['typ']} Gr. {res['haken']['gr']}<br>
            <span class="reason-text">{res['haken']['grund']}</span>
        </div>
        <div class="result-box">
            <b>Vorfach:</b> {res['vorfach']['mat']} ({res['vorfach']['len']} cm)<br>
            <span class="reason-text">{res['vorfach']['grund']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("⚙️ System & Köder")
        st.markdown(f"""
        <div class="result-box">
            <b>Blei:</b> {res['blei']['gewicht']}g {res['blei']['form']} ({res['blei']['typ']})<br>
            <span class="reason-text">{res['blei']['grund']}</span>
        </div>
        <div class="result-box">
            <b>Köder:</b> {res['koeder']['art']} ({res['koeder']['gr']} mm)<br>
            <span class="reason-text">{res['koeder']['grund']}</span>
        </div>
        """, unsafe_allow_html=True)
