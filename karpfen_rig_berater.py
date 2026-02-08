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
# 3. EXPERTEN-LOGIK-ENGINE (TEIL 2)
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
        "futter_menge": "", 
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], 
        "spot_analyse": "", 
        "unsicher": False
    }

    # --- BODEN- & MONTAGEN-LOGIK (Korrektur: Heli-Safe) ---
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        if boden_struktur == "Weiß ich nicht": s["unsicher"] = True
        s["blei_typ"] = "Heli-Safe System"
        s["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        s["rig_typ"] = "Helikopter-Rig"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append(
            "➔ **Warum Heli-Safe?** Bei weichem Boden oder Kraut sinkt das Blei ein. Das Heli-Safe System ermöglicht es dem Vorfach, auf dem Leader nach oben zu gleiten, "
            "sodass der Köder frei präsentiert bleibt. Im Gegensatz zum Standard-Heli erlaubt dieses System den sicheren Bleiabwurf im Drill, "
            "was Fischverluste durch hängende Bleie im Kraut minimiert."
        )
    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        s["blei_form"] = "Kompaktes Birnenblei / Torpedo"
        s["vorfach_laenge"] = "12-15 cm"
        s["begruendungen"].append("➔ **Warum kompaktes Blei?** Auf hartem Untergrund liefert eine kompakte Bleiform den direktesten Gegendruck beim Ansaugen – ideal für einen aggressiven Selbsthakeffekt.")

    # --- STRÖMUNGS-PHYSIK (Das 'Warum' der Krallen) ---
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        s["begruendungen"].append(
            f"➔ **Warum Gripper-Blei?** Ein glattes Blei hat bei {stroemung}er Strömung zu wenig Reibungswiderstand und würde über den Grund rollen. "
            "Die Krallen (Gripper) verankern das Blei physisch im Boden. Dies fixiert die Montage am Spot und stellt sicher, dass der Fisch beim "
            "Ansaugen sofort auf den festen Widerstand des Bleis trifft, was den Selbsthakeffekt erst ermöglicht."
        )
        s["begruendungen"].append(
            "➔ **Warum im Winkel mit der Strömung werfen?** Wirfst du gegen den Strom, drückt der Wasserdruck das Vorfach über das Blei zurück "
            "in Richtung Hauptschnur, was fast immer zu Verwicklungen führt. Wirfst du schräg mit der Strömung, streckt der Wasserdruck "
            "das Vorfach sauber vom Blei weg."
        )

    # --- HAKEN-LOGIK (Form & Mechanik) ---
    if s["koeder_praesentation"] == "Pop-Up oder Schneemann":
        s["haken_typ"] = "Curve Shank"
        s["h_oehr"] = "Nach innen gebogen"
        s["begruendungen"].append("➔ **Warum Curve Shank?** Durch den gebogenen Schenkel dreht sich der Haken bei Pop-Up Präsentationen extrem schnell in die Unterlippe des Karpfens.")
    
    if any(h in ["Totholz", "Muschelbänke", "Scharfe Kanten"] for h in hindernisse) or ziel_gewicht > 18:
        s["h_spitze"] = "Beaked Point (Nach innen gebogen)"
        s["h_draht"] = "Dickdrahtig (X-Strong)"
        s["begruendungen"].append("➔ **Warum Beaked Point & dicker Draht?** Die nach innen gebogene Spitze schützt vor Beschädigungen am Boden und hält im Drill unter Belastung (Hindernisse/Großfisch) sicherer, ohne aufzubiegen.")

    # --- FUTTER-LOGIK ---
    menge_basis = 0.5 if temp < 12 else 1.8
    if weissfisch in ["Hoch", "Extrem", "Weiß ich nicht"]:
        if weissfisch == "Weiß ich nicht": s["unsicher"] = True
        s["futter_art"] = "Harte 24mm Boilies + Tigernüsse"
        menge_basis *= 2.5
        s["begruendungen"].append("➔ **Warum hartes Futter?** Um Weißfisch-Beifänge zu minimieren, nutzen wir Köder, die für Brassen zu groß oder zu hart sind.")
    
    s["futter_menge"] = f"{round(menge_basis, 1)} kg pro Tag/Rute"

    # --- SPOT-ANALYSE ---
    if jahreszeit == "Winter":
        s["spot_analyse"] = f"Suche die tiefsten/wärmsten Zonen bei ca. {round(tiefe_max*0.75, 1)}m."
    else:
        s["spot_analyse"] = f"Deine Tiefe von {tiefe_spot}m an Kantenübergängen ist für {jahreszeit} ideal."

    return s

# Logik ausführen
res = berechne_pro_logic()
# ==========================================
# 4. FINALE AUSGABE (UI)
# ==========================================
st.divider()
st.header("🏁 Deine Experten-Analyse & Rig-Konfiguration")

