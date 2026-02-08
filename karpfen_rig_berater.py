import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen Profi-Taktik", layout="wide")

st.markdown("""
    <style>
    .hinweis-box { 
        background-color: #e8f4fd; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #2196f3; margin-bottom: 25px;
    }
    .worst-case-warnung {
        background-color: #fff4e5; padding: 10px; border-radius: 5px;
        border: 1px solid #ffa000; color: #663c00; font-size: 0.9rem; margin-bottom: 10px;
    }
    .taktik-detail {
        background-color: #f8f9fa; padding: 10px; border-radius: 5px;
        border-left: 3px solid #2e7d32; margin-bottom: 10px; font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Der Ultimative Karpfen-Rig-Konfigurator")

st.markdown("""
    <div class="hinweis-box">
        <strong>💡 Profi-Tipp:</strong> Je präziser die Parameter, desto besser das Rig. 
        Solltest du Informationen nicht haben, frage den <strong>Gewässereigentümer</strong>. 
        Bei <em>'Weiß ich nicht'</em> plant das System mit dem <strong>Worst Case</strong> (Sicherheits-Setup).
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 1. PHASE: EINGABEMASKE
# ==========================================
st.header("📍 Schritt 1: Gegebenheiten am Spot")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    
    # Dynamische Strömung
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=4)
    
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Keine Hindernisse", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"], 
                                default="Weiß ich nicht")

with c3:
    aktivitaet = st.select_slider("Fischverhalten / Aktivität (Beißlust)", 
                                  options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    weissfisch = st.select_slider("Vorkommen anderer Weißfische (Brassen, Rotaugen etc.)", 
                                  options=["Niedrig", "Mittel", "Hoch", "Extrem", "Weiß ich nicht"], value="Weiß ich nicht")
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Wurfweite (m)", 0, 180, 60) if ausbringung != "Boot" else 0

# ==========================================
# 2. PHASE: EXPERTEN-LOGIK & BEGRÜNDUNG
# ==========================================

def berechne_pro_logic():
    setup = {
        "blei_typ": "Safety-Clip Montage",
        "blei_form": "Birnenform (Smooth)",
        "blei_gewicht": 95,
        "rig": "Haar-Rig (Standard)",
        "futter_menge": "",
        "futter_art": "Mix aus Boilies & Pellets",
        "begruendungen": [],
        "unsicher": False
    }

    # --- BLEI-LOGIK ---
    # Schlamm / Unbekannt
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        if boden_struktur == "Weiß ich nicht": setup["unsicher"] = True
        setup["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        setup["blei_gewicht"] = 75
        setup["rig"] = "Helikopter-System (Pop-Up / Schneemann)"
        setup["begruendungen"].append("➔ **Blei:** Ein flaches Flächenblei sinkt weniger tief in weichen Boden ein als kompakte Formen.")
        setup["begruendungen"].append("➔ **Rig:** Helikopter gewählt, damit das Rig auf dem Leader nach oben gleiten kann, wenn das Blei im Schlamm versinkt.")

    # Strömung
    if stroemung in ["Mittel", "Stark"]:
        setup["blei_form"] = "Krallenblei (Gripper)"
        setup["blei_gewicht"] = 160
        setup["begruendungen"].append("➔ **Strömung:** Gripper-Bleie krallen sich in den Boden. Wichtig: Nicht gegen die Strömung werfen, um Verhedderungen zu vermeiden!")

    # Vorsichtige Fische & Hindernisse
    if aktivitaet in ["Weiß ich nicht", "Vorsichtig"]:
        if aktivitaet == "Weiß ich nicht": setup["unsicher"] = True
        if "Keine Hindernisse" in hindernisse:
            setup["blei_typ"] = "Inline-Blei (Fest)"
            setup["begruendungen"].append("➔ **Scheu:** Inline-Bleie bieten den direktesten Widerstand beim Ansaugen, ideal für vorsichtige Fische im hindernisfreien Wasser.")
        else:
            setup["blei_typ"] = "Inline-Blei mit Sicherheitsclip"
            setup["begruendungen"].append("➔ **Sicherheit:** Inline-System mit Clip gewählt, um Tarnung bei scheuen Fischen mit Schutz vor Hängern zu kombinieren.")

    # Weitwurf
    if wurfweite > 90 and setup["rig"] != "Helikopter-System":
        setup["blei_typ"] = "Helikopter-System"
        setup["begruendungen"].append("➔ **Wurfweite:** Das Helikopter-System bietet die besten Flugeigenschaften und verhindert Tangles bei weiten Würfen.")

    # --- FUTTER-LOGIK ---
    menge_basis = 0.5 # kg pro Tag
    if temp > 18: menge_basis = 2.0
    if temp < 10: menge_basis = 0.2
    
    if weissfisch in ["Hoch", "Extrem", "Weiß ich nicht"]:
        if weissfisch == "Weiß ich nicht": setup["unsicher"] = True
        setup["futter_art"] = "Große, harte Boilies (selektiv)"
        menge_basis *= 2
        setup["begruendungen"].append("➔ **Weißfische:** Da viele Beifänge zu erwarten sind (oder Bestand unbekannt), nutzen wir mehr und härteres Futter zur Selektion.")
    
    setup["futter_menge"] = f"{round(menge_basis, 1)} kg pro Tag/Rute"

    return setup

ergebnis = berechne_pro_logic()

# ==========================================
# 3. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup & Begründung")

if ergebnis["unsicher"]:
    st.markdown('<div class="worst-case-warnung">⚠️ Hinweis: Da einige Parameter unbekannt sind, wurde ein Sicherheits-Setup für den Worst Case gewählt.</div>', unsafe_allow_html=True)

o1, o2 = st.columns([1, 2])

with o1:
    st.subheader("📦 Hardware")
    st.metric("Bleigewicht", f"{ergebnis['blei_gewicht']} g")
    st.success(f"**Montage:** {ergebnis['blei_typ']}")
    st.info(f"**Bleiform:** {ergebnis['blei_form']}")
    st.write(f"**Rig:** {ergebnis['rig']}")
    
    st.subheader("🥣 Futter")
    st.write(f"**Menge:** {ergebnis['futter_menge']}")
    st.write(f"**Art:** {ergebnis['futter_art']}")

with o2:
    st.subheader("🧐 Taktische Begründung")
    for b in ergebnis['begruendungen']:
        st.markdown(f'<div class="taktik-detail">{b}</div>', unsafe_allow_html=True)

st.divider()
st.warning("⚠️ **Wichtiger Hinweis:** Diese Empfehlungen basieren auf den eingegebenen Daten und Erfahrungswerten. Da jedes Gewässer seine eigenen, speziellen Bedingungen hat, dient dies nur als Orientierungshilfe. Bitte passe dein Rig, Vorfach, Leader und Blei immer an die tatsächlichen Gegebenheiten vor Ort an.")

st.caption("Karpfen-Rig-Konfigurator v3.0 | Taktik & Logik")
