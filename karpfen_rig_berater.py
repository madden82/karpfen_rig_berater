import streamlit as st

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
    .stSelectbox, .stSlider, .stNumberInput, .stMultiSelect { margin-bottom: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik Pro (Mobil)</div>', unsafe_allow_html=True)

# ==========================================
# EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässer & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    tiefe_max = st.number_input("Maximale Tiefe (m)", 1.0, 60.0, 8.0, step=0.5)
    tiefe_spot = st.number_input("Aktuelle Spottiefe (m)", 0.5, 50.0, 3.5, step=0.1)

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    boden_struktur = st.selectbox("Bodenbeschaffenheit", ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=4)
    nacht_angeln = st.checkbox("🌙 Nachtsession geplant?", value=False)

with c3:
    hindernisse = st.multiselect("Hindernisse am Platz", ["Keine Hindernisse", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"], default="Weiß ich nicht")
    aktivitaet = st.select_slider("Fischverhalten", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    weissfisch = st.select_slider("Weißfischvorkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], value="Weiß ich nicht")
    ausbringung = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    ziel_gewicht = st.number_input("Zielgewicht Karpfen (kg)", 5, 40, 15)
# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (VOLLSTÄNDIG)
# ==========================================

def berechne_pro_logic():
    # Initialisierung des Ergebnis-Objekts mit allen Feldern
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
        "spot_analyse": "", 
        "unsicher": False
    }

    # --- HAKEN-GRÖSSE ---
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 20: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # --- BODEN- & MONTAGEN-LOGIK ---
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        if boden_struktur == "Weiß ich nicht": s["unsicher"] = True
        s["blei_typ"] = "Heli-Safe System"
        s["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append(
            "➔ **Warum Heli-Safe?** Bei weichem Boden oder Kraut sinkt das Blei ein. Das Heli-Safe System ermöglicht es dem Vorfach, auf dem Leader nach oben zu gleiten. "
            "Im Gegensatz zum Standard-Heli erlaubt dieses System den sicheren Bleiabwurf im Drill, was Fischverluste im Kraut minimiert."
        )
    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        s["blei_form"] = "Kompaktes Birnenblei / Torpedo"
        s["vorfach_laenge"] = "12-15 cm"
        s["begruendungen"].append("➔ **Warum kompaktes Blei?** Auf hartem Untergrund liefert eine kompakte Bleiform den direktesten Gegendruck beim Ansaugen.")

    # --- STRÖMUNGS-PHYSIK ---
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        s["begruendungen"].append(f"➔ **Warum Gripper-Blei?** Die Krallen verankern das Blei physisch im Boden bei {stroemung}er Strömung.")

    # --- HAKEN-LOGIK ---
    if s["koeder_praesentation"] in ["Pop-Up oder Schneemann"]:
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
        s["begruendungen"].append("➔ **Warum Curve Shank?** Durch den gebogenen Schenkel dreht sich der Haken bei Pop-Ups aggressiver ein.")
    
    if "Muschelbänke" in hindernisse or "Scharfe Kanten" in hindernisse:
        s["h_draht"] = "X-Strong (Dickdrähtig)"
        s["leader"] = "Dicke Schlagschnur + Leadcore"
        s["begruendungen"].append("➔ **X-Strong Haken:** Verhindert das Aufbiegen bei Drills an scharfen Hindernissen.")

    # --- NACHTANGEL-LOGIK (KRITERIEN) ---
    if nacht_angeln:
        if "Kraut" in hindernisse:
            s["begruendungen"].append(
                "⚠️ **Nacht-Sauerstoff:** Pflanzen verbrauchen nachts O2. Suche bei viel Kraut eher die Randbereiche auf, "
                "da dort der Sauerstoffgehalt stabiler bleibt als mitten im dichten Feld."
            )
        if tiefe_spot < 2.0:
            s["begruendungen"].append(
                "🌙 **Nacht-Ufer-Bonus:** Fische ziehen nachts extrem nah ans Ufer (Sicherheitszone). Dein flacher Spot "
                "von " + str(tiefe_spot) + "m ist nachts oft fängiger als am Tag. Absolute Ruhe am Ufer ist jetzt Pflicht!"
            )
        s["begruendungen"].append("🌙 **Schnurschwimmer:** Nutze nachts Backleads (Absenker), um keine falschen Alarme durch nahrungssuchende Fische zu bekommen.")

    # --- SPOT-ANALYSE ---
    if jahreszeit == "Frühjahr":
        if tiefe_spot < 2.0: s["spot_analyse"] = "Hervorragend! Flachzonen erwärmen sich jetzt schnell."
        else: s["spot_analyse"] = "Etwas zu tief für Frühjahr. Suche Plateaus unter 2m."
    elif jahreszeit == "Winter":
        if tiefe_spot > 5.0: s["spot_analyse"] = "Gute Tiefe. Wasser ist hier im Winter am stabilsten (4°C)."
        else: s["spot_analyse"] = "Vorsicht: Flachbereiche kühlen im Winter zu stark aus."
    else:
        s["spot_analyse"] = "Die Tiefe ist für die aktuelle Jahreszeit plausibel."

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
    st.warning(f"**Modell:** {ergebnis['haken_typ']}")
    st.warning(f"**Größe:** {ergebnis['h_groesse']}")
    st.warning(f"**Drahtstärke:** {ergebnis['h_draht']}")

# --- NACHTANGEL-MODUS INFO ---
if nacht_angeln:
    st.markdown('<div class="section-header">🌙 Nachtangel-Modus: Aktiv</div>', unsafe_allow_html=True)
    n1, n2 = st.columns(2)
    with n1:
        st.write("**Verhalten am Spot:**")
        st.write("➔ Ufernähe bevorzugen (Fische ziehen flach)")
        st.write("➔ Absolute Ruhe (Schall überträgt nachts stärker)")
    with n2:
        st.write("**Technik-Tipp:**")
        st.write("➔ Backleads (Absenker) gegen Schnurschwimmer")
        st.write("➔ Rotlicht für Stirnlampe (Tarnung)")

# --- DETAILLIERTE HAKEN-TABELLE ---
st.markdown("### 📊 Haken-Spezifikationen im Detail")
st.table({
    "Eigenschaft": ["Haken-Modell", "Empfohlene Größe", "Drahtstärke", "Öhr-Stellung", "Spitzen-Form"],
    "Spezifikation": [
        ergebnis['haken_typ'], 
        f"Größe {ergebnis['h_groesse']}", 
        ergebnis['h_draht'], 
        ergebnis['h_oehr'], 
        ergebnis['h_spitze']
    ]
})

# --- SPOT-ANALYSE & FUTTER ---
st.markdown('<div class="section-header">🔍 3. Spot-Check & Futterstrategie</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)

with sa1:
    st.markdown(f'<div class="spot-empfehlung"><strong>Spot-Analyse:</strong><br>{ergebnis["spot_analyse"]}</div>', unsafe_allow_html=True)

with sa2:
    st.write("**Fütterungsempfehlung:**")
    st.write(f"➔ Menge: {ergebnis['futter_menge']}")
    st.write(f"➔ Art: {ergebnis['futter_art']}")

# --- BEGRÜNDUNGEN (UNVERKÜRZT) ---
st.markdown('<div class="section-header">📖 Warum dieses Setup? (Experten-Logik)</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="taktik-detail">➔ Standard-Setup aktiv. Keine speziellen Anpassungen für diese Bedingungen notwendig.</div>', unsafe_allow_html=True)

if ergebnis["unsicher"]:
    st.warning("⚠️ Hinweis: Da einige Angaben auf 'Weiß ich nicht' stehen, wurde ein universelles Sicherheits-Setup gewählt.")
# ==========================================
# 5. NATUR-FAKTOREN (MOND & WETTER)
# ==========================================
import datetime

def get_moon_phase(date):
    # Berechnung des Mondzyklus (Lunation ca. 29.5 Tage)
    diff = date - datetime.date(2001, 1, 1)
    days = diff.days
    lunation = 29.530588853
    phase_pos = (days / lunation) % 1
    
    if phase_pos < 0.06: return "🌑 Neumond", "Top-Zeit! Karpfen sind oft weniger vorsichtig."
    elif phase_pos < 0.20: return "🌒 Zunehmende Sichel", "Gute Bedingungen für die Nacht."
    elif phase_pos < 0.30: return "🌓 Erstes Viertel", "Normales Beißverhalten."
    elif phase_pos < 0.45: return "🌔 Zunehmender Mond", "Aktivität steigt oft an."
    elif phase_pos < 0.55: return "🌕 Vollmond", "Oft große Fische, aber sehr hohe Vorsicht!"
    elif phase_pos < 0.70: return "🌖 Abnehmender Mond", "Aktivität lässt leicht nach."
    elif phase_pos < 0.80: return "🌗 Letztes Viertel", "Konzentration auf tiefere Bereiche."
    else: return "🌘 Abnehmende Sichel", "Ruhephase vor Neumond."

# Berechnungen für den heutigen Tag
heute = datetime.date.today()
mond_name, mond_tipp = get_moon_phase(heute)

st.markdown('<div class="section-header">🌙 4. Natur-Faktoren (Live)</div>', unsafe_allow_html=True)
m_c1, m_c2 = st.columns(2)

with m_c1:
    st.metric("Aktuelle Mondphase", mond_name)
    st.write(f"_{mond_tipp}_")

with m_c2:
    st.write("**Beißfenster-Check:**")
    # Auswertung basierend auf der Temperatur-Eingabe aus Teil 1
    if temp > 12 and temp < 22:
        st.success("✅ Stoffwechsel optimal (Gute Beißchance)")
    elif temp >= 22:
        st.warning("⚠️ Sauerstoffmangel möglich (Spots mit Bewegung suchen)")
    else:
        st.info("❄️ Träge Phase (Sehr wenig füttern!)")

# Abschlusszeile für die App
st.markdown("---")
st.caption(f"Karpfen-Taktik Pro v6.0 | Mobil-Modus | Stand: {heute.strftime('%d.%m.%Y')}")
