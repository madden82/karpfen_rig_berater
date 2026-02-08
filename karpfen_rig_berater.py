import streamlit as st

# ==========================================
# SETUP & DESIGN
# ==========================================
st.set_page_config(page_title="Karpfen-Taktik Pro v6.0", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 2.2rem; color: #1b5e20; font-weight: bold; margin-bottom: 20px; }
    .hinweis-box { background-color: #e8f4fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196f3; margin-bottom: 25px; }
    .section-header { background-color: #2e7d32; color: white; padding: 8px 15px; border-radius: 5px; margin-top: 20px; margin-bottom: 15px; font-weight: bold; }
    .taktik-detail { background-color: #f8f9fa; padding: 12px; border-radius: 5px; border-left: 4px solid #2e7d32; margin-bottom: 10px; font-size: 0.95rem; }
    .spot-empfehlung { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px dashed #4caf50; font-weight: 500; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik-Konfigurator (Modular)</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="hinweis-box">
        <strong>💡 Anwendungshinweis:</strong> Dieses System berechnet basierend auf physikalischen Grundsätzen das optimale Setup. 
        Nutze die <strong>Fragezeichen (?)</strong> neben den Feldern für Details. 
        Bei <em>'Weiß ich nicht'</em> wird das <strong>Sicherheits-Setup</strong> gewählt.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässerprofil & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"],
                                help="Bestimmt die grundlegende Montage und Strömungsgefahr.")
    
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"],
                                    help="Beeinflusst Bleigewicht, Bleiform (Krallen) und Wurfwinkel.")
    
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0, step=0.5,
                                help="Wichtig, um das thermische Verhalten des Wassers (Sprungschicht/Winterlager) zu berechnen.")
    tiefe_spot = st.number_input("Deine aktuelle Spottiefe (m)", 0.5, 50.0, 3.5, step=0.1,
                                help="Die Tiefe, in der dein Köder tatsächlich liegen soll.")

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"],
                               help="Bestimmt die Aktivität der Fische und die optimale Tiefe.")
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15,
                     help="Direkter Einfluss auf den Stoffwechsel und die benötigte Futtermenge.")
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=4,
                                 help="Entscheidet über Bleiform (Einsinken) und Vorfachlänge.")

with c3:
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Keine Hindernisse", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"], 
                                default="Weiß ich nicht",
                                help="Bestimmt das Montagensystem (Heli-Safe/Safety-Clip) und die Hakenstabilität.")
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"],
                                  help="Beeinflusst die Tarnung (Fluorocarbon) und das Bleisystem (Inline vs. Clip).")
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], value="Weiß ich nicht",
                                  help="Beeinflusst Ködergröße und Härte, um Beifänge zu vermeiden.")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Benötigte Wurfweite (m)", 0, 180, 60) if ausbringung != "Boot" else 0
    ziel_gewicht = st.number_input("Max. erwartetes Karpfengewicht (kg)", 5, 40, 15, help="Wichtig für die Wahl der Haken-Drahtstärke.")

# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE
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
        "begruendungen": []
    }

    # Haken-Größe basierend auf Zielgewicht
    if ziel_gewicht < 10: s["h_groesse"] = 8
    elif ziel_gewicht > 20: s["h_groesse"] = 4
    else: s["h_groesse"] = 6

    # BODEN-LOGIK
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"
        s["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append(
            "➔ **Warum Heli-Safe?** Bei weichem Boden oder Kraut sinkt das Blei ein. Das Heli-Safe System ermöglicht es dem Vorfach, auf dem Leader nach oben zu gleiten."
        )
    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        s["blei_form"] = "Kompaktes Birnenblei / Torpedo"
        s["vorfach_laenge"] = "12-15 cm"
        s["begruendungen"].append("➔ **Warum kompaktes Blei?** Auf hartem Untergrund liefert dies den direktesten Gegendruck beim Ansaugen.")

    # STRÖMUNGS-LOGIK
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        s["begruendungen"].append(f"➔ **Warum Gripper-Blei?** Die Krallen verankern das Blei physisch im Boden bei {stroemung}er Strömung.")

    # HAKEN-LOGIK
    if s["koeder_praesentation"] == "Pop-Up oder Schneemann":
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
        s["begruendungen"].append("➔ **Warum Curve Shank?** Durch den gebogenen Schenkel dreht sich der Haken bei Pop-Ups aggressiver ein.")
    
    if "Muschelbänke" in hindernisse or "Scharfe Kanten" in hindernisse:
        s["h_draht"] = "X-Strong (Dickdrähtig)"
        s["begruendungen"].append("➔ **X-Strong Haken:** Erhöhte Stabilität an Hindernissen.")

    return s

# Berechnung ausführen
ergebnis = berechne_pro_logic()

# ==========================================
# 4. AUSGABE-BEREICH
# ==========================================
st.markdown('<div class="section-header">🛡️ 2. Deine optimierte Taktik-Empfehlung</div>', unsafe_allow_html=True)
res_c1, res_c2, res_c3 = st.columns(3)

with res_c1:
    st.subheader("🎣 Montage")
    st.info(f"**Bleisystem:** {ergebnis['blei_typ']}")
    st.info(f"**Blei:** {ergebnis['blei_form']} ({ergebnis['blei_gewicht']}g)")

with res_c2:
    st.subheader("🧶 Vorfach")
    st.success(f"**Rig:** {ergebnis['rig_typ']}")
    st.success(f"**Länge:** {ergebnis['vorfach_laenge']}")

with res_c3:
    st.subheader("🪝 Haken")
    st.warning(f"**Typ:** {ergebnis['haken_typ']} (Gr. {ergebnis['h_groesse']})")
    st.warning(f"**Draht:** {ergebnis['h_draht']}")

# HAKEN-TABELLE
st.markdown("### 📊 Detaillierte Haken-Konfiguration")
st.table({
    "Eigenschaft": ["Haken-Modell", "Empfohlene Größe", "Drahtstärke", "Öhr-Stellung", "Spitzen-Form"],
    "Spezifikation": [ergebnis['haken_typ'], f"Größe {ergebnis['h_groesse']}", ergebnis['h_draht'], ergebnis['h_oehr'], ergebnis['h_spitze']]
})

st.markdown('<div class="section-header">📖 Begründungen & Tipps</div>', unsafe_allow_html=True)
if ergebnis["begruendungen"]:
    for b in ergebnis["begruendungen"]:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
else:
    st.write("Keine speziellen Anpassungen für das Standard-Setup notwendig.")