# Worst-Case Warnung
if res.get("unsicher"):
    st.markdown("""
        <div class="worst-case-warnung">
            ⚠️ <strong>Sicherheits-Modus aktiv:</strong> Da einige Parameter auf 'Weiß ich nicht' stehen, 
            wurde ein Setup für den schwierigsten Fall (Worst Case) gewählt.
        </div>
    """, unsafe_allow_html=True)

# Layout aufteilen
col_links, col_rechts = st.columns([1.2, 1.8])

with col_links:
    st.subheader("📦 Hardware-Spezifikation")
    
    with st.expander("⚓ Bleisystem & Montage", expanded=True):
        st.success(f"**Montage:** {res['blei_typ']}")
        st.info(f"**Blei:** {res['blei_gewicht']}g ({res['blei_form']})")
        st.write(f"**Leader:** {res['leader']}")

    with st.expander("🪝 Vorfach & Rig-Typ", expanded=True):
        st.warning(f"**Material:** {res['vorfach_material']}")
        st.write(f"**Länge:** {res['vorfach_laenge']}")
        st.write(f"**Rig:** {res['rig_typ']}")
        st.write(f"**Präsentation:** {res['koeder_praesentation']}")

    with st.expander("⚙️ Haken-Details", expanded=True):
        st.error(f"**Modell:** {res['haken_typ']}")
        st.write(f"📍 **Spitze:** {res['h_spitze']}")
        st.write(f"👁️ **Öhr:** {res['h_oehr']}")
        st.write(f"💪 **Draht:** {res['h_draht']}")

    with st.expander("🥣 Futter-Strategie", expanded=True):
        st.write(f"**Menge:** {res['futter_menge']}")
        st.write(f"**Köder:** {res['futter_art']}")

with col_rechts:
    st.subheader("🧐 Taktische Begründungen (Das 'Warum')")
    # Alle gesammelten Begründungen anzeigen
    if res['begruendungen']:
        for begrue in res['begruendungen']:
            st.markdown(f'<div class="taktik-detail">{begrue}</div>', unsafe_allow_html=True)
    else:
        st.write("Keine speziellen taktischen Anpassungen für diese Bedingungen nötig.")
    
    st.subheader("🗺️ Lokalisierung: Spot-Empfehlung")
    st.markdown(f'<div class="spot-empfehlung">📍 {res["spot_analyse"]}</div>', unsafe_allow_html=True)

# Finaler Haftungsausschluss
st.divider()
st.info("""
    💡 **Orientierungshilfe:** Die hier getroffenen Empfehlungen dienen als Orientierung basierend auf den eingegebenen Daten und 
    Erfahrungswerten. Da jedes Gewässer seine eigenen, speziellen Bedingungen hat, solltest du dein Rig, 
    Vorfach, Leader und Blei immer an die tatsächlichen Gegebenheiten vor Ort anpassen.
""")

st.caption("Karpfen-Rig-Konfigurator v6.0 | Modular & High-Detail")
# ==========================================
# EINGABEMASKE: WETTER-TRENDS (TEIL 4)
# ==========================================
st.markdown('<div class="section-header">⛈️ 3. Session-Wetter & Luftdruck</div>', unsafe_allow_html=True)
w1, w2 = st.columns(2)

with w1:
    luftdruck_trend = st.select_slider(
        "Luftdruck-Entwicklung", 
        options=["Stark fallend", "Fallend", "Stabil", "Steigend", "Sehr hoch"], 
        value="Stabil",
        help="Ein fallender Luftdruck (Tiefdruckgebiet) bringt oft Aktivität, während sehr hoher Druck die Fische passiv macht."
    )
    wind_wechsel = st.checkbox("Plötzlicher Windumschlag / Gewitterfront", 
                                help="Starke Wetterwechsel bringen Sauerstoff, können aber auch die Thermik im See komplett drehen.")

