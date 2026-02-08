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
# 2. EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässer & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"],
                                help="Bestimmt die grundlegende Montage und Strömungsgefahr am Spot.")
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"],
                                    help="Beeinflusst Bleigewicht, Bleiform (Krallen) und Wurfwinkel.")
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0,
                                help="Wichtig, um das thermische Verhalten des Wassers (Sprungschicht) zu berechnen.")
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5,
                                help="Die Tiefe, in der dein Köder tatsächlich liegen soll.")
    angeltag = st.date_input("Wann fischst du?", datetime.date.today(),
                             help="Berechnet die Mondphase und die saisonale Taktik für diesen Tag.")

with c2:
    # JAHRESZEIT AUTOMATIK
    month = angeltag.month
    if 3 <= month <= 5: jahreszeit = "Frühjahr"
    elif 6 <= month <= 8: jahreszeit = "Sommer"
    elif 9 <= month <= 11: jahreszeit = "Herbst"
    else: jahreszeit = "Winter"
    st.write(f"**Erkannte Jahreszeit:** {jahreszeit}")
    
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15,
                     help="Direkter Einfluss auf den Stoffwechsel und die benötigte Futtermenge.")
    luftdruck = st.number_input("Luftdruck (hPa)", 950, 1050, 1013,
                                help="1013 hPa ist der Standard. Fallender Druck ist oft ein Beiß-Signal.")
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"],
                                 help="Fallender Druck deutet oft auf fressende Fische hin.")

with c3:
    boden = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], 
                                 index=0, help="Entscheidet über Bleiform (Einsinken) und Vorfachlänge.")
    zeit = st.multiselect("Wann planst du zu fischen?", 
                                 ["Vormittag", "Nachmittag", "Abend", "Nacht"], 
                                 placeholder="-- Bitte wählen --",
                                 help="Beeinflusst Lichtverhältnisse, Sauerstoff und Fischzugrouten.")
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], 
                                placeholder="-- Bitte wählen --",
                                help="Bestimmt das Montagensystem (Heli-Safe/Safety-Clip) und die Hakenstabilität.")
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", 
                                  options=["Niedrig", "Mittel", "Hoch", "Extrem"], 
                                  value="Mittel",
                                  help="Beeinflusst Ködergröße und Härte, um Beifänge zu vermeiden.")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], 
                           horizontal=True, help="Wähle, wie du deine Montage zum Spot bringst.")
    
    boots_taktik = "Normal"; wurfweite = 0
    if ausbringung == "Boot":
        boots_taktik = st.selectbox("Vorgehen vom Boot", ["Nur Ablegen", "Vom Boot auswerfen"], help="Ablegen erlaubt schwerere Bleie.")
    elif ausbringung == "Wurf vom Ufer":
        wurfweite = st.slider("Wurfweite (m)", 0, 180, 60, help="Beeinflusst Bleiform, Gewicht und Verwicklungsgefahr.")
    
    ziel_kg = st.number_input("Max. Karpfengewicht (kg)", 5, 40, 15, help="Wichtig für Hakenstärke.")
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", 
                                  options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"], 
                                  value="Normal", help="Bestimmt Vorfachmaterial und Steifigkeit.")
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (VOLLSTÄNDIG)
# ==========================================
def berechne_pro_logic():
    # Standard-Setup initialisieren
    s = {
        "blei_typ": "Safety-Clip Montage", "blei_form": "Birnenform (Smooth)", "blei_gew": 90,
        "rig_typ": "Standard Haar-Rig", "pres": "Bodenköder", 
        "vorfach_mat": "Coated Braid (Ummantelt)", "vorfach_len": "15-20 cm",
        "leader": "Leadcore / Anti-Tangle-Tube", "h_typ": "Wide Gape",
        "h_spitze": "Straight Point", "h_oehr": "Gerade", "h_draht": "Standard", "h_gr": 6,
        "h_farbe": "Dunkelgrau (Matt)", "k_empf": "Standard 20mm Boilie", 
        "k_h": "Normal", "k_gr": "20mm", "f_menge": "Moderat (ca. 1kg)", 
        "f_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], "spot_empfehlungen": [], "unsicher": False
    }

    # Haken-Farbe (Licht-Physik)
    if any(z in zeit for z in ["Vormittag", "Nachmittag"]) and temp > 10:
        s["h_farbe"] = "Teflon beschichtet (Reflexionsfrei)"
        s["begruendungen"].append("➔ **Licht-Physik:** Teflon verhindert Metall-Reflexionen bei Tageslicht.")

    # Vorfach & Wurfweite-Logik
    verwicklungsgefahr = (ausbringung == "Wurf vom Ufer" and wurfweite > 70)
    
    if aktivitaet == "Aggressiv":
        if verwicklungsgefahr:
            s["vorfach_mat"] = "Coated Braid (Steif)"
            s["begruendungen"].append("➔ **Wurfsicherheit:** Ummanteltes Geflecht verhindert Überschläge bei Weitwürfen.")
        else:
            s["vorfach_mat"] = "Steifes Mono (Stiff Rig)"
            s["begruendungen"].append("➔ **Aggressiv:** Steifes Material maximiert den Hebeleffekt für schnelles Haken.")
    elif aktivitaet == "Vorsichtig":
        s["vorfach_mat"] = "Fluorocarbon (Unsichtbar)"
        s["begruendungen"].append("➔ **Tarnung:** Fluorocarbon ist im klaren Wasser fast unsichtbar.")

    # Boden & Montage
    if boden in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"; s["rig_typ"] = "Helikopter-Rig"
        s["pres"] = "Pop-Up / Schneemann"; s["vorfach_len"] = "25-35 cm"
        s["begruendungen"].append("➔ **Heli-Safe:** Verhindert das Einsinken des Köders im weichen Grund/Kraut.")
    
    # Luftdruck & Futter
    if druck_tendenz == "Fallend":
        s["f_menge"] = "Aggressiv (2-3kg)"
        s["begruendungen"].append("➔ **Luftdruck:** Fallender Druck steigert den Fresstrieb massiv.")
    elif luftdruck > 1025:
        s["f_menge"] = "Minimal (Single Bait)"; s["k_empf"] = "Auffälliger Pop-Up"

    # Weißfisch-Abwehr
    if weissfisch in ["Hoch", "Extrem"] or "Krebse" in hindernisse:
        s["k_h"] = "Extra Hart"; s["k_gr"] = "24mm+"; s["k_empf"] = "Harte Fisch-Boilies / Tigernüsse"
    
    # Boot & Wurfweite
    if ausbringung == "Boot":
        s["blei_gew"] = 140 if boots_taktik == "Nur Ablegen" else 110
    elif ausbringung == "Wurf vom Ufer" and wurfweite > 100:
        s["blei_gew"] = 125; s["blei_form"] = "Zip-Blei (Distanz)"

    # Haken-Mechanik
    if s["pres"] != "Bodenköder":
        s["h_typ"] = "Curve Shank"; s["h_oehr"] = "Nach innen gebogen"
    if ziel_kg > 22 or any(h in hindernisse for h in ["Muschelbänke", "Scharfe Kanten"]):
        s["h_draht"] = "X-Strong"; s["h_gr"] = 4
        s["begruendungen"].append("➔ **Stabilität:** X-Strong Haken verhindern das Aufbiegen bei Großfisch/Hindernis.")

    return s

