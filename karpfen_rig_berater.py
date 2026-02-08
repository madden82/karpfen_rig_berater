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
    angeltag = st.date_input("Wann fischst du?", datetime.date.today(), help="Berechnet die Mondphase.")

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"], help="Einfluss auf Aktivität.")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    
    # NEU: Neutraler Start für Bodenbeschaffenheit
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], 
                                 index=0)
    
    # NEU: Zeitfenster jetzt als Selectbox für den neutralen Start, danach Mehrfachauswahl möglich
    zeitfenster = st.multiselect("Wann planst du zu fischen?", 
                                 ["Vormittag", "Nachmittag", "Abend", "Nacht"],
                                 default=None, placeholder="-- Bitte wählen --")

with c3:
    # NEU: Neutraler Start für Hindernisse
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], 
                                default=None, placeholder="-- Bitte wählen --")
    
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", 
                                  options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], value="Weiß ich nicht")
    
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    if ausbringung == "Boot":
        boots_taktik = st.selectbox("Vorgehen vom Boot", ["Nur Ablegen", "Vom Boot auswerfen"])
    
    ziel_gewicht = st.number_input("Max. erwartetes Gewicht (kg)", 5, 40, 15)
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (ROBUST)
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
        "spot_analyse_text": "",
        "spot_empfehlungen": [], 
        "unsicher": False
    }

    # Sicherheits-Check: Falls nichts gewählt wurde
    auswahl_fehlt = (boden_struktur == "-- Bitte wählen --" or not zeitfenster or not hindernisse)
    if auswahl_fehlt:
        s["unsicher"] = True

    # --- HAKEN-GRÖSSE ---
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 20: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # --- WEISSFISCH- & KÖDER-LOGIK ---
    if weissfisch in ["Hoch", "Extrem"]:
        s["koeder_haerte"] = "Extra Hart (Gepökelt)"
        s["koeder_groesse"] = "24mm oder Doppel-20mm"
        s["koeder_empfehlung"] = "Harte Fisch-Boilies oder Tigernüsse (resistent)."
        s["begruendungen"].append("➔ **Weißfisch-Abwehr:** Bei hohem Druck schützen harte Köder vor unerwünschten Beifängen.")
    elif weissfisch == "Niedrig":
        s["koeder_groesse"] = "15-18mm"
        s["koeder_empfehlung"] = "Süße Boilies oder auffällige Pop-Ups."

    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"] or (hindernisse and "Kraut" in hindernisse):
        s["blei_typ"] = "Heli-Safe System"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append("➔ **Heli-Safe:** Bestes System für weichen Boden/Kraut, um eine perfekte Köderpräsentation zu garantieren.")
    
    # --- TAGESZEITEN-LOGIK ---
    if zeitfenster:
        if "Nacht" in zeitfenster:
            s["spot_empfehlungen"].append("📍 Nachts: Eine Rute extrem flach (bis 1m) ans Ufer legen.")
            if hindernisse and "Kraut" in hindernisse:
                s["begruendungen"].append("⚠️ **Nacht-Sauerstoff:** Im dichten Kraut sinkt nachts der O2-Gehalt. Befische eher die Kanten.")
        
        if any(z in zeitfenster for z in ["Vormittag", "Nachmittag"]):
            if aktivitaet in ["Vorsichtig", "Apathisch"]:
                s["vorfach_material"] = "Fluorocarbon (Tarnung)"
                s["begruendungen"].append("➔ **Tarnung:** Bei Tageslicht erhöht Fluorocarbon die Chance auf einen Biss vorsichtiger Fische.")

    # --- BOOTS- & AUSBRINGUNGS-LOGIK ---
    if ausbringung == "Boot":
        s["blei_gewicht"] = 140 if boots_taktik == "Nur Ablegen" else 110
            
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 170 if stroemung == "Stark" else 140

    # --- HAKEN-MECHANIK ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
    if hindernisse and any(h in hindernisse for h in ["Muschelbänke", "Scharfe Kanten"]):
        s["h_draht"] = "X-Strong (Dickdrähtig)"
        s["begruendungen"].append("➔ **Haken-Stabilität:** X-Strong Haken verhindern das Aufbiegen an scharfen Kanten.")

    return s

# Berechnung ausführen (triggert live)
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
    st.warning(f"**Modell:** {ergebnis['haken_typ']}")
    st.warning(f"**Größe:** {ergebnis['h_groesse']}")
    st.warning(f"**Drahtstärke:** {ergebnis['h_draht']}")
    st.warning(f"**Öhr-Stellung:** {ergebnis['h_oehr']}")
    st.warning(f"**Haken-Spitze:** {ergebnis['h_spitze']}")

