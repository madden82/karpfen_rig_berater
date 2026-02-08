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
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"],
                                help="Bestimmt die grundlegende Montage und Strömungsgefahr.")
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"],
                                    help="Beeinflusst Bleigewicht und Krallenform.")
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5, step=0.1, help="Die Tiefe am exakten Ablegeplatz.")
    angeltag = st.date_input("Wann fischst du?", datetime.date.today(), help="Berechnet die Mondphase für dieses Datum.")

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"], help="Einfluss auf Fischaktivität und Tiefe.")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15, help="Direkter Einfluss auf den Stoffwechsel.")
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], 
                                 index=0, help="Entscheidet über Bleiform und Vorfachlänge.")
    zeitfenster = st.multiselect("Wann planst du zu fischen?", 
                                 ["Vormittag", "Nachmittag", "Abend", "Nacht"],
                                 default=["Vormittag"],
                                 help="Beeinflusst Lichtverhältnisse, Sauerstoff und Fischzugrouten.")

with c3:
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], 
                                default=None, placeholder="Hier auswählen...",
                                help="Bestimmt Hakenstärke und Montagensystem.")
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", 
                                  options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], 
                                  value="Weiß ich nicht",
                                  help="Entscheidend für Ködergröße und Härte gegen Beifänge (Brassen/Krebse).")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    boots_taktik = "Normal"
    if ausbringung == "Boot":
        boots_taktik = st.selectbox("Vorgehen vom Boot", ["Nur Ablegen", "Vom Boot auswerfen"], help="Wichtig für Bleigewicht und Präzision.")
    
    ziel_gewicht = st.number_input("Max. erwartetes Gewicht (kg)", 5, 40, 15, help="Wichtig für die Wahl der Haken-Drahtstärke.")
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"], help="Beeinflusst Tarnung (Fluorocarbon) und Vorfach.")
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (KORRIGIERT)
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
        "koeder_empfehlung": "", 
        "koeder_haerte": "Normal", 
        "koeder_groesse": "20mm",
        "futter_menge": "Moderat (ca. 500g - 1kg)", 
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], 
        "spot_analyse_text": "",
        "spot_empfehlungen": [], 
        "unsicher": False
    }

    # --- HAKEN-GRÖSSE ---
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 20: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # --- WEISSFISCH- & KÖDER-LOGIK ---
    if weissfisch in ["Hoch", "Extrem"]:
        s["koeder_haerte"] = "Gepökelt / Extra Hart"
        s["koeder_groesse"] = "24mm+ oder Doppel-20mm"
        s["koeder_empfehlung"] = "Harte Fisch-Boilies oder Tigernüsse."
        s["begruendungen"].append("➔ **Weißfisch-Abwehr:** Bei hohem Druck sind Tigernüsse oder extra harte Boilies nötig, um Beifänge zu minimieren.")
    elif weissfisch == "Niedrig":
        s["koeder_groesse"] = "15-18mm / Single Bait"
        s["koeder_empfehlung"] = "Süße Boilies oder auffällige Pop-Ups (Instant-Wirkung)."
    else:
        s["koeder_empfehlung"] = "Standard 20mm Boilie mit PVA-Stick."

    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)", "-- Bitte wählen --", "Weiß ich nicht"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append("➔ **Heli-Safe:** Verhindert das Einsinken des Köders im weichen Boden oder Kraut.")
    
    # --- TAGESZEITEN-LOGIK ---
    if "Nacht" in zeitfenster:
        s["spot_empfehlungen"].append("📍 Nachts: Ziehe eine Rute extrem flach (bis 1m) direkt ans Ufer.")
        if "Kraut" in hindernisse:
            s["begruendungen"].append("⚠️ **Sauerstoff (Nacht):** Krautfelder nachts eher von außen befischen (O2-Mangel nachts im Kraut).")
    
    if any(z in zeitfenster for z in ["Vormittag", "Nachmittag"]):
        if aktivitaet in ["Vorsichtig", "Apathisch"]:
            s["vorfach_material"] = "Fluorocarbon (Vollmaterial)"
            s["begruendungen"].append("➔ **Tarnung:** Bei Tageslicht und vorsichtigen Fischen sorgt Fluorocarbon für maximale Unsichtbarkeit.")

    # --- BOOTS- & STRÖMUNGS-LOGIK ---
    if ausbringung == "Boot":
        s["blei_gewicht"] = 140 if boots_taktik == "Nur Ablegen" else 110
        s["begruendungen"].append(f"➔ **Boot-Taktik ({boots_taktik}):** Bleigewicht optimiert für sauberes Straffen der Schnur.")
            
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 170 if stroemung == "Stark" else 140

    # --- HAKEN-MECHANIK ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
    if any(h in hindernisse for h in ["Muschelbänke", "Scharfe Kanten"]):
        s["h_draht"] = "X-Strong (Dickdrähtig)"
        s["begruendungen"].append("➔ **X-Strong Haken:** Erhöhte Stabilität für harte Drills an Hindernissen.")

    # --- SPOT-ANALYSE ---
    if jahreszeit == "Frühjahr":
        if tiefe_spot < 2.0: s["spot_analyse_text"] = "Hervorragender Spot! Flachzonen sind im Frühjahr die Futterkammern."
        else: s["spot_empfehlungen"].append("📍 Frühjahrstipp: Suche Plateaus unter 2m Tiefe.")
    
    return s

