import streamlit as st
import datetime

# ============================
# 1. Setup & Design
# ============================
st.set_page_config(page_title="Karpfen-Hilfe v2.5 Ultimate", layout="wide")

st.markdown("""
<style>
.main-header { font-size: 2.2rem; color: #1b5e20; font-weight: bold; text-align: center; }
.section-header { background-color: #2e7d32; color: white; padding: 10px; border-radius: 8px; margin-top: 20px; font-weight: bold; }
.result-card { background-color: #f1f8e9; padding: 20px; border-radius: 15px; border: 1px solid #c8e6c9; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎣 Karpfen-Hilfe v2.5 (Vollversion)</div>', unsafe_allow_html=True)

# ============================
# 2. Eingaben (Alle Felder!)
# ============================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🌊 Gewässer & Mechanik")
    gewaesser_typ = st.selectbox("Typ", ["-- Bitte wählen --", "See", "Baggersee", "Kanal", "Fluss", "Strom"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömung", ["Keine", "Leicht", "Mittel", "Stark"])
    tiefe_spot = st.number_input("Tiefe (m)", 0.5, 40.0, 3.5)
    ausbringung = st.selectbox("Ausbringung", ["-- Bitte wählen --", "Wurf", "Boot", "Beides"])
    boot_variante = None
    if ausbringung == "Boot":
        boot_variante = st.selectbox("Boot-Unterauswahl", ["-- Bitte wählen --", "Wurf vom Boot", "Ablegen vom Boot"])
    wurfweite = st.slider("Wurfweite (m)", 0, 180, 60)

with c2:
    st.markdown("### 🌡️ Umwelt & Biologie")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    wetter = st.selectbox("Wetter", ["-- Bitte wählen --", "Sonnig", "Bewölkt", "Regen"])
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["-- Bitte wählen --", "Stabil", "Fallend", "Steigend"])
    zeit = st.multiselect("Zeitraum", ["Vormittag", "Nachmittag", "Abend", "Nacht"], default=["Abend"])
    jahreszeit = st.selectbox("Jahreszeit", ["Winter", "Frühling", "Sommer", "Herbst"], 
                             index=datetime.datetime.now().month // 3 % 4)
    weissfisch = st.select_slider("Weißfisch-Dichte", ["Niedrig", "Mittel", "Hoch", "Extrem"])
    karpfen_max = st.number_input("Erwartete Maximalgröße (kg)", 1.0, 50.0, 12.0)

with c3:
    st.markdown("### 🏗️ Spot & Strategie")
    boden = st.selectbox("Boden", ["-- Bitte wählen --", "Sand/Kies", "Lehm", "Schlamm", "Moder"])
    hindernisse = st.multiselect("Hindernisse", ["Muschelbänke", "Totholz", "Kraut", "Krebse"])
    angeldruck = st.selectbox("Angeldruck", ["-- Bitte wählen --", "Gering", "Mittel", "Hoch"])

# ============================
# 3. Logik-Engine (Verknüpfung)
# ============================
def berechne_hilfe():
    t = {
        "blei_form": "Birne", "blei_gew": 85, "blei_typ": "Safety-Clip",
        "vorfach_mat": "Coated Braid", "vorfach_len": 20, "h_typ": "Wide Gape",
        "h_gr": 6, "h_farbe": "Dunkel", "koeder": "Boilie", "koeder_gr": 20,
        "koeder_h": "Normal", "futter_menge": 0, "futter_typ": "", "begruendungen": []
    }

    # -- BLEI & SYSTEM --
    if stroemung in ["Mittel", "Stark"] or gewaesser_typ == "Strom":
        t["blei_form"], t["blei_gew"] = "Grippa", (180 if stroemung == "Stark" else 130)
    elif wurfweite > 90:
        t["blei_form"] = "Zip-Blei"

    if "Kraut" in hindernisse or boden == "Schlamm":
        t["blei_typ"], t["vorfach_len"] = "Heli-Safe", 30
        t["begruendungen"].append("☁️ Helikopter-System für weichen Boden/Kraut.")
    elif any(h in ["Muschelbänke", "Totholz"] for h in hindernisse):
        t["blei_typ"], t["vorfach_mat"] = "Drop-Off", "Abriebfestes Mono"
        t["begruendungen"].append("🪵 Drop-Off & Snag-Leader für Hindernisse.")

    # -- HAKEN (Größe vs. Fischgewicht vs. Druck) --
    h_nummer = 8 if karpfen_max < 8 else (4 if karpfen_max > 20 else 6)
    if angeldruck == "Hoch": h_nummer = min(10, h_nummer + 2) # Kleinerer Haken bei Druck
    t["h_gr"] = h_nummer
    
    if wetter == "Sonnig" and tiefe_spot < 4:
        t["h_farbe"] = "Matt / Reflexionsfrei"

    # -- KÖDER (Temp x Weißfisch x Krebse) --
    if weissfisch in ["Hoch", "Extrem"] or "Krebse" in hindernisse:
        t["koeder_gr"], t["koeder_h"] = 24, "Extra Hart"
        t["begruendungen"].append("🦀 Köder gegen Krebse/Weißfisch gehärtet.")
    elif temp < 12:
        t["koeder"], t["koeder_gr"] = "Wafter / Pop-Up", 16

    # -- FUTTER (Jahreszeit x Temp x Druck) --
    menge = 0.5
    if temp > 15: menge += 1.5
    if jahreszeit == "Herbst": menge += 1.0 # "Fressen für den Winter"
    if druck_tendenz == "Fallend": menge += 0.5
    t["futter_menge"] = round(menge, 1)
    t["futter_typ"] = "High-Attract / Low-Oil" if temp < 12 else "Nahrhaft (Fischmehl)"

    return t

# ============================
# 4. Ausgabe
# ============================
if st.button("HILFE GENERIEREN"):
    if gewaesser_typ == "-- Bitte wählen --" or boden == "-- Bitte wählen --":
        st.warning("⚠️ Bitte wähle mindestens Gewässertyp und Boden aus!")
    else:
        res = berechne_hilfe()
        st.markdown('<div class="section-header">📋 Dein Einsatzplan</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Blei", f"{res['blei_gew']}g", res["blei_form"])
            r1.write(f"System: {res['blei_typ']}")
            r2.metric("Vorfach", f"{res['vorfach_len']}cm", res["vorfach_mat"])
            r2.write(f"Haken: Gr. {res['h_gr']} ({res['h_farbe']})")
            r3.metric("Köder", f"{res['koeder_gr']}mm", res["koeder_h"])
            r3.write(f"Typ: {res['koeder']}")
            r4.metric("Futter", f"{res['futter_menge']}kg", res["futter_typ"])
            r4.write(f"Saison: {jahreszeit}")
            st.markdown('</div>', unsafe_allow_html=True)
        for b in res["begruendungen"]:
            st.info(b)
