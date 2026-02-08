import streamlit as st
import datetime

# ==========================================
# 1. SETUP & MOBIL-OPTIMIERTES DESIGN
# ==========================================
st.set_page_config(page_title="Karpfen-Taktik Pro v6.0", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 1.8rem; color: #1b5e20; font-weight: bold; margin-bottom: 15px; text-align: center; }
    .hinweis-box { background-color: #e8f4fd; padding: 12px; border-radius: 10px; border-left: 5px solid #2196f3; margin-bottom: 20px; font-size: 0.9rem; }
    .section-header { background-color: #2e7d32; color: white; padding: 10px; border-radius: 8px; margin-top: 15px; margin-bottom: 10px; font-weight: bold; font-size: 1.1rem; text-align: center; }
    .taktik-detail { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #2e7d32; margin-bottom: 10px; font-size: 0.95rem; line-height: 1.4; }
    .spot-empfehlung { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px dashed #4caf50; font-weight: 500; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik Pro v6.0</div>', unsafe_allow_html=True)

# ==========================================
# 2. EINGABEMASKE
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässer & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0)
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5)
    angeltag = st.date_input("Wann fischst du?", datetime.date.today())

with c2:
    m = angeltag.month
    if m in [3,4,5]: jz = "Frühjahr"
    elif m in [6,7,8]: jz = "Sommer"
    elif m in [9,10,11]: jz = "Herbst"
    else: jz = "Winter"
    st.write(f"**Erkannte Jahreszeit:** {jz}")
    
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    luftdruck = st.number_input("Luftdruck (hPa)", 950, 1050, 1013)
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"])

with c3:
    boden = st.selectbox("Bodenbeschaffenheit", ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=0)
    zeit = st.multiselect("Wann fischst du?", ["Vormittag", "Nachmittag", "Abend", "Nacht"], placeholder="-- Bitte wählen --")
    hindernisse = st.multiselect("Hindernisse", ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], placeholder="-- Bitte wählen --")
    weissfisch = st.select_slider("Weißfischvorkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"], value="Mittel")
    ausbringung = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    b_taktik = "Normal"; w_weite = 0
    if ausbringung == "Boot":
        b_taktik = st.selectbox("Boot-Vorgehen", ["Nur Ablegen", "Vom Boot auswerfen"])
    elif ausbringung == "Wurf vom Ufer":
        w_weite = st.slider("Wurfweite (m)", 0, 180, 60)
    
    ziel_kg = st.number_input("Max. Karpfengewicht (kg)", 5, 40, 15)
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"], value="Normal")

# ==========================================
# 3. EXPERTEN-LOGIK (VORFACH, WURF & HAKENFARBE)
# ==========================================
def berechne_pro_logic():
    s = {
        "blei_typ": "Safety-Clip Montage", "blei_form": "Birnenform", "blei_gew": 90,
        "rig_typ": "Standard Haar-Rig", "pres": "Bodenköder", "vorfach_mat": "Coated Braid", 
        "vorfach_len": "15-20 cm", "h_typ": "Wide Gape", "h_gr": 6, "h_farbe": "Dunkelgrau (Matt)",
        "k_empf": "Standard 20mm Boilie", "f_menge": "Moderat (ca. 1kg)",
        "logik": {"montage": "", "haken": "", "vorfach": "", "tangle": ""}
    }

    # HAKENFARBE & BESCHICHTUNG (Lichtphysik)
    if any(z in zeit for z in ["Vormittag", "Nachmittag"]) and temp > 10:
        s["h_farbe"] = "Teflon beschichtet (Matt-Grau)"
        s["logik"]["haken"] = "➔ **Licht-Physik:** Bei Tageslicht verhindern Teflon-Beschichtungen Lichtreflexionen am Metall, die Fische abschrecken könnten."
    else:
        s["h_farbe"] = "Dunkelgrau / Schwarz"

    # VORFACH-MATERIAL & WURF-SICHERHEIT
    verwicklungsgefahr = (ausbringung == "Wurf vom Ufer" and w_weite > 70)

    if aktivitaet == "Aggressiv":
        if verwicklungsgefahr:
            s["vorfach_mat"] = "Coated Braid (Steif gestrippt)"
            s["logik"]["tangle"] = "⚠️ **Wurf-Sicherung:** Wegen der Wurfweite nutzen wir ein ummanteltes Geflecht. Das steife Ende verhindert Überschläge im Flug, während das weiche Haar den aggressiven Fisch hakt."
        else:
            s["vorfach_mat"] = "Steifes Mono / Stiff Rig"
            s["logik"]["vorfach"] = "➔ **Aggressiv:** Maximale Hebelwirkung für schnelles Greifen des Hakens."
            
    elif aktivitaet == "Vorsichtig":
        s["vorfach_mat"] = "Fluorocarbon (Unsichtbar)"
        if verwicklungsgefahr:
            s["logik"]["tangle"] = "⚠️ **Wurf-Sicherung:** Nutze zwingend einen langen 'Anti-Tangle-Sleeve', um das Fluorocarbon beim Wurf vom Blei wegzudrücken."
    
    elif aktivitaet == "Apathisch":
        s["vorfach_mat"] = "Sehr weiches Geflecht"
        if verwicklungsgefahr:
            s["logik"]["tangle"] = "⚠️ **Warnung:** Weiches Geflecht verwickelt sich beim Wurf extrem leicht. Nutze PVA-Tape oder Schaum am Haken!"

    # RESTE DER LOGIK
    if boden in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"; s["rig_typ"] = "Helikopter-Rig"; s["vorfach_len"] = "25-35 cm"
    if ausbringung == "Wurf vom Ufer" and w_weite > 100: s["blei_gew"] = 125; s["blei_form"] = "Zip-Blei"

    return s

ergebnis = berechne_pro_logic()

# ==========================================
# 4. AUSGABE
# ==========================================
st.markdown("---")
st.markdown('<div class="section-header">🛡️ 2. Deine optimierte Taktik-Empfehlung</div>', unsafe_allow_html=True)
res_c1, res_c2, res_c3 = st.columns(3)

with res_c1:
    st.subheader("🎣 Montage")
    st.info(f"**System:** {ergebnis['blei_typ']}\n\n**Blei:** {ergebnis['blei_form']} ({ergebnis['blei_gew']}g)")

with res_c2:
    st.subheader("🧶 Rig & Vorfach")
    st.success(f"**Material:** {ergebnis['vorfach_mat']}\n\n**Länge:** {ergebnis['vorfach_len']}")
    if ergebnis['logik']['tangle']: st.warning(ergebnis['logik']['tangle'])
    else: st.markdown(f"<small>{ergebnis['logik']['vorfach']}</small>", unsafe_allow_html=True)

with res_c3:
    st.subheader("🪝 Haken-Setup")
    st.warning(f"**Modell:** {ergebnis['h_typ']} (Gr. {ergebnis['h_gr']})\n\n**Farbe:** {ergebnis['h_farbe']}")
    st.markdown(f"<small>{ergebnis['logik']['haken']}</small>", unsafe_allow_html=True)

st.markdown('<div class="section-header">🔍 3. Analyse-Details</div>', unsafe_allow_html=True)
st.write(f"➔ **Fischverhalten:** {aktivitaet} | **Wurfsicherheit:** {'Kritisch' if w_weite > 80 else 'Stabil'}")
if druck_tendenz == "Fallend": st.success("🔥 **Beißfenster:** Druck fällt - Fische fressen!")

def get_moon(d):
    diff = d - datetime.date(2001, 1, 1); lun = 29.530588853; pos = (diff.days / lun) % 1
    if pos < 0.06: return "🌑 Neumond", "Dunkelheit: Beste Tarnung."
    if 0.45 < pos < 0.55: return "🌕 Vollmond", "Vorsicht vor Lichtreflexionen am Haken!"
    return "🌓 Sichelmond", "Normal."

mond_n, mond_t = get_moon(angeltag)
st.markdown(f'<div class="taktik-detail">🌙 **Mond ({angeltag.strftime("%d.%m.%Y")}):** {mond_n} - {mond_t}</div>', unsafe_allow_html=True)
