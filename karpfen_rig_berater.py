import streamlit as st
import datetime

# ==========================================
# 1. SETUP & DESIGN
# ==========================================
st.set_page_config(page_title="Karpfen-Taktik Pro v9.1", layout="wide")

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

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik Pro v9.1 (Final Run)</div>', unsafe_allow_html=True)

# ==========================================
# 2. EINGABEN
# ==========================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 🌊 Gewässer")
    gewaesser_typ = st.selectbox("Typ", ["See", "Baggersee", "Kanal", "Fluss", "Strom"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömung", ["Keine", "Leicht", "Mittel", "Stark"])
    tiefe_spot = st.number_input("Tiefe (m)", 0.5, 40.0, 3.5)
    ausbringung = st.radio("Ausbringung", ["Wurf", "Futterboot", "Boot"])
    wurfweite = st.slider("Wurfweite (m)", 0, 180, 60) if ausbringung == "Wurf" else 0

with c2:
    st.markdown("### 🌡️ Umwelt")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"])
    zeit = st.multiselect("Zeitraum", ["Vormittag", "Nachmittag", "Abend", "Nacht"], default=["Abend"])
    jahreszeit = st.selectbox(
        "Jahreszeit",
        ["Winter", "Frühling", "Sommer", "Herbst"],
        index=datetime.datetime.now().month // 3 % 4
    )

with c3:
    st.markdown("### 🏗️ Spot")
    boden = st.selectbox("Boden", ["Sand/Kies", "Lehm", "Schlamm", "Moder"])
    hindernisse = st.multiselect("Hindernisse", ["Muschelbänke", "Totholz", "Kraut", "Krebse"])
    spot_typ = st.selectbox("Spot-Typ", ["Plateau", "Kante", "Rinne", "Freiwasser", "Ufernah"])
    angeldruck = st.selectbox("Angeldruck", ["Gering", "Mittel", "Hoch"])

with c4:
    st.markdown("### 🐟 Fisch & Köder")
    weissfisch = st.select_slider("Weißfisch-Dichte", ["Niedrig", "Mittel", "Hoch", "Extrem"])
    aktivitaet = st.select_slider("Fisch-Vorsicht", ["Vorsichtig", "Normal", "Aggressiv"], value="Normal")
    koeder_art = st.selectbox("Köder-Art", ["Bodenköder", "Pop-Up", "Wafter", "Snowman"])
    futterstrategie = st.selectbox("Futterstrategie", ["Punktuell", "Flächig", "Nachlegen"])

# ==========================================
# 3. HILFSFUNKTIONEN
# ==========================================
def kleinerer_haken(gr):
    return min(10, gr + 1)

def groesserer_haken(gr):
    return max(2, gr - 1)

# ==========================================
# 4. LOGIK-ENGINE
# ==========================================
def berechne_taktik():
    s = {
        "blei_form": "Birne",
        "blei_gew": 85,
        "blei_typ": "Safety-Clip",
        "vorfach_mat": "Coated Braid",
        "vorfach_len": 20,
        "h_typ": "Wide Gape",
        "h_gr": 6,
        "h_farbe": "Dunkel",
        "koeder": koeder_art,
        "koeder_gr": 20,
        "koeder_h": "Normal",
        "begruendungen": []
    }

    score = 50

    # --- Strömung & Distanz
    if stroemung == "Stark" or gewaesser_typ == "Strom":
        s["blei_form"], s["blei_gew"] = "Krallenblei (Grippa)", 180
        s["begruendungen"].append("🌊 Starke Strömung → Grippa für sicheren Halt.")
        score += 5
    elif stroemung == "Mittel":
        s["blei_form"], s["blei_gew"] = "Flaches Sargblei", 130

    if ausbringung == "Wurf" and wurfweite > 90:
        s["blei_form"] = "Zip-Blei"
        s["begruendungen"].append("🚀 Große Distanz → aerodynamisches Zip-Blei.")
        score += 3

    # --- Tiefe
    if tiefe_spot > 10:
        s["blei_gew"] += 30
        s["begruendungen"].append("⬇️ Große Tiefe → schwereres Blei für saubere Ablage.")
        score += 5

    # --- Boden & Hindernisse
    if boden == "Schlamm" or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe"
        s["vorfach_len"] += 10
        s["begruendungen"].append("☁️ Weicher Boden → Helikopter-Rig verhindert Einsinken.")
        score += 5

    if any(h in hindernisse for h in ["Totholz", "Muschelbänke"]):
        s["blei_typ"] = "Drop-Off"
        s["begruendungen"].append("🪵 Hindernisse → Drop-Off reduziert Fischverluste.")
        score -= 5

    # --- Vorfachmaterial
    if any(h in hindernisse for h in ["Muschelbänke", "Totholz"]):
        s["vorfach_mat"] = "Abriebfestes Mono / Snag Leader"
        s["begruendungen"].append("🪨 Abriebgefahr → robustes Vorfachmaterial.")
    elif aktivitaet == "Vorsichtig" and boden in ["Sand/Kies", "Lehm"]:
        s["vorfach_mat"] = "Fluorocarbon"
        s["begruendungen"].append("👀 Vorsichtige Fische → Fluorocarbon für Tarnung.")
    else:
        s["vorfach_mat"] = "Coated Braid"

    # --- Luftdruck
    if druck_tendenz == "Fallend":
        s["vorfach_len"] -= 5
        s["begruendungen"].append("📉 Fallender Luftdruck → aggressiveres Rig.")
        score += 5
    elif druck_tendenz == "Steigend":
        s["vorfach_len"] += 5
        s["h_gr"] = kleinerer_haken(s["h_gr"])
        s["begruendungen"].append("📈 Steigender Druck → vorsichtigere Präsentation.")
        score -= 5

    # --- Fischverhalten
    if aktivitaet == "Vorsichtig":
        s["vorfach_len"] += 10
        s["h_gr"] = kleinerer_haken(s["h_gr"])
        s["begruendungen"].append("🎯 Vorsichtige Fische → längeres Vorfach & kleinerer Haken.")
        score -= 5
    elif aktivitaet == "Aggressiv":
        s["vorfach_len"] -= 5
        s["h_gr"] = groesserer_haken(s["h_gr"])
        s["begruendungen"].append("💥 Aggressive Fische → kürzeres Vorfach & größerer Haken.")
        score += 5

    # --- Weißfisch / Krebse
    if weissfisch in ["Hoch", "Extrem"] or "Krebse" in hindernisse:
        s["koeder_gr"] = 24
        s["koeder_h"] = "Extra Hart"
        s["begruendungen"].append("🐟 Störfische → große, harte Köder.")
        score -= 5

    # --- Futter & Temperatur
    if temp < 7:
        s["futter_menge"] = 0.3
        s["futter_typ"] = "Fein & hochattraktiv"
        s["begruendungen"].append("❄️ Kaltes Wasser → sehr wenig, hochattraktives Futter.")
    elif temp < 13:
        s["futter_menge"] = 0.8
        s["futter_typ"] = "Leicht verdaulich, kompakt"
        s["begruendungen"].append("🌡️ Kühles Wasser → reduzierte Futtermenge.")
    elif temp < 22:
        s["futter_menge"] = 2.0
        s["futter_typ"] = "Boilies + Partikel"
        s["begruendungen"].append("☀️ Optimale Temperatur → aktive Fische.")
    else:
        s["futter_menge"] = 1.5
        s["futter_typ"] = "Kontrolliert & punktuell"
        s["begruendungen"].append("🔥 Sehr warm → nicht überfüttern.")

    # --- Angeldruck
    if angeldruck == "Hoch":
        score -= 5
    elif angeldruck == "Gering":
        score += 5

    # --- Score
    score = max(0, min(100, score))
    s["score"] = score

    if score >= 75:
        s["ampel"] = "🟢 Sehr hohe Chance"
    elif score >= 50:
        s["ampel"] = "🟡 Solide Bedingungen"
    else:
        s["ampel"] = "🔴 Anspruchsvoll"

    return s

# ==========================================
# 5. AUSGABE
# ==========================================
if st.button("PRO-TAKTIK GENERIEREN"):
    t = berechne_taktik()

    st.markdown('<div class="section-header">📋 Dein Einsatzplan</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns(4)

        r1.metric("Blei", f"{t['blei_gew']} g", t["blei_form"])
        r1.write(f"System: {t['blei_typ']}")

        r2.metric("Vorfach", f"{t['vorfach_len']} cm", t["vorfach_mat"])
        r2.write(f"Haken: {t['h_typ']} Gr. {t['h_gr']} ({t['h_farbe']})")

        r3.metric("Köder", f"{t['koeder_gr']} mm", t["koeder_h"])
        r3.write(f"Typ: {t['koeder']}")

        r4.metric("Score", f"{t['score']} %", t["ampel"])
        r4.write(f"Futter: {t['futter_menge']} kg – {t['futter_typ']}")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Warum diese Taktik?")
    for b in t["begruendungen"]:
        st.write("•", b)
