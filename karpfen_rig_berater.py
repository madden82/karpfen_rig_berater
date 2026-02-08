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
                                    help="Beeinflusst Bleigewicht und Bleiform (Krallen).")
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0, step=0.5, help="Wichtig für das thermische Verhalten (Sprungschicht).")
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5, step=0.1, help="Die Tiefe am exakten Ablegeplatz.")

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"], help="Bestimmt die Aktivität und die Tiefe.")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15, help="Direkter Einfluss auf den Stoffwechsel.")
    # NEU: Neutraler Index
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], 
                                 index=0, help="Entscheidet über Bleiform und Vorfachlänge.")
    nacht_angeln = st.checkbox("🌙 Nachtsession geplant?", help="Aktiviert Sauerstoff-Warnungen und Ufer-Taktik.")
    # NEU: Datums-Eingabe für Mond
    angeltag = st.date_input("Wann fischst du?", datetime.date.today(), help="Berechnet die Mondphase für diesen Tag.")

with c3:
    # NEU: Platzhalter für Hindernisse
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], 
                                default=None, placeholder="Hier auswählen...",
                                help="Bestimmt Montagensystem und Hakenstabilität.")
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"], help="Beeinflusst Tarnung und Bleisystem.")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True, help="Wurfweite vs. präzises Ablegen.")
    
    # NEU: Unterauswahl für Boot
    boots_taktik = "Normal"
    if ausbringung == "Boot":
        boots_taktik = st.selectbox("Vorgehen vom Boot", ["Nur Ablegen", "Vom Boot auswerfen"], help="Entscheidet über Bleigewicht (Verdriften beim Absinken).")
    
    ziel_gewicht = st.number_input("Max. erwartetes Gewicht (kg)", 5, 40, 15, help="Wichtig für die Wahl der Haken-Drahtstärke.")
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (OPTIMIERT)
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
        "futter_menge": "Moderat (ca. 500g - 1kg)", 
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], 
        "spot_analyse_text": "", 
        "spot_empfehlungen": [],
        "unsicher": False
    }

    # --- HAKEN-GRÖSSEN-LOGIK ---
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 20: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht", "-- Bitte wählen --"] or "Kraut" in hindernisse:
        if boden_struktur in ["Weiß ich nicht", "-- Bitte wählen --"]: s["unsicher"] = True
        s["blei_typ"] = "Heli-Safe System"
        s["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append("➔ **Heli-Safe:** Verhindert das Einsinken im weichen Grund.")
    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        s["blei_form"] = "Kompaktes Birnenblei / Torpedo"
        s["vorfach_laenge"] = "12-15 cm"

    # --- BOOTS- & AUSBRINGUNGS-LOGIK ---
    if ausbringung == "Boot":
        if boots_taktik == "Nur Ablegen":
            s["blei_gewicht"] = 140 # Schwereres Blei zum sauberen Straffen der Schnur
            s["begruendungen"].append("➔ **Schweres Blei (Ablegen):** Verhindert, dass das Blei beim Straffen der Schnur vom Boot aus verrutscht.")
        else:
            s["blei_gewicht"] = 110
            s["begruendungen"].append("➔ **Mittelschweres Blei (Boot-Wurf):** Ideal für präzise Würfe auf kurze Distanz vom Boot.")
    
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 170 if stroemung == "Stark" else 140

    # --- HAKEN-SETUP DETAILS (Integriert) ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
    if "Muschelbänke" in hindernisse or "Scharfe Kanten" in hindernisse:
        s["h_draht"] = "X-Strong (Dickdrähtig)"

    # --- ERWEITERTE SPOT-ANALYSE ---
    # Thermik & Tiefe
    if temp < 10:
        s["spot_empfehlungen"].append("📍 Suche nach den tiefsten Stellen (Winterlager).")
        s["spot_empfehlungen"].append("📍 Südhang-Ufer suchen (maximale Sonneneinstrahlung).")
    elif 12 <= temp <= 20:
        s["spot_empfehlungen"].append("📍 Plateaus in 2-4m Tiefe abfischen.")
        s["spot_empfehlungen"].append("📍 Windzugewandtes Ufer (Sauerstoff & Nahrung).")
    
    if "Kraut" in hindernisse:
        s["spot_empfehlungen"].append("📍 'Löcher' im Kraut suchen oder Krautkanten befischen.")
    if "Totholz" in hindernisse:
        s["spot_empfehlungen"].append("📍 Unmittelbare Nähe zum Holz suchen, aber 'Tight Clutch' fischen.")

    if nacht_angeln:
        s["spot_empfehlungen"].append("📍 Nachts: Ziehe eine Rute extrem flach (bis 1m) ans Ufer.")

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
    # Alle Haken-Details jetzt hier direkt in der Rubrik (Tabelle entfernt)
    st.warning(f"**Modell:** {ergebnis['haken_typ']}")
    st.warning(f"**Größe:** {ergebnis['h_groesse']}")
    st.warning(f"**Drahtstärke:** {ergebnis['h_draht']}")
    st.warning(f"**Öhr-Stellung:** {ergebnis['h_oehr']}")
    st.warning(f"**Haken-Spitze:** {ergebnis['h_spitze']}")

# --- ERWEITERTE SPOT-ANALYSE ---
st.markdown('<div class="section-header">🔍 3. Spot-Check & Empfehlungen</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    st.markdown(f'<div class="spot-empfehlung"><strong>Status deines Spots:</strong><br>{ergebnis["spot_analyse_text"] if ergebnis["spot_analyse_text"] else "Tiefe und Temperatur sind für die Jahreszeit plausibel."}</div>', unsafe_allow_html=True)
    
    # Neue detaillierte Spot-Vorschläge
    st.write("**Konkrete Spot-Empfehlungen:**")
    if ergebnis["spot_empfehlungen"]:
        for empf in ergebnis["spot_empfehlungen"]:
            st.write(empf)
    else:
        st.write("➔ Suche nach Strukturveränderungen (Kanten/Muscheln).")

with sa2:
    st.write("**Futterstrategie:**")
    st.write(f"➔ Menge: {ergebnis['futter_menge']}")
    st.write(f"➔ Art: {ergebnis['futter_art']}")
    if nacht_angeln:
        st.write("➔ Nacht-Tipp: Ufernahe Futterstraße anlegen.")

# --- BEGRÜNDUNGEN ---
st.markdown('<div class="section-header">📖 Warum dieses Setup?</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="taktik-detail">➔ Standard-Setup aktiv. Keine speziellen Hindernis-Anpassungen nötig.</div>', unsafe_allow_html=True)

if ergebnis["unsicher"]:
    st.warning("⚠️ Hinweis: Da 'Bitte wählen' oder 'Weiß ich nicht' beim Boden steht, wurde ein Sicherheits-Setup gewählt.")
# ==========================================
# 5. NATUR-FAKTOREN (DYNAMISCHES DATUM)
# ==========================================

def get_moon_phase(date_obj):
    # Berechnung basierend auf dem vom User gewählten Datum
    diff = date_obj - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Top-Zeit! Karpfen sind oft mutiger und ziehen aktiv."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen für die Nacht."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten zu erwarten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Fressaktivität steigt oft spürbar an."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Vorsicht geboten! Oft große Fische, aber sehr scheu."
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt meist leicht nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Fische ziehen sich oft in tiefere Bereiche zurück."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor dem nächsten Neumond."

# Berechnung für das gewählte Datum aus der Eingabemaske
mond_name, mond_tipp = get_moon_phase(angeltag)

st.markdown('<div class="section-header">🌙 4. Natur-Faktoren für den ' + angeltag.strftime('%d.%m.%Y') + '</div>', unsafe_allow_html=True)
m_c1, m_c2 = st.columns(2)

with m_c1:
    st.metric("Voraussichtliche Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

with m_c2:
    st.write("**Thermischer Beiß-Check:**")
    # Bewertung basierend auf der Temperatur-Eingabe
    if 13 <= temp <= 21:
        st.success("✅ Stoffwechsel im Idealbereich")
    elif temp > 21:
        st.warning("⚠️ Hohe Temperatur: Sauerstoff am Grund prüfen!")
    elif temp < 7:
        st.info("❄️ Kaltwasser-Modus: Minimal füttern!")
    else:
        st.write("➔ Übergangsphase: Beobachte den Luftdruck.")

# Abschlusszeile
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Datumsfokus: {angeltag.strftime('%d.%m.%Y')} | Petri Heil!")
