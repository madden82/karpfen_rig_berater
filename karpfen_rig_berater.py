import streamlit as st
import datetime

# ==========================================
# 1. SETUP & DESIGN
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
# 2. EINGABEMASKE: GEWÄSSER & UMWELT
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
    # JAHRESZEIT AUTOMATIK (Berechnung für die Logik)
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
    
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", options=["Niedrig", "Mittel", "Hoch", "Extrem"], value="Mittel")
    
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    # DYNAMISCHE UNTERAUSWAHLEN
    boots_taktik = "Normal"
    wurfweite = 0
    if ausbringung == "Boot":
        boots_taktik = st.selectbox("Vorgehen vom Boot", ["Nur Ablegen", "Vom Boot auswerfen"])
    elif ausbringung == "Wurf vom Ufer":
        wurfweite = st.slider("Benötigte Wurfweite (m)", 0, 180, 60)
    
    ziel_gewicht = st.number_input("Max. erwartetes Gewicht (kg)", 5, 40, 15)
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"], value="Normal")
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

    # --- LUFTDRUCK-LOGIK ---
    if druck_tendenz == "Fallend":
        s["futter_menge"] = "Aggressiv (ca. 1.5kg - 3kg)"
        s["begruendungen"].append("➔ **Luftdruck-Bonus:** Fallender Druck steigert den Stoffwechsel. Erhöhe die Futtermenge!")
    elif druck_tendenz == "Steigend" or luftdruck > 1025:
        s["futter_menge"] = "Minimal (PVA-Stick / Single)"
        s["koeder_empfehlung"] = "Hochattraktiver Single-Bait (Pop-Up)"
        s["begruendungen"].append("➔ **Hochdruck-Taktik:** Fische stehen oft passiv. Wenig Futter, Reizköder nutzen.")

    # --- WURFWEITE & BOOT-LOGIK ---
    if ausbringung == "Wurf vom Ufer":
        if wurfweite > 100:
            s["blei_gewicht"] = 120
            s["blei_form"] = "Distanz-Blei (Zip/Torpedo)"
            s["begruendungen"].append(f"➔ **Distanz-Wurf ({wurfweite}m):** Aerodynamisches Blei nötig.")
    elif ausbringung == "Boot":
        if boots_taktik == "Nur Ablegen":
            s["blei_gewicht"] = 140
            s["begruendungen"].append("➔ **Boot-Ablegen:** Schweres Blei verhindert das Verrutschen beim Straffen.")
        else:
            s["blei_gewicht"] = 110

    # --- JAHRESZEIT-LOGIK (vom Datum) ---
    if jahreszeit == "Winter":
        s["futter_art"] = "Low-Oil Pellets & Groundbait"
        s["spot_empfehlungen"].append(f"📍 Winter-Check: Suche die tiefsten Stellen (ca. {tiefe_max}m) auf.")
    
    # --- WEISSFISCH-LOGIK ---
    if weissfisch in ["Hoch", "Extrem"]:
        s["koeder_haerte"] = "Extra Hart / Gepökelt"
        s["koeder_groesse"] = "24mm oder Doppel-20mm"
        s["koeder_empfehlung"] = "Harte Fisch-Boilies oder Tigernüsse."

    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)", "-- Bitte wählen --"] or (hindernisse and "Kraut" in hindernisse):
        s["blei_typ"] = "Heli-Safe System"; s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"; s["vorfach_laenge"] = "25-35 cm"

    # --- HAKEN-MECHANIK ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"; s["h_oehr"] = "Nach innen gebogen"

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
    if ausbringung == "Wurf vom Ufer":
        st.info(f"**Wurf-Setup:** {wurfweite}m Distanz")

with res_c2:
    st.subheader("🧶 Vorfach & Rig")
    st.success(f"**Rig-Typ:** {ergebnis['rig_typ']}")
    st.success(f"**Material:** {ergebnis['vorfach_material']}")
    st.success(f"**Länge:** {ergebnis['vorfach_laenge']}")
    st.success(f"**Präsentation:** {ergebnis['koeder_praesentation']}")

with res_c3:
    st.subheader("🪝 Haken-Setup")
    st.warning(f"**Modell:** {ergebnis['haken_typ']}")
    st.warning(f"**Größe:** {ergebnis['h_groesse']}")
    st.warning(f"**Draht:** {ergebnis['h_draht']}")
    st.warning(f"**Öhr:** {ergebnis['h_oehr']}")