# Logik ausführen
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
    # Alle Haken-Spezifikationen direkt hier integriert (Tabelle entfernt)
    st.warning(f"**Modell:** {ergebnis['haken_typ']}")
    st.warning(f"**Größe:** {ergebnis['h_groesse']}")
    st.warning(f"**Drahtstärke:** {ergebnis['h_draht']}")
    st.warning(f"**Öhr-Stellung:** {ergebnis['h_oehr']}")
    st.warning(f"**Haken-Spitze:** {ergebnis['h_spitze']}")

# --- NEU: KÖDER-TAKTIK (BASIEREND AUF WEISSFISCH-DRUCK) ---
st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k_c1, k_c2 = st.columns(2)

with k_c1:
    st.write("**Köder-Konfiguration:**")
    st.write(f"➔ Empfehlung: **{ergebnis['koeder_empfehlung']}**")
    st.write(f"➔ Größe: {ergebnis['koeder_groesse']}")
    st.write(f"➔ Härte: {ergebnis['koeder_haerte']}")

with k_c2:
    st.write("**Fütterung:**")
    st.write(f"➔ Menge: {ergebnis['futter_menge']}")
    st.write(f"➔ Art: {ergebnis['futter_art']}")

# --- ERWEITERTE SPOT-ANALYSE ---
st.markdown('<div class="section-header">🔍 4. Detaillierte Spot-Analyse</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    st.markdown(f'<div class="spot-empfehlung"><strong>Status deines Spots:</strong><br>{ergebnis["spot_analyse_text"] if ergebnis["spot_analyse_text"] else "Die Tiefe ist für das gewählte Zeitfenster plausibel."}</div>', unsafe_allow_html=True)

with sa2:
    st.write("**Konkrete Spot-Vorschläge:**")
    if ergebnis["spot_empfehlungen"]:
        for empf in ergebnis["spot_empfehlungen"]:
            st.write(empf)
    else:
        st.write("➔ Suche nach markanten Strukturveränderungen am Grund.")

# --- BEGRÜNDUNGEN ---
st.markdown('<div class="section-header">📖 Warum dieses Setup?</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="taktik-detail">➔ Standard-Setup aktiv. Keine speziellen Anpassungen erforderlich.</div>', unsafe_allow_html=True)

if boden_struktur == "-- Bitte wählen --":
    st.warning("⚠️ Hinweis: Bitte wähle noch die Bodenbeschaffenheit aus, um das Rig zu optimieren!")
# ==========================================
# 5. NATUR-FAKTOREN (DYNAMISCH & ZEITBEZOGEN)
# ==========================================

def get_moon_phase(date_obj):
    # Berechnung der Mondphase für das gewählte Datum
    diff = date_obj - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Perfekt für flache Spots! Maximale Dunkelheit macht Fische unvorsichtig."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen, besonders in den Abendstunden."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten zu erwarten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Fressaktivität steigt oft spürbar an."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Extreme Sichtbarkeit! Nachts Tarnung und Schattenwurf am Ufer beachten."
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt meist leicht nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Fische ziehen oft in tiefere, dunklere Bereiche."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor dem nächsten Neumond."

# Berechnung basierend auf der Eingabe aus Teil 1
mond_name, mond_tipp = get_moon_phase(angeltag)

st.markdown('<div class="section-header">🌙 5. Natur-Faktoren für den ' + angeltag.strftime('%d.%m.%Y') + '</div>', unsafe_allow_html=True)
m_c1, m_c2 = st.columns(2)

with m_c1:
    st.metric("Voraussichtliche Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

with m_c2:
    st.write("**Zeitfenster-Analyse:**")
    # Dynamische Tipps basierend auf gewählten Zeiten & Mond
    if "Nacht" in zeitfenster and "Vollmond" in mond_name:
        st.warning("🌔 Vollmond-Nacht: Meide extrem flache Uferbereiche ohne Deckung (Schattenwurf!).")
    elif "Nacht" in zeitfenster and "Neumond" in mond_name:
        st.success("🌑 Neumond-Nacht: Ideal für flaches Angeln direkt an der Uferkante.")
    
    # Thermischer Check basierend auf der Slider-Eingabe (temp)
    if 14 <= temp <= 20:
        st.success("✅ Wassertemperatur ideal für hohe Futteraufnahme.")
    elif temp > 22:
        st.warning("⚠️ Warmwasser: Beißphasen verlagern sich oft in die kühleren Morgenstunden.")
    else:
        st.write("➔ Stoffwechsel verlangsamt: Attraktive Einzelköder bevorzugen.")

# Abschlusszeile für die Web-App
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Datumsfokus: {angeltag.strftime('%d.%m.%Y')} | Mobil-Optimiert für Python & Streamlit Cloud")
