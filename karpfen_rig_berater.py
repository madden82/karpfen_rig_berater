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
    if month in [3, 4, 5]: jahreszeit = "Frühjahr"
    elif month in [6, 7, 8]: jahreszeit = "Sommer"
    elif month in [9, 10, 11]: jahreszeit = "Herbst"
    else: jahreszeit = "Winter"
    
    st.write(f"**Erkannte Jahreszeit:** {jahreszeit}")
    
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15,
                     help="Direkter Einfluss auf den Stoffwechsel und die benötigte Futtermenge.")
    luftdruck = st.number_input("Luftdruck (hPa)", 950, 1050, 1013,
                                help="1013 hPa ist der Standard. Fallender Druck ist oft ein Beiß-Signal.")
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"],
                                 help="Fallender Druck deutet oft auf fressende Fische hin.")

with c3:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], 
                                 index=0, help="Entscheidet über Bleiform (Einsinken) und Vorfachlänge.")
    
    zeitfenster = st.multiselect("Wann planst du zu fischen?", 
                                 ["Vormittag", "Nachmittag", "Abend", "Nacht"], 
                                 placeholder="-- Bitte wählen --",
                                 help="Beeinflusst Lichtverhältnisse, Sauerstoff und Fischzugrouten.")
    
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], 
                                placeholder="-- Bitte wählen --",
                                help="Bestimmt das Montagensystem und die Hakenstabilität.")
    
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
        wurfweite = st.slider("Wurfweite (m)", 0, 180, 60, help="Beeinflusst Bleiform und Gewicht.")
    
    ziel_gewicht = st.number_input("Max. Karpfengewicht (kg)", 5, 40, 15, help="Wichtig für Hakenstärke.")
    aktivitaet = st.select_slider("Fischverhalten", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"], value="Normal")

# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE
# ==========================================
def berechne_pro_logic():
    s = {
        "blei_typ": "Safety-Clip Montage", "blei_form": "Birnenform (Smooth)", "blei_gewicht": 90,
        "rig_typ": "Standard Haar-Rig", "koeder_praesentation": "Bodenköder",
        "vorfach_material": "Ummanteltes Geflecht (Coated Braid)", "vorfach_laenge": "15-20 cm",
        "leader": "Standard Leadcore / Anti-Tangle-Tube", "haken_typ": "Wide Gape",
        "h_spitze": "Straight Point", "h_oehr": "Gerade", "h_draht": "Standard", "h_groesse": 6,
        "koeder_empfehlung": "Standard 20mm Boilie", "koeder_haerte": "Normal", "koeder_groesse": "20mm",
        "futter_menge": "Moderat (ca. 500g - 1kg)", "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], "spot_empfehlungen": [], "unsicher": False
    }

    if boden_struktur == "-- Bitte wählen --" or not zeitfenster or not hindernisse: s["unsicher"] = True

    # Haken-Größe
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 22: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # Luftdruck
    if druck_tendenz == "Fallend":
        s["futter_menge"] = "Aggressiv (ca. 1.5kg - 3kg)"
        s["begruendungen"].append("➔ **Luftdruck-Bonus:** Fallender Druck steigert den Stoffwechsel. Futtermenge erhöhen!")
    elif druck_tendenz == "Steigend" or luftdruck > 1025:
        s["futter_menge"] = "Minimal (PVA-Stick / Single)"
        s["koeder_empfehlung"] = "Hochattraktiver Single-Bait (Pop-Up)"

    # Wurf/Boot
    if ausbringung == "Wurf vom Ufer" and wurfweite > 100:
        s["blei_gewicht"] = 120; s["blei_form"] = "Distanz-Blei (Zip/Torpedo)"
    elif ausbringung == "Boot":
        s["blei_gewicht"] = 140 if boots_taktik == "Nur Ablegen" else 110

    # Weißfisch
    if weissfisch in ["Hoch", "Extrem"]:
        s["koeder_haerte"] = "Extra Hart / Gepökelt"; s["koeder_groesse"] = "24mm oder Doppel-20mm"
        s["koeder_empfehlung"] = "Harte Fisch-Boilies oder Tigernüsse."

    # Boden/Hindernisse
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"; s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"; s["vorfach_laenge"] = "25-35 cm"
    
    if any(h in hindernisse for h in ["Muschelbänke", "Scharfe Kanten"]):
        s["h_draht"] = "X-Strong (Dickdrähtig)"
        s["leader"] = "Dickes Mono / Schlagschnur + Leadcore"

    if aktivitaet in ["Vorsichtig", "Apathisch"]:
        s["vorfach_material"] = "Fluorocarbon (Unsichtbar)"

    if jahreszeit == "Winter":
        s["spot_empfehlungen"].append(f"📍 Winter-Tipp: Suche die tiefsten Stellen (ca. {tiefe_max}m) auf.")

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
    st.info(f"**System:** {ergebnis['blei_typ']}\n\n**Blei:** {ergebnis['blei_form']} ({ergebnis['blei_gewicht']}g)")

with res_c2:
    st.subheader("🧶 Rig & Vorfach")
    st.success(f"**Rig:** {ergebnis['rig_typ']}\n\n**Material:** {ergebnis['vorfach_material']}\n\n**Länge:** {ergebnis['vorfach_laenge']}")

with res_c3:
    st.subheader("🪝 Haken-Setup")
    st.warning(f"**Haken:** {ergebnis['haken_typ']} (Gr. {ergebnis['h_groesse']})\n\n**Draht:** {ergebnis['h_draht']}\n\n**Öhr:** {ergebnis['h_oehr']}")

st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k_c1, k_c2 = st.columns(2)
with k_c1:
    st.write(f"**Köder:** {ergebnis['koeder_empfehlung']}\n\n**Größe:** {ergebnis['koeder_groesse']} | **Härte:** {ergebnis['koeder_haerte']}")
with k_c2:
    st.write(f"**Futtermenge:** {ergebnis['futter_menge']}\n\n**Futterart:** {ergebnis['futter_art']}")

st.markdown('<div class="section-header">🔍 4. Spot-Analyse & Natur-Physik</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)
with sa1:
    st.markdown(f'<div class="spot-empfehlung">Tiefe: {tiefe_spot}m | Zeit: {", ".join(zeitfenster)}</div>', unsafe_allow_html=True)
    if luftdruck > 1022: st.warning("⚖️ **Hoher Luftdruck:** Teste ein **ZIG-Rig** (Mittelwasser)!")
with sa2:
    for empf in ergebnis["spot_empfehlungen"]: st.write(empf)
    if ausbringung == "Boot": st.write("➔ **Profi-Tipp:** Nutze Backleads zum Absenken der Schnur am Boot.")

def get_moon(d):
    diff = d - datetime.date(2001, 1, 1); days = diff.days; lun = 29.530588853; pos = (days / lun) % 1
    if pos < 0.06: return "🌑 Neumond", "Top-Zeit! Maximale Dunkelheit."
    elif pos < 0.55 and pos > 0.45: return "🌕 Vollmond", "Vorsicht: Hohe Sichtbarkeit nachts!"
    return "🌓 Sichel/Halbmond", "Normale Bedingungen."

mond_n, mond_t = get_moon(angeltag)
st.markdown(f'<div class="taktik-detail">🌙 **Mondphase für {angeltag.strftime("%d.%m.%Y")}:** {mond_n} - {mond_t}</div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📖 Experten-Logik (Begründungen)</div>', unsafe_allow_html=True)
for b in ergebnis["begruendungen"]: st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
if ergebnis["unsicher"]: st.warning("⚠️ Hinweis: Auswahl unvollständig. Sicherheits-Setup aktiv.")
