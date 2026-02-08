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
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik-Konfigurator (Modular)</div>', unsafe_allow_html=True)

st.markdown("""
    <div class="hinweis-box">
        <strong>💡 Anwendungshinweis:</strong> Fülle zuerst alle Parameter aus. Bei <em>'Weiß ich nicht'</em> wird automatisch das 
        <strong>Worst-Case-Sicherheits-Setup</strong> gewählt.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässerprofil & Tiefen</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    
    # Dynamische Strömungsabfrage
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0, step=0.5)
    tiefe_spot = st.number_input("Deine aktuelle Spottiefe (m)", 0.5, 50.0, 3.5, step=0.1)

with c2:
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=4)

with c3:
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Keine Hindernisse", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"], 
                                default="Weiß ich nicht")

# ==========================================
# EINGABEMASKE: TAKTIK & FISCH
# ==========================================
st.markdown('<div class="section-header">🎯 2. Fischverhalten & Taktik</div>', unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)

with t1:
    aktivitaet = st.select_slider("Fischverhalten (Vorsicht)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    wasser_klarheit = st.select_slider("Wasser-Sichtigkeit", options=["Trüb", "Mittel", "Klar", "Glasklar"])

with t2:
    weissfisch = st.select_slider("Vorkommen anderer Weißfische", options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], value="Weiß ich nicht")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)

with t3:
    wurfweite = st.slider("Benötigte Wurfweite (m)", 0, 180, 60) if ausbringung != "Boot" else 0
    ziel_gewicht = st.number_input("Max. erwartetes Karpfengewicht (kg)", 5, 40, 15)


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
        "futter_menge": "", 
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [], 
        "spot_analyse": "", 
        "unsicher": False
    }

    # --- BLEI- & BODEN-LOGIK ---
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        if boden_struktur == "Weiß ich nicht": s["unsicher"] = True
        s["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        s["blei_gewicht"] = 75 if wurfweite < 80 else 85
        s["rig_typ"] = "Helikopter-System"
        s["koeder_praesentation"] = "Pop-Up oder Schneemann"
        s["vorfach_laenge"] = "25-35 cm"
        s["begruendungen"].append(f"➔ **Boden-Physik:** Ein flaches Flächenblei verhindert bei {boden_struktur} das tiefe Einsinken. Das Helikopter-Rig sorgt dafür, dass das Vorfach auf dem Leader nach oben gleiten kann, anstatt mit dem Blei im Schlamm zu verschwinden.")
    
    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        s["blei_form"] = "Kompaktes Birnenblei / Torpedo"
        s["vorfach_laenge"] = "12-15 cm"
        s["begruendungen"].append("➔ **Boden-Physik:** Auf hartem Untergrund liefert eine kompakte Bleiform den direktesten Gegendruck beim Ansaugen – ideal für den Selbsthakeffekt.")

    # --- HINDERNIS-LOGIK & SICHERHEIT ---
    if "Weiß ich nicht" in hindernisse or any(h in ["Totholz", "Muschelbänke", "Scharfe Kanten"] for h in hindernisse):
        if "Weiß ich nicht" in hindernisse: s["unsicher"] = True
        s["blei_typ"] = "Safety-Clip (Blei verlierend eingestellt)"
        s["vorfach_material"] = "Abriebfestes Mono / Snag-Link"
        s["leader"] = "Schlagschnur (min. 0.50mm) + Safety Clip"
        s["begruendungen"].append("🛡️ **Sicherheit:** Bei Hindernissen muss das Blei im Drill sofort ausklinken. Ein festes Blei würde den Fisch bei einem Hänger unweigerlich zum Abriss führen.")

    # --- STRÖMUNGS-LOGIK ---
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        s["begruendungen"].append(f"🌊 **Strömungs-Physik:** Ein Gripper-Blei ist bei {stroemung}er Strömung nötig. **Taktik:** Wirf immer im Winkel mit der Strömung aus, damit der Wasserdruck das Vorfach nicht in die Hauptschnur drückt.")

    # --- FISCH-VORSICHT & INLINE-LOGIK ---
    if aktivitaet in ["Weiß ich nicht", "Vorsichtig"]:
        if aktivitaet == "Weiß ich nicht": s["unsicher"] = True
        if "Keine Hindernisse" in hindernisse:
            s["blei_typ"] = "Inline-Blei (Festmontage)"
            s["vorfach_material"] = "Fluorocarbon (unsichtbar)"
            s["begruendungen"].append("🤫 **Tarnung:** Da keine Hindernisse da sind, bietet das Inline-Blei bei scheuen Fischen den direktesten Hakeffekt und beste Tarnung.")
        else:
            s["blei_typ"] = "Inline-Blei mit Sicherheitsclip"
            s["begruendungen"].append("⚠️ **Hybrid-Lösung:** Inline-System mit Clip gewählt – maximale Tarnung bei gleichzeitigem Schutz vor Fischverlust durch Hänger.")

    # --- WEITWURF-LOGIK ---
    if wurfweite > 95 and s["rig_typ"] != "Helikopter-System":
        s["rig_typ"] = "Helikopter-System (Weitwurf-Konfiguration)"
        s["begruendungen"].append("🚀 **Wurf-Physik:** Bei Distanzen über 95m ist das Helikopter-Rig am aerodynamischsten, da das Blei ganz vorne sitzt und Verhedderungen verhindert.")

    # --- FUTTER-LOGIK ---
    menge_basis = 0.5 if temp < 12 else 1.8
    if weissfisch in ["Hoch", "Extrem", "Weiß ich nicht"]:
        if weissfisch == "Weiß ich nicht": s["unsicher"] = True
        s["futter_art"] = "Harte 24mm Boilies + Tigernüsse (selektiv)"
        menge_basis *= 2.5
        s["begruendungen"].append("🐟 **Selektion:** Bei hohem Weißfischdruck nutzen wir hartes, großes Futter, um Brassen und Rotaugen vom Haken fernzuhalten.")
    
    s["futter_menge"] = f"{round(menge_basis, 1)} kg pro Tag/Rute"

    return s

res = berechne_pro_logic()
# ==========================================
# 4. SPOT-ANALYSE & HAKEN-LOGIK (TEIL 3)
# ==========================================

def finalisiere_taktik(s):
    # --- HAKEN-LOGIK (Formen & Gründe) ---
    if s["koeder_praesentation"] == "Pop-Up oder Schneemann":
        s["haken_typ"] = "Curve Shank oder Chod-Haken"
        s["haken_begruendung"] = "➔ **Haken-Mechanik:** Bei Pop-Ups dreht sich ein Curve Shank Haken durch die gebogene Form schneller in die Unterlippe."
    else:
        s["haken_typ"] = "Wide Gape (Gr. 4-6)"
        s["haken_begruendung"] = "➔ **Haken-Mechanik:** Der Wide Gape ist der Allrounder für Bodenköder. Er greift durch den weiten Bogen extrem sicher im Fleisch."

    # --- PRÄZISE SPOT-ANALYSE (Tiefen-Verhältnis) ---
    if jahreszeit == "Winter" or temp < 8:
        optimale_tiefe = tiefe_max * 0.75
        s["spot_analyse"] = f"Winter-Modus: Suche die tiefsten/wärmsten Zonen bei ca. {round(optimale_tiefe, 1)}m. Deine {tiefe_spot}m könnten zu kalt sein."
    elif jahreszeit == "Frühjahr":
        s["spot_analyse"] = "Frühjahrs-Modus: Suche flache Plateaus (0.5m - 2.5m). Deine Tiefe ist okay, aber suche nach sonnigen Kanten!"
    elif temp > 22:
        s["spot_analyse"] = "Sommer-Hitze: Sauerstoffmangel im Tiefenwasser möglich. Fische in 3m - 5m an Windkanten."
    else:
        s["spot_analyse"] = f"Standard-Zugrouten: Deine Tiefe von {tiefe_spot}m an Kantenübergängen ist für {jahreszeit} ideal."

    return s

# Finalisierung ausführen
final_res = finalisiere_taktik(res)

# ==========================================
# 5. VISUELLE AUSGABE (UI)
# ==========================================
st.divider()
st.header("🏁 Taktik-Analyse & Rig-Empfehlung")

# Worst-Case Warnung bei "Weiß ich nicht"
if final_res["unsicher"]:
    st.markdown('<div class="worst-case-warnung">⚠️ **Hinweis:** Da einige Parameter unbekannt sind, wurde ein Sicherheits-Setup für den Worst Case (Schlamm/Hindernisse/Weißfische) berechnet.</div>', unsafe_allow_html=True)

o1, o2 = st.columns([1, 1.5])

with o1:
    st.subheader("📦 Hardware-Konfiguration")
    st.metric("Empf. Bleigewicht", f"{final_res['blei_gewicht']} g")
    st.success(f"**Montage:** {final_res['blei_typ']}")
    st.info(f"**Blei:** {final_res['blei_form']}")
    st.warning(f"**Vorfach:** {final_res['vorfach_material']} ({final_res['vorfach_laenge']})")
    
    st.write(f"**Haken:** {final_res['haken_typ']}")
    st.write(f"**Leader:** {final_res['leader']}")
    st.write(f"**Rig:** {final_res['rig_typ']}")
    st.write(f"**Präsentation:** {final_res['koeder_praesentation']}")
    
    st.subheader("🥣 Futter-Strategie")
    st.write(f"**Menge:** {final_res['futter_menge']}")
    st.write(f"**Art:** {final_res['futter_art']}")

with o2:
    st.subheader("🧐 Taktische Begründungen")
    # Alle Begründungen aus der Logik anzeigen
    for b in final_res['begruendungen']:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)
    
    # Haken-Begründung hinzufügen
    st.markdown(f'<div class="taktik-detail">{final_res["haken_begruendung"]}</div>', unsafe_allow_html=True)
    
    st.subheader("🗺️ Spot- & Tiefen-Empfehlung")
    st.markdown(f'<div class="spot-empfehlung">📍 {final_res["spot_analyse"]}</div>', unsafe_allow_html=True)

st.divider()
st.info("💡 **Orientierungshilfe:** Die hier getroffenen Empfehlungen dienen als Orientierung basierend auf den eingegebenen Daten und Erfahrungswerten. Da jedes Gewässer seine eigenen, speziellen Bedingungen hat, solltest du dein Rig, Vorfach, Leader und Blei immer an die tatsächlichen Gegebenheiten vor Ort anpassen.")

st.caption("Karpfen-Rig-Konfigurator v6.0 | Modular & High-Detail")
# ==========================================
# 4. ERWEITERTE HAKEN-ENGINE (MODULAR)
# ==========================================

def berechne_haken_logik(s, boden, hindernisse, aktivitaet, praesentation):
    h = {
        "typ": "Wide Gape",
        "begruendungen": []
    }

    # 1. Logik: Wide Gape (Der Allrounder)
    if praesentation in ["Bodenköder", "Snowman", "Wafter"] and "Keine Hindernisse" in hindernisse:
        h["typ"] = "Wide Gape"
        h["begruendungen"].append("➔ **Haken:** Wide Gape gewählt. Großer Bogen & stabiler Halt – verzeiht Rig-Fehler und ist ideal für Bodenköder auf fast allen Böden.")

    # 2. Logik: Curve Shank (Aggressiv bei Vorsicht)
    if aktivitaet == "Vorsichtig" and not any(hi in ["Totholz", "Scharfe Kanten"] for hi in hindernisse):
        h["typ"] = "Curve Shank"
        h["begruendungen"].append("➔ **Haken:** Curve Shank gewählt. Aggressives Eindrehen bei vorsichtigen Fischen. **Achtung:** Erhöhte Hebelwirkung, daher nur in hindernisfreiem Wasser!")

    # 3. Logik: Long Shank (Präzision auf hartem Boden)
    if boden in ["Sand / Kies (hart)", "Lehm (fest)"] and aktivitaet == "Vorsichtig":
        h["typ"] = "Long Shank"
        h["begruendungen"].append("➔ **Haken:** Long Shank gewählt. Ideal für harte Böden und vorsichtige Fische. Bietet extrem schnelle Penetration im Fischmaul.")

    # 4. Logik: Short Shank / Stiff Rigger (Die Brechstange)
    if any(hi in ["Kraut", "Muschelbänke", "Totholz"] for hi in hindernisse):
        h["typ"] = "Short Shank / Stiff Rigger"
        h["begruendungen"].append("➔ **Haken:** Short Shank gewählt. Sehr kompakt und stabil für hindernisreiche Gewässer. Minimale Hebelwirkung verhindert Aufbiegen/Ausschlitzen.")

    # 5. Logik: Chod Hook (Spezialist für Extremfälle)
    if s["rig_typ"] == "Helikopter-System" and boden in ["Schlamm (weich)", "Moder (faulig)"]:
        h["typ"] = "Chod Hook"
        h["begruendungen"].append("➔ **Haken:** Chod Hook gewählt. Speziell für Pop-Ups im Tiefschlamm oder Kraut. Dreht extrem schnell an steifen Vorfächern.")

    # 6. Logik: Krank (Der Hybrid-Vorteil)
    if boden == "Weiß ich nicht" or (praesentation == "Snowman" and aktivitaet == "Normal"):
        h["typ"] = "Krank (Wide Curve Hybrid)"
        h["begruendungen"].append("➔ **Haken:** Krank gewählt. Vereint die Vorteile von Wide Gape und Curve Shank. Hohe Hakquote bei geringerem Ausschlitzrisiko.")

    return h

# Integration in den Hauptablauf:
haken_ergebnis = berechne_haken_logik(res, boden_struktur, hindernisse, aktivitaet, res["koeder_praesentation"])
res["haken_typ"] = haken_ergebnis["typ"]
res["begruendungen"].extend(haken_ergebnis["begruendungen"])
# ==========================================
# 5. HAKEN-EIGENSCHAFTEN (TEIL 5)
# ==========================================

def berechne_haken_details(h_typ, boden, hindernisse, gewicht, aktivitaet):
    d = {
        "spitze": "Straight Point (Gerade)",
        "oehr": "Gerade (Universell)",
        "draht": "Standard",
        "detail_begruendung": []
    }

    # 1. Logik: Hakenspitze
    if any(hi in ["Kraut", "Muschelbänke", "Totholz"] for hi in hindernisse) or boden == "Weiß ich nicht":
        d["spitze"] = "Beaked Point (Nach innen gebogen)"
        d["detail_begruendung"].append("📍 **Spitze:** Ein Beaked Point schützt die Spitze vor Beschädigungen am Boden und hält im Drill unter Belastung (Hindernisse) sicherer.")
    elif boden in ["Sand / Kies (hart)", "Lehm (fest)"]:
        d["spitze"] = "Straight Point (Gerade)"
        d["detail_begruendung"].append("📍 **Spitze:** Auf hartem Boden bietet eine gerade Spitze (Straight Point) die schnellste Penetration im Fischmaul.")

    # 2. Logik: Öhr-Winkel
    if h_typ in ["Curve Shank", "Long Shank", "Krank"]:
        d["oehr"] = "Nach innen gebogen (In-turned Eye)"
        d["detail_begruendung"].append("👁️ **Öhr:** Das nach innen gebogene Öhr unterstützt die aggressive Drehbewegung dieser Hakenformen.")
    elif h_typ in ["Chod Hook", "Short Shank / Stiff Rigger"]:
        d["oehr"] = "Nach außen gebogen (Out-turned Eye)"
        d["detail_begruendung"].append("👁️ **Öhr:** Das nach außen gebogene Öhr ist ideal für steife Monovorfächer (D-Rig/Chod), damit das Material nicht abknickt.")

    # 3. Logik: Drahtstärke
    if gewicht > 18 or any(hi in ["Totholz", "Muschelbänke"] for hi in hindernisse):
        d["draht"] = "Dickdrahtig (X-Strong / Heavy Wire)"
        d["detail_begruendung"].append("💪 **Draht:** Aufgrund des Fischgewichts oder der Hindernisse ist ein dickdrahtiger Haken nötig, um ein Aufbiegen zu verhindern.")
    elif aktivitaet == "Vorsichtig" and gewicht < 12:
        d["draht"] = "Dünndrahtig (Fine Wire)"
        d["detail_begruendung"].append("💪 **Draht:** Bei vorsichtigen Fischen im Freiwasser dringt ein dünndrahtiger Haken leichter ein und ist unauffälliger.")

    return d

# Integration in den Ablauf:
h_details = berechne_haken_details(res["haken_typ"], boden_struktur, hindernisse, ziel_gewicht, aktivitaet)
res["h_spitze"] = h_details["spitze"]
res["h_oehr"] = h_details["oehr"]
res["h_draht"] = h_details["draht"]
res["begruendungen"].extend(h_details["detail_begruendung"])
# ==========================================
# 6. FINALE HIGH-DETAIL AUSGABE (UI)
# ==========================================
st.divider()
st.header("🏁 Deine Experten-Analyse & Rig-Konfiguration")

# Worst-Case Warnung prominent platzieren
if res.get("unsicher"):
    st.markdown("""
        <div class="worst-case-warnung">
            ⚠️ <strong>Sicherheits-Modus aktiv:</strong> Da einige Parameter auf 'Weiß ich nicht' stehen, 
            wurde ein Setup für den schwierigsten Fall (Worst Case) gewählt, um Fischverlust zu vermeiden.
        </div>
    """, unsafe_allow_html=True)

# Layout aufteilen: Links Hardware, Rechts Begründungen & Spot
col_links, col_rechts = st.columns([1.2, 1.8])

with col_links:
    st.subheader("📦 Hardware-Spezifikation")
    
    # Blei-Sektion
    with st.expander("⚓ Bleisystem & Montage", expanded=True):
        st.success(f"**Montage:** {res['blei_typ']}")
        st.info(f"**Blei:** {res['blei_gewicht']}g ({res['blei_form']})")
        st.write(f"**Leader:** {res['leader']}")

    # Vorfach-Sektion
    with st.expander("🪝 Vorfach & Rig-Typ", expanded=True):
        st.warning(f"**Material:** {res['vorfach_material']}")
        st.write(f"**Länge:** {res['vorfach_laenge']}")
        st.write(f"**Rig:** {res['rig_typ']}")
        st.write(f"**Präsentation:** {res['koeder_praesentation']}")

    # Haken-Sektion (Neu mit allen Zusatzparametern)
    with st.expander("⚙️ Haken-Details", expanded=True):
        st.error(f"**Modell:** {res['haken_typ']}")
        st.write(f"📍 **Spitze:** {res['h_spitze']}")
        st.write(f"👁️ **Öhr:** {res['h_oehr']}")
        st.write(f"💪 **Draht:** {res['h_draht']}")

    # Futter-Sektion
    with st.expander("🥣 Futter-Strategie", expanded=True):
        st.write(f"**Menge:** {res['futter_menge']}")
        st.write(f"**Köder:** {res['futter_art']}")

with col_rechts:
    st.subheader("🧐 Taktische Begründungen (Das 'Warum')")
    # Alle gesammelten Begründungen aus den Modulen anzeigen
    for begrue in res['begruendungen']:
        st.markdown(f'<div class="taktik-detail">{begrue}</div>', unsafe_allow_html=True)
    
    st.subheader("🗺️ Lokalisierung: Spot-Empfehlung")
    st.markdown(f'<div class="spot-empfehlung">📍 {res["spot_analyse"]}</div>', unsafe_allow_html=True)

# Finaler Haftungsausschluss
st.divider()
st.info("""
    💡 **Orientierungshilfe:** Die hier getroffenen Empfehlungen basieren auf den eingegebenen Daten und 
    dienen als taktische Orientierung. Da jedes Gewässer seine eigenen Gesetze hat, solltest du dein Rig, 
    Vorfach, Leader und Blei immer an die tatsächlichen Gegebenheiten vor Ort anpassen.
""")

st.caption("Karpfen-Rig-Konfigurator v6.0 | Profi-Modul für Haken-Mechanik")
    # --- KORREKTUR: MONTAGEN-LOGIK (Heli-Safe & Strömungs-Physik) ---

    # 1. Logik: Heli-Safe System
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"
        s["rig_typ"] = "Helikopter-Rig"
        s["begruendungen"].append(
            "➔ **Warum Heli-Safe?** Bei weichem Boden oder Kraut sinkt das Blei ein. Das Heli-Safe System ermöglicht es dem Vorfach, auf dem Leader nach oben zu gleiten, "
            "sodass der Köder frei präsentiert bleibt. Gleichzeitig bietet es die Sicherheit, dass das Blei im Drill oder bei einem Hänger ausgeklinkt wird, "
            "was bei Helikopter-Montagen sonst oft ein Problem darstellt."
        )

    # 2. Logik: Strömungs-Physik (Das "Warum" der Krallen)
    if stroemung in ["Mittel", "Stark"]:
        s["blei_form"] = "Krallenblei (Gripper)"
        s["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        s["begruendungen"].append(
            f"➔ **Warum Gripper-Blei?** Bei {stroemung}er Strömung bietet ein glattes Blei zu wenig Reibungswiderstand und würde über den Grund rollen. "
            "Die Krallen (Gripper) verankern das Blei physisch im Boden, wodurch die Montage fixiert wird. Nur so bleibt der Köder präzise am Spot liegen "
            "und der Selbsthakeffekt wird durch den festen Widerstand des verankerten Bleis erst ermöglicht."
        )

    # 3. Logik: Safety-Clip (Wann und Warum?)
    if s["blei_typ"] == "Safety-Clip Montage" and any(h in ["Totholz", "Muschelbänke"] for h in hindernisse):
        s["begruendungen"].append(
            "➔ **Warum Safety-Clip?** In Hindernissen ist der Safety-Clip nötig, weil er als Sollbruchstelle fungiert. Sobald das Blei hängen bleibt, "
            "hebelt der Clip das Blei ab. Ohne diesen Mechanismus würde das Blei als Anker wirken und zum Abriss der Hauptschnur führen."
        )

    # 4. Logik: Wurf-Taktik (Das "Warum" des Winkels)
    if stroemung != "Keine":
        s["begruendungen"].append(
            "➔ **Warum im Winkel mit der Strömung werfen?** Wenn du gegen den Strom wirfst, drückt der Wasserdruck die Schnur und das Vorfach "
            "zurück über das Blei und die Hauptschnur. Dies führt fast immer zu Verwicklungen. Wirfst du mit oder schräg zur Strömung, "
            "streckt der Wasserdruck das Vorfach sauber vom Blei weg."
        )