with w2:
    wolken = st.selectbox("Bewölkung", ["Pralle Sonne", "Leicht bewölkt", "Bedeckt", "Regen"],
                          help="Bei praller Sonne ziehen sich Fische oft in tiefere Bereiche oder Schattenplätze zurück.")
    # --- WETTER- & LUFTDRUCK-LOGIK ---
    
    # 1. Luftdruck-Analyse
    if luftdruck_trend in ["Stark fallend", "Fallend"]:
        s["begruendungen"].append(
            "➔ **Luftdruck-Alarm (Positiv):** Fallender Druck deutet auf ein heraufziehendes Tiefdruckgebiet hin. "
            "Dies ist oft die beste Beißphase! Erhöhe die Futtermenge leicht, da die Fische jetzt aktiv fressen."
        )
    elif luftdruck_trend == "Sehr hoch":
        s["koeder_praesentation"] = "Zigs oder sehr leichter Pop-Up"
        s["begruendungen"].append(
            "➔ **Luftdruck-Alarm (Negativ):** Bei extrem hohem Druck stehen die Fische oft lethargisch im Mittelwasser. "
            "Bodenköder sind jetzt schwer an den Fisch zu bringen. Versuche es mit Zig-Rigs oder biete den Köder extrem leicht (kritisch balanciert) an."
        )

    # 2. Wind- & Sauerstoff-Logik
    if wind_wechsel:
        s["spot_analyse"] = "🚨 **Taktik-Wechsel:** Der Windumschlag bringt Unruhe. Suche den Spot jetzt direkt am ufernahen Bereich, auf den der neue Wind drückt (Sauerstoff & Nahrung)."
        s["begruendungen"].append(
            "➔ **Wetterwechsel:** Starke Fronten aktivieren die Fische. Bleib wachsam, oft erfolgt ein Beißrausch kurz vor dem eigentlichen Gewitter/Regen."
        )

    # 3. Lichtverhältnisse & Tarnung
    if wolken == "Pralle Sonne" and wasser_klarheit in ["Klar", "Glasklar"]:
        s["vorfach_material"] = "Fluorocarbon (Vollmaterial)"
        s["begruendungen"].append(
            "➔ **Licht-Physik:** Bei starker Sonne und klarem Wasser werfen geflochtene Vorfächer Schatten auf den Grund. "
            "Fluorocarbon ist hier entscheidend, um keine Scheuchwirkung zu erzeugen."
        )
# ==========================================
# EINGABEMASKE: NACHT-MODUS (TEIL 6)
# ==========================================
st.markdown('<div class="section-header">🌃 4. Nachtangeln & Sichtbarkeit</div>', unsafe_allow_html=True)
n1, n2 = st.columns(2)

with n1:
    ist_nacht = st.checkbox("Ich angle (auch) nachts", help="Aktiviert spezielle Logik für Sicherheit und Detektion im Dunkeln.")
    
    mond_phase = "Keiner"
    if ist_nacht:
        mond_phase = st.selectbox("Mondphase (Nacht)", ["Keiner", "Neumond", "Halbmond", "Vollmond"], help="Die Helligkeit beeinflusst die Tarnung in der Nacht.")

with n2:
    if ist_nacht:
        beleuchtung = st.select_slider("Beleuchtung am Spot", options=["Stockdunkel", "Leicht beleuchtet", "Hell (Stadtlicht/Laterne)"], help="Fische sind nachts oft weniger scheu als tagsüber.")

    # --- NACHT-MODUS LOGIK ---

    if ist_nacht:
        # 1. Taktik: Schnurschwimmer verhindern
        # Nachts können Schnurschwimmer durch Vögel oder Wind unbemerkt bleiben.
        # Wir erhöhen das Bleigewicht leicht, um die Schnur straffer zu halten.
        s["blei_gewicht"] += 10 # 10g extra für mehr Stabilität
        s["begruendungen"].append(
            "➔ **Nacht-Sicherheit (Blei):** Wir haben das Bleigewicht um 10g erhöht. Dies hilft, die Hauptschnur straffer am Boden zu halten und reduziert Fehlalarme durch Vögel oder Wind (Schnurschwimmer)."
        )

        # 2. Taktik: Köder-Sichtbarkeit in der Dunkelheit
        if mond_phase == "Neumond" or beleuchtung == "Stockdunkel":
            # Wenn es zappenduster ist, muss der Köder visuell oder olfaktorisch hervorstechen.
            s["koeder_praesentation"] = "Fluo Pop-Up (High-Vis) oder extrem gesoakter Hookbait"
            s["begruendungen"].append(
                "➔ **Nacht-Sichtbarkeit:** Bei Neumond oder Dunkelheit empfehlen wir einen fluoreszierenden (Fluo) Pop-Up oder einen stark gesoakten Köder. Karpfen nutzen nachts ihre Sehorgane und Geruchssinne intensiv."
            )
        elif mond_phase == "Vollmond" or beleuchtung in ["Leicht beleuchtet", "Hell (Stadtlicht/Laterne)"]:
             s["begruendungen"].append(
                "➔ **Nacht-Tarnung:** Bei Vollmond oder Stadtlicht kann die Tarnung wieder wichtiger werden. Halte dich an das Standard-Setup oder nutze dunkle (Black-Out) Haken, falls die Fische scheu sind."
            )

        # 3. Akustische Detektion
        s["begruendungen"].append(
            "➔ **Akustische Detektion:** Nutze Bissanzeiger mit hoher Lautstärke oder Funkboxen. Stelle die Empfindlichkeit nicht zu hoch ein, um Windbisse zu vermeiden."
        )

