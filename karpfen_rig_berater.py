import streamlit as st
import datetime

# ============================
# 1. Setup & Design
# ============================
st.set_page_config(page_title="Karpfen-Hilfe v1.0", layout="wide")

st.markdown("""
<style>
.main-header {
    font-size: 2.2rem;
    color: #1b5e20;
    font-weight: bold;
    text-align: center;
}
.section-header {
    background-color: #2e7d32;
    color: white;
    padding: 10px;
    border-radius: 8px;
    margin-top: 20px;
    font-weight: bold;
}
.result-card {
    background-color: #f1f8e9;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #c8e6c9;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎣 Karpfen-Hilfe v1.0</div>', unsafe_allow_html=True)

# ============================
# 2. Eingaben
# ============================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🌊 Gewässer")
    gewaesser_typ = st.selectbox("Typ", ["See", "Baggersee", "Kanal", "Fluss", "Strom"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömung", ["Keine", "Leicht", "Mittel", "Stark"])
    tiefe_spot = st.number_input("Tiefe (m)", 0.5, 40.0, 3.5)
    ausbringung = st.radio("Ausbringung", ["Wurf", "Boot", "Beides"])
    
with c2:
    st.markdown("### 🌡️ Umwelt & Zeit")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"])
    zeit = st.multiselect("Zeitraum", ["Vormittag", "Nachmittag", "Abend", "Nacht"], default=["Abend"])
    weissfisch = st.select_slider("Weißfisch-Dichte", ["Niedrig", "Mittel", "Hoch", "Extrem"])

with c3:
    st.markdown("### 🏗️ Spot & Hindernisse")
    boden = st.selectbox("Boden", ["Sand/Kies", "Lehm", "Schlamm", "Moder"])
    hindernisse = st.multiselect("Hindernisse", ["Muschelbänke", "Totholz", "Kraut", "Krebse"])
    angeldruck = st.selectbox("Angeldruck", ["Gering", "Mittel", "Hoch"])

# ============================
# 3. Hilfsfunktionen
# ============================
def kleinerer_haken(gr):
    return min(10, gr + 1)

def groesserer_haken(gr):
    return max(2, gr - 1)

# ============================
# 4. Logik-Engine
# ============================
def berechne_hilfe():
    t = {
        "blei_form": "Birne",
        "blei_gew": 85,
        "blei_typ": "Safety-Clip",
        "vorfach_mat": "Coated Braid",
        "vorfach_len": 20,
        "h_typ": "Wide Gape",
        "h_gr": 6,
        "h_farbe": "Dunkel",
        "koeder": "",
        "koeder_gr": 20,
        "koeder_h": "Normal",
        "futter_menge": 0,
        "futter_typ": "",
        "spot_hilfe": "",
        "begruendungen": []
    }

    # ============================
    # Spot-Hilfestellung
    # ============================
    if tiefe_spot < 3:
        t["spot_hilfe"] = "Flachwasser, nahe Ufer – ruhig ablegen, Fische nahe Kraut oder Muscheln."
    elif tiefe_spot < 10:
        t["spot_hilfe"] = "Mittlere Tiefe – Plateau oder Kanten, Fische mittig im Wasser."
    else:
        t["spot_hilfe"] = "Tiefe Stellen – Rinnen oder Plateaus, Fische eher am Boden."

    t["begruendungen"].append(f"📍 Spot-Hilfe: {t['spot_hilfe']}")

    # ============================
    # Hindernisse & Blei
    # ============================
    if hindernisse:
        if any(h in ["Muschelbänke", "Totholz"] for h in hindernisse):
            t["blei_typ"] = "Drop-Off"
            t["vorfach_mat"] = "Abriebfestes Mono/Snag Leader"
            t["begruendungen"].append("🪵 Hindernisse → Drop-Off Blei & robustes Vorfach.")
        if "Kraut" in hindernisse or boden=="Schlamm":
            t["blei_typ"] = "Heli-Safe"
            t["vorfach_len"] += 10
            t["begruendungen"].append("☁️ Kraut/Schlamm → Helikopter-Rig verhindert Einsinken.")
    else:
        t["begruendungen"].append("✅ Keine Hindernisse – Standardsetup.")

    # ============================
    # Blei-Form & Gewicht
    # ============================
    if stroemung=="Stark" or gewaesser_typ=="Strom":
        t["blei_form"], t["blei_gew"] = "Krallenblei (Grippa)", 180
        t["begruendungen"].append("🌊 Starke Strömung → Grippa-Blei für Halt.")
    elif stroemung=="Mittel":
        t["blei_form"], t["blei_gew"] = "Flaches Sargblei", 130
    if ausbringung in ["Wurf","Beides"] and tiefe_spot>10:
        t["blei_form"] = "Zip-Blei"
        t["begruendungen"].append("🚀 Weitwurf/Tiefe → aerodynamisches Zip-Blei.")

    # ============================
    # Köderart automatisch
    # ============================
    if hindernisse or weissfisch in ["Hoch","Extrem"]:
        t["koeder"] = "Hart/Pop-Up"
        t["koeder_gr"] = 24
        t["koeder_h"] = "Extra Hart"
        t["begruendungen"].append("🐟 Störfische/Hindernisse → Hart/Pop-Up Köder.")
    elif temp<13:
        t["koeder"] = "Fein/Wafter"
        t["koeder_gr"] = 18
        t["koeder_h"] = "Normal"
        t["begruendungen"].append("❄️ Kalt → Feiner Köder.")
    else:
        t["koeder"] = "Boilie"
        t["koeder_gr"] = 20
        t["koeder_h"] = "Normal"
        t["begruendungen"].append("☀️ Standardbedingungen → Boilie Köder.")

    # ============================
    # Futterstrategie automatisch
    # ============================
    if temp<7:
        t["futter_menge"] = 0.3
        t["futter_typ"] = "Fein & hochattraktiv"
    elif temp<13:
        t["futter_menge"] = 0.8
        t["futter_typ"] = "Leicht verdaulich, kompakt"
    elif temp<22:
        t["futter_menge"] = 2.0
        t["futter_typ"] = "Boilies + Partikel"
    else:
        t["futter_menge"] = 1.5
        t["futter_typ"] = "Kontrolliert & punktuell"
    t["begruendungen"].append(f"🍽️ Futter: {t['futter_menge']} kg – {t['futter_typ']}")

    return t

# ============================
# 5. Ausgabe
# ============================
if st.button("Hilfe generieren"):
    t = berechne_hilfe()

    st.markdown('<div class="section-header">📋 Dein Setup</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)

        r1.metric("Blei", f"{t['blei_gew']} g", t["blei_form"])
        r1.write(f"System: {t['blei_typ']}")

        r2.metric("Vorfach", f"{t['vorfach_len']} cm", t["vorfach_mat"])
        r2.write(f"Haken: {t['h_typ']} Gr. {t['h_gr']} ({t['h_farbe']})")

        r3.metric("Köder", f"{t['koeder_gr']} mm", t["koeder_h"])
        r3.write(f"Typ: {t['koeder']}")

        r4.metric("Futter", f"{t['futter_menge']} kg", t["futter_typ"])
        r4.write(f"Spot-Hilfe: {t['spot_hilfe']}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Begründungen")
    for b in t["begruendungen"]:
        st.write("•", b)
