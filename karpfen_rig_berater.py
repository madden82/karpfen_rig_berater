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
        <strong>💡 Anwendungshinweis:</strong> Dieses Programm ist in Module unterteilt. 
        Fülle zuerst alle Parameter aus. Bei <em>'Weiß ich nicht'</em> wird automatisch das 
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

st.info("Kopiere nun **Teil 2 (Die Logik-Engine)** unter diesen Code.")
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
