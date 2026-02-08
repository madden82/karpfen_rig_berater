import streamlit as st
import datetime

# ==========================================
# SETUP & MOBIL-OPTIMIERTES DESIGN
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

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik Pro (Mobil)</div>', unsafe_allow_html=True)

# ==========================================
# EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässer & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0)
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5)
    angeltag = st.date_input("Wann fischst du?", datetime.date.today())

with c2:
    # JAHRESZEIT AUTOMATIK
    month = angeltag.month
    if month in [3, 4, 5]: jahreszeit = "Frühjahr"
    elif month in [6, 7, 8]: jahreszeit = "Sommer"
    elif month in [9, 10, 11]: jahreszeit = "Herbst"
    else: jahreszeit = "Winter"
    
    st.write(f"**Erkannte Jahreszeit:** {jahreszeit}")
    
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    luftdruck = st.number_input("Luftdruck (hPa)", 950, 1050, 1013)
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"])

with c3:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=0)
    zeitfenster = st.multiselect("Wann planst du zu fischen?", 
                                 ["Vormittag", "Nachmittag", "Abend", "Nacht"], placeholder="-- Bitte wählen --")
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], placeholder="-- Bitte wählen --")
    
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (DYNAMISCH)
# ==========================================

def berechne_pro_logic():
    # Initialisierung des Ergebnis-Objekts
    s = {
        "blei_typ": "Safety-Clip Montage", 
        "blei_form": "Birnenform (Smooth)", 
        "blei_gewicht": 90,
        "rig_typ": "Standard Haar-Rig", 
        "koeder_praesentation": "Bodenköder",
        "vorfach_material": "Ummanteltes Geflecht (Coated Braid)", 
        "vorfach_laenge": "15-20 cm",
        "leader": "Standard Leadcore / Anti-Tangle-Tube", 
        "haken_typ": "Wide Gape",
        "h_spitze": "Straight Point",
        "h_oehr": "Gerade", 
        "h_draht": "Standard", 
        "h_groesse": 6,
        "koeder_empfehlung": "Standard 20mm Boilie", 
        "koeder_haerte": "Normal", 
        "koeder_groesse": "20mm",
        "futter_menge": "Moderat (ca. 500g - 1kg)", 
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], 
        "spot_empfehlungen": [], 
        "unsicher": False
    }

    # --- LUFTDRUCK-LOGIK (Beißintensität & Futter) ---
    if druck_tendenz == "Fallend":
        s["futter_menge"] = "Aggressiv (ca. 1.5kg - 3kg)"
        s["begruendungen"].append("➔ **Luftdruck-Bonus:** Fallender Druck steigert den Stoffwechsel. Du kannst jetzt mehr füttern, um die Fische am Platz zu halten.")
    elif druck_tendenz == "Steigend" or luftdruck > 1025:
        s["futter_menge"] = "Minimal (nur eine Handvoll)"
        s["koeder_empfehlung"] = "Hochattraktiver Single-Bait (Pop-Up)"
        s["begruendungen"].append("➔ **Hochdruck-Taktik:** Bei steigendem/hohem Druck stehen Fische oft im Mittelwasser. Wenig Futter, aber hochattraktive Köder nutzen.")

    # --- JAHRESZEIT-LOGIK (Basierend auf Datum) ---
    if jahreszeit == "Winter":
        s["futter_art"] = "Low-Oil Pellets & Groundbait"
        s["futter_menge"] = "Sehr wenig (PVA-Stick)"
        s["spot_empfehlungen"].append(f"📍 Winter-Check: Suche die tiefsten Stellen (ca. {tiefe_max}m) auf.")
    elif jahreszeit == "Frühjahr":
        if tiefe_spot < 2.5:
            s["begruendungen"].append("➔ **Frühjahrs-Sonne:** Dein flacher Spot ist ideal, da sich das Wasser hier zuerst erwärmt.")

    # --- WEISSFISCH- & KÖDER-LOGIK ---
    if weissfisch in ["Hoch", "Extrem"]:
        s["koeder_haerte"] = "Extra Hart / Gepökelt"
        s["koeder_groesse"] = "24mm oder Doppel-20mm"
        s["koeder_empfehlung"] = "Harte Fisch-Boilies oder Tigernüsse."
    
    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)", "-- Bitte wählen --"] or (hindernisse and "Kraut" in hindernisse):
        s["blei_typ"] = "Heli-Safe System"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
    
    # --- BOOTS- & STRÖMUNGS-LOGIK ---
    if ausbringung == "Boot":
        s["blei_gewicht"] = 140
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 170 if stroemung == "Stark" else 140

    # --- HAKEN-MECHANIK ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"

    return s

# Berechnung ausführen
ergebnis = berechne_pro_logic()
# ==========================================
# 4. AUSGABE: RESULTATE & TAKTIK
# ==========================================

# Trennung zur Eingabemaske
st.markdown("---")
st.markdown('<div class="section-header">🛡️ 2. Deine optimierte Taktik-Empfehlung</div>', unsafe_allow_html=True)

# Layout für die Haupt-Ergebnisse (Mobil-Optimiert)
res_c1, res_c2, res_c3 = st.columns(3)