# --- KÖDER-TAKTIK ---
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
st.markdown('<div class="section-header">🔍 4. Detaillierte Spot-Analyse & Boots-Tipps</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    zeit_str = ", ".join(zeitfenster) if zeitfenster else "--"
    st.markdown(f'<div class="spot-empfehlung"><strong>Status deines Spots:</strong><br>Tiefe: {tiefe_spot}m | Zeit: {zeit_str}</div>', unsafe_allow_html=True)
    
    # Boots-Spezifische Tipps
    if ausbringung == "Boot":
        st.write("**Profi-Tipp für Boot-Angler:**")
        st.write("➔ **Schnur absenken:** Nutze 'Backleads' direkt unter der Bootsrute, damit die Schnur steil zum Boden geht.")
        st.write("➔ **Präzision:** Lege den Köder langsam ab, um Verwicklungen beim Aufprall zu vermeiden.")

with sa2:
    st.write("**Konkrete Spot-Vorschläge:**")
    if ergebnis["spot_empfehlungen"]:
        for empf in ergebnis["spot_empfehlungen"]:
            st.write(empf)
    else:
        st.write("➔ Bitte fülle die Felder oben aus für konkrete Vorschläge.")

# --- BEGRÜNDUNGEN ---
st.markdown('<div class="section-header">📖 Warum dieses Setup?</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="taktik-detail">➔ Standard-Setup aktiv. Wähle mehr Kriterien für tiefere Analysen.</div>', unsafe_allow_html=True)

if ergebnis["unsicher"]:
    st.warning("⚠️ Hinweis: Einige Auswahlfelder stehen noch auf '-- Bitte wählen --'.")
# ==========================================
# 5. NATUR-FAKTOREN (MOND, LUFTDRUCK & LICHT)
# ==========================================

# Eingabe für Luftdruck (wird hier lokal für diesen Block abgefragt)
st.markdown('<div class="section-header">🌡️ 5. Wetter-Check & Natur-Faktoren</div>', unsafe_allow_html=True)
wc1, wc2 = st.columns(2)

with wc1:
    luftdruck = st.number_input("Aktueller Luftdruck (hPa)", 950, 1050, 1013, help="1013 hPa ist der Standardwert. Fallender Druck ist oft besser.")
    druck_tendenz = st.selectbox("Tendenz", ["Stabil", "Steigend", "Fallend"], help="Fallender Druck deutet oft auf fressende Fische hin.")

def get_moon_phase(date_obj):
    diff = date_obj - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Top-Zeit! Maximale Dunkelheit am Spot."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Fressaktivität steigt oft an."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Vorsicht! Fische sehen Schnüre und Schatten besser."
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt meist nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Konzentration auf tiefere Bereiche."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor Neumond."

mond_name, mond_tipp = get_moon_phase(angeltag)

with wc2:
    st.metric("Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

# --- LUFTDRUCK-ANALYSE ---
st.markdown("### 📊 Beiß-Indikatoren")
i1, i2 = st.columns(2)

with i1:
    if druck_tendenz == "Fallend":
        st.success("🔥 Fressrausch-Gefahr! Fallender Luftdruck aktiviert die Fische massiv.")
    elif druck_tendenz == "Steigend":
        st.warning("⚖️ Vorsicht: Steigender Druck kann die Fische kurzzeitig passiv machen.")
    else:
        st.info("ℹ️ Stabiler Druck: Solide Bedingungen für Langzeit-Ansitze.")

with i2:
    # --- BOOTS-LICHT & TARNUNG ---
    if ausbringung == "Boot" and zeitfenster and any(z in zeitfenster for z in ["Abend", "Nacht"]):
        st.write("**🌙 Boots-Taktik bei Nacht:**")
        if "Vollmond" in mond_name:
            st.write("➔ **Tarnung:** Meide unnötiges Licht im Boot. Deine Silhouette wird gegen den hellen Mond extrem sichtbar.")
        st.write("➔ **Licht:** Nutze Positionslichter nur zur Sicherheit, am Spot nur schwaches Rotlicht verwenden.")
    else:
        # Thermischer Beiß-Check (aus temp von Teil 1)
        if 14 <= temp <= 20:
            st.success("✅ Wassertemperatur im Idealbereich.")
        else:
            st.write("➔ Stoffwechsel beachten (Futtermenge anpassen).")

# Abschlusszeile
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Stand: {angeltag.strftime('%d.%m.%Y')} | Petri Heil!")