# --- KÖDER- & FUTTERSTRATEGIE ---
st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k_c1, k_c2 = st.columns(2)

with k_c1:
    st.write("**Köder-Setup:**")
    st.write(f"➔ Empfehlung: **{ergebnis['koeder_empfehlung']}**")
    st.write(f"➔ Größe: {ergebnis['koeder_groesse']}")
    st.write(f"➔ Härte: {ergebnis['koeder_haerte']}")

with k_c2:
    st.write("**Futter-Taktik:**")
    st.write(f"➔ Menge: {ergebnis['futter_menge']}")
    st.write(f"➔ Art: {ergebnis['futter_art']}")

# --- ERWEITERTE SPOT-ANALYSE ---
st.markdown('<div class="section-header">🔍 4. Detaillierte Spot-Analyse & Boots-Tipps</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    zeit_info = ", ".join(zeitfenster) if zeitfenster else "keine Zeit gewählt"
    st.markdown(f"""
        <div class="spot-empfehlung">
            <strong>Spot-Umgebung:</strong><br>
            Tiefe: {tiefe_spot}m (Max: {tiefe_max}m)<br>
            Phase: {jahreszeit} | Zeit: {zeit_info}
        </div>
    """, unsafe_allow_html=True)
    
    if ausbringung == "Boot":
        st.write("**Profi-Tipp für Boot:**")
        st.write(f"➔ Modus: {boots_taktik}")
        st.write("➔ Schnur absenken (Backleads) gegen Boote/Wasservögel.")

with sa2:
    st.write("**Konkrete Spot-Vorschläge:**")
    if ergebnis["spot_empfehlungen"]:
        for empf in ergebnis["spot_empfehlungen"]:
            st.write(empf)
    else:
        st.write(f"➔ Suche markante Strukturen bei {tiefe_spot}m Tiefe.")

# --- BEGRÜNDUNGEN ---
st.markdown('<div class="section-header">📖 Experten-Logik</div>', unsafe_allow_html=True)
for b in ergebnis["begruendungen"]:
    st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
# ==========================================
# 5. NATUR-FAKTOREN (MOND, DRUCK & PHYSIK)
# ==========================================

def get_moon_phase(date_obj):
    # Mondphasen-Berechnung
    diff = date_obj - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Maximale Dunkelheit: Fische ziehen extrem flach."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Fressaktivität steigt oft an."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Extreme Sichtbarkeit! Vorsicht vor Schattenwurf."
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt meist nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Fische oft tiefer stehend."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor Neumond."

# Berechnung für das gewählte Datum
mond_name, mond_tipp = get_moon_phase(angeltag)

st.markdown('<div class="section-header">🌙 5. Natur-Faktoren & Physik am Spot</div>', unsafe_allow_html=True)
m_c1, m_c2 = st.columns(2)

with m_c1:
    st.metric("Voraussichtliche Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

with m_c2:
    st.write("**Physik am Spot (Taktik):**")
    
    # 1. Luftdruck-Physik (ZIG-Rig Logik)
    if luftdruck > 1022:
        st.warning("⚖️ **Hoher Luftdruck:** Fische stehen oft im Mittelwasser. Teste ein **ZIG-Rig** (Pop-Up in halber Wassertiefe)!")
    elif druck_tendenz == "Fallend":
        st.success("🔥 **Druckabfall:** Die Fische suchen am Grund nach Nahrung. Bleib bei Bodenködern!")
    
    # 2. Mondlicht & Tarnung
    if "🌕 Vollmond" in mond_name and any(z in zeitfenster for z in ["Abend", "Nacht"]):
        st.warning("🌕 **Lichtbrechung:** Meide flache Zonen ohne Deckung. Nutze Fluorocarbon als Leader.")
    elif "🌑 Neumond" in mond_name:
        st.success("🌑 **Dunkelphasen-Vorteil:** Die Fische trauen sich nachts extrem nah an die Uferkante.")

    # 3. Thermik-Check
    if 14 <= temp <= 20:
        st.success("✅ Wassertemperatur ideal für volle Futteraufnahme.")
    else:
        st.info("➔ Stoffwechsel-Hinweis: Futtermenge an Beißintensität anpassen.")

# Abschlusszeile der App
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Datumsfokus: {angeltag.strftime('%d.%m.%Y')} | Automatik-Modus: {jahreszeit} | Petri Heil!")