ergebnis = berechne_pro_logic()

# ==========================================
# 4. AUSGABE: RESULTATE
# ==========================================
st.markdown("---")
st.markdown('<div class="section-header">🛡️ 2. Deine optimierte Taktik-Empfehlung</div>', unsafe_allow_html=True)
res_c1, res_c2, res_c3 = st.columns(3)

with res_c1:
    st.subheader("🎣 Montage")
    st.info(f"**System:** {ergebnis['blei_typ']}\n\n**Blei:** {ergebnis['blei_form']} ({ergebnis['blei_gew']}g)")

with res_c2:
    st.subheader("🧶 Vorfach")
    st.success(f"**Material:** {ergebnis['vorfach_mat']}\n\n**Länge:** {ergebnis['vorfach_len']}\n\n**Rig:** {ergebnis['rig_typ']}")

with res_c3:
    st.subheader("🪝 Haken")
    st.warning(f"**Modell:** {ergebnis['h_typ']} (Gr. {ergebnis['h_gr']})\n\n**Farbe:** {ergebnis['h_farbe']}\n\n**Draht:** {ergebnis['h_draht']}")

st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k1, k2 = st.columns(2)
with k1:
    st.write(f"**Köder:** {ergebnis['k_empf']}\n\n**Größe:** {ergebnis['k_gr']} | **Härte:** {ergebnis['k_h']}")
with k2:
    st.write(f"**Menge:** {ergebnis['f_menge']}\n\n**Art:** {ergebnis['f_art']}")

st.markdown('<div class="section-header">🔍 4. Spot-Analyse & Natur-Physik</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)
with sa1:
    st.markdown(f'<div class="spot-empfehlung">Tiefe: {tiefe_spot}m | Max: {tiefe_max}m | Jahreszeit: {jahreszeit}</div>', unsafe_allow_html=True)
    if luftdruck > 1022: st.warning("⚖️ **ZIG-Rig Tipp:** Hoher Druck! Fische stehen evtl. im Mittelwasser.")
with sa2:
    if "Nacht" in zeit: st.write("📍 Nacht-Tipp: Eine Rute extrem flach (0.5 - 1.5m) ablegen.")
    if ausbringung == "Boot": st.write("➔ **Boot-Profi:** Backleads nutzen, um Schnur am Boot abzusenken.")

def get_moon(d):
    diff = d - datetime.date(2001, 1, 1); lun = 29.530588853; pos = (diff.days / lun) % 1
    if pos < 0.06: return "🌑 Neumond", "Beste Tarnung nachts."
    if 0.45 < pos < 0.55: return "🌕 Vollmond", "Reflexionen & Schnurschatten kritisch!"
    return "🌓 Sichelmond", "Normale Bedingungen."

m_n, m_t = get_moon(angeltag)
st.markdown(f'<div class="taktik-detail">🌙 **Mond ({angeltag.strftime("%d.%m.%Y")}):** {m_n} - {m_t}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📖 Experten-Logik (Das Warum)</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]: st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.write("➔ Standard-Setup aktiv. Alle Komponenten für maximale Zuverlässigkeit gewählt.")