with res_c1:
    st.subheader("🎣 Montage & Blei")
    st.info(f"**System:** {ergebnis['blei_typ']}")
    st.info(f"**Bleiform:** {ergebnis['blei_form']}")
    st.info(f"**Gewicht:** {ergebnis['blei_gewicht']}g")
    st.info(f"**Leader:** {ergebnis['leader']}")

with res_c2:
    st.subheader("🧶 Vorfach & Rig")
    st.success(f"**Rig-Typ:** {ergebnis['rig_typ']}")
    st.success(f"**Material:** {ergebnis['vorfach_material']}")
    st.success(f"**Länge:** {ergebnis['vorfach_laenge']}")
    st.success(f"**Präsentation:** {ergebnis['koeder_praesentation']}")

with res_c3:
    st.subheader("🪝 Haken-Setup")
    # Alle Haken-Spezifikationen direkt hier integriert
    st.warning(f"**Modell:** {ergebnis['haken_typ']} (Gr. {ergebnis['h_groesse']})")
    st.warning(f"**Drahtstärke:** {ergebnis['h_draht']}")
    st.warning(f"**Öhr-Stellung:** {ergebnis['h_oehr']}")
    st.warning(f"**Haken-Spitze:** {ergebnis['h_spitze']}")

# --- KÖDER- & FUTTERSTRATEGIE (Luftdruck-abhängig) ---
st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k_c1, k_c2 = st.columns(2)

with k_c1:
    st.write("**Köder-Konfiguration:**")
    st.write(f"➔ Empfehlung: **{ergebnis['koeder_empfehlung']}**")
    st.write(f"➔ Größe: {ergebnis['koeder_groesse']}")
    st.write(f"➔ Härte: {ergebnis['koeder_haerte']}")

with k_c2:
    st.write("**Fütterung (Luftdruck-optimiert):**")
    st.write(f"➔ Menge: {ergebnis['futter_menge']}")
    st.write(f"➔ Art: {ergebnis['futter_art']}")

# --- ERWEITERTE SPOT-ANALYSE ---
st.markdown('<div class="section-header">🔍 4. Detaillierte Spot-Analyse</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    # Analyse basierend auf Luftdruck und Zeitfenster
    zeit_info = ", ".join(zeitfenster) if zeitfenster else "keine Angabe"
    st.markdown(f"""
        <div class="spot-empfehlung">
            <strong>Physik-Check:</strong><br>
            Jahreszeit: {jahreszeit}<br>
            Luftdruck: {luftdruck} hPa ({druck_tendenz})<br>
            Zeitfenster: {zeit_info}
        </div>
    """, unsafe_allow_html=True)

with sa2:
    st.write("**Konkrete Spot-Vorschläge:**")
    if ergebnis["spot_empfehlungen"]:
        for empf in ergebnis["spot_empfehlungen"]:
            st.write(empf)
    else:
        st.write(f"➔ Bei {jahreszeit} und {luftdruck}hPa: Achte auf Kanten in der Nähe von {tiefe_max/2}m Tiefe.")

# --- BEGRÜNDUNGEN ---
st.markdown('<div class="section-header">📖 Experten-Logik</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="taktik-detail">➔ Standard-Setup aktiv. Wähle mehr Kriterien für tiefere Analysen.</div>', unsafe_allow_html=True)
# ==========================================
# 5. NATUR-FAKTOREN (MOND & LICHT-PHYSIK)
# ==========================================

def get_moon_phase(date_obj):
    # Berechnung der Mondphase für das gewählte Datum
    diff = date_obj - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Maximale Dunkelheit: Fische ziehen extrem flach und unvorsichtig."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen, wenig Streulicht."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Lichtintensität nimmt zu."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Hohe Lichtintensität! Vorsicht vor Schattenwurf und sichtbaren Schnüren."
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt meist leicht nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Fische oft tiefer stehend."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor Neumond."

# Berechnung basierend auf dem Datum aus Teil 1
mond_name, mond_tipp = get_moon_phase(angeltag)

st.markdown('<div class="section-header">🌙 5. Natur-Faktoren für den ' + angeltag.strftime('%d.%m.%Y') + '</div>', unsafe_allow_html=True)
m_c1, m_c2 = st.columns(2)

with m_c1:
    st.metric("Voraussichtliche Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

with m_c2:
    st.write("**Physik am Spot:**")
    # Logik zur Lichtbrechung und Sichtbarkeit
    if "🌕 Vollmond" in mond_name:
        st.warning("⚠️ **Lichtbrechung:** Bei Vollmond dringen Lichtstrahlen tief ein. Deine Hauptschnur wirft einen scharfen Schatten am Grund. Nutze Backleads oder Fluorocarbon.")
    elif "🌑 Neumond" in mond_name:
        st.success("🌑 **Tarnung:** Dunkelheit schützt! Du kannst jetzt auch mit gröberen Montagen in flachem Wasser Erfolg haben.")
    
    # Ergänzender Beiß-Check
    if druck_tendenz == "Fallend":
        st.success("🔥 Beißfenster: Geöffnet durch fallenden Luftdruck!")
    elif luftdruck > 1025:
        st.info("ℹ️ Beißfenster: Zäh durch hohen Luftdruck. Kleine Köder nutzen.")

# Abschlusszeile für die Web-App am Handy
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Automatik-Modus: {jahreszeit} | Luftdruck: {luftdruck}hPa | Petri Heil!")
