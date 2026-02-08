import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen Rig & Blei Experte", layout="wide")

st.markdown("""
    <style>
    .stSlider { padding-bottom: 20px; }
    .stHeader { font-size: 1.5rem !important; }
    .taktik-box { 
        background-color: #f9f9f9; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7d32;
        margin-top: 10px;
    }
    .metric-container {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Profi-Karpfen-Taktik & Rig-Konfigurator")

# ==========================================
# 1. PHASE: EINGABE (GEWÄSSER & TAKTIK)
# ==========================================
st.header("📍 Schritt 1: Bedingungen am Spot")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)"])

with c2:
    hindernisse = st.multiselect("Hindernisse am Platz", [
        "Keine", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse"
    ], default="Keine")
    stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    aktivitaet = st.select_slider("Fischverhalten", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])

with c3:
    ausbringung = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Benötigte Distanz (m)", 0, 180, 60) if ausbringung != "Boot" else 0
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)

# ==========================================
# 2. PHASE: EXPERTEN-LOGIK
# ==========================================

def berechne_setup():
    # Standard-Werte
    setup = {
        "rig": "Haar-Rig (Standard)",
        "blei_typ": "Safety-Clip Montage",
        "blei_form": "Birnenform (Smooth)",
        "blei_gewicht": 90,
        "haken": "Gr. 4-6",
        "vorfach": "Ummanteltes Geflecht",
        "taktik": []
    }

    # --- BLEI & MONTAGE LOGIK (Basierend auf deinen Vorgaben) ---
    
    # 1. Fokus: Vorsichtige Fische & Hindernisse
    if aktivitaet == "Vorsichtig":
        if "Keine" in hindernisse or not hindernisse:
            setup["blei_typ"] = "Inline-Blei (Festmontage)"
            setup["blei_form"] = "Kompaktes Inline-Blei"
            setup["taktik"].append("🤫 **Tarn-Modus:** Bei scheuen Fischen ohne Hindernisse nutzen wir Inline-Bleie für den direktesten Hakeffekt.")
        else:
            setup["blei_typ"] = "Inline-Blei mit Sicherheitsclip"
            setup["taktik"].append("⚠️ **Sicherheits-Inline:** Vorsichtige Fische am Holz/Kraut? Inline-System mit Clip nutzen, damit das Blei im Notfall abfällt.")

    # 2. Fokus: Bodenbeschaffenheit (Schlamm/Weich)
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        setup["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        setup["blei_gewicht"] = 70
        setup["rig"] = "Helikopter-Rig mit Pop-Up / Schneemann"
        setup["taktik"].append("☁️ **Schlamm-Spezial:** Verzicht auf Weite, dafür ein Flächenblei nutzen, damit es nicht einsinkt.")
        setup["taktik"].append("🍦 **Präsentation:** Der Köder muss als Pop-Up oder Schneemann präsentiert werden, um über dem Schlamm zu arbeiten.")
        if wurfweite > 70:
            setup["blei_typ"] = "Helikopter-System"
            setup["taktik"].append("🚀 **Weitwurf-Schlamm:** Helikopter-Montage gewählt, da das Blei vorne sitzt und das Rig beim Wurf nicht verheddert.")

    # 3. Fokus: Strömung (Gripper Logik)
    if stroemung in ["Mittel", "Stark"] or gewaesser_typ in ["Fluss", "Strom"]:
        setup["blei_form"] = "Krallenblei (Gripper Lead)"
        setup["blei_gewicht"] = 140 if stroemung == "Mittel" else 180
        setup["taktik"].append("🌊 **Strömungs-Regel:** Krallenblei hält die Montage am Platz. **Wichtig:** Nicht gegen die Strömung werfen! Sonst drückt der Wasserdruck den Köder in die Hauptschnur.")

    # 4. Fokus: Hindernisse & Haken
    if any(h in ["Muschelbänke", "Totholz", "Scharfe Kanten"] for h in hindernisse):
        setup["haken"] = "Gr. 2-4 (Dickdrahtig)"
        setup["vorfach"] = "Mono-Schlagschnur + Snag-Link"
        if setup["blei_typ"] == "Safety-Clip Montage":
            setup["taktik"].append("🛡️ **Snag-Taktik:** Safety-Clip so einstellen, dass das Blei bei Kontakt sofort ausklinkt.")

    return setup

# Berechnung starten
res = berechne_setup()

# ==========================================
# 3. PHASE: AUSGABE (UI)
# ==========================================
st.divider()
st.header("🏁 Dein optimiertes Setup")

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Blei-System")
    st.metric("Gewicht", f"{res['blei_gewicht']} g")
    st.success(f"**Typ:** {res['blei_typ']}")
    st.info(f"**Form:** {res['blei_form']}")

with o2:
    st.subheader("🪝 Rig & Haken")
    st.success(f"**Rig:** {res['rig']}")
    st.write(f"**Haken:** {res['haken']}")
    st.write(f"**Material:** {res['vorfach']}")

with o3:
    st.subheader("💡 Taktik-Hinweise")
    for tipp in res['taktik']:
        st.markdown(tipp)

# Dynamische Futter-Empfehlung
st.markdown("---")
st.subheader("🥣 Futter-Strategie")
f_menge = "Gering (Attraktion)" if temp < 10 else "Mittel (Platzaufbau)"
if temp > 20 or jahreszeit == "Herbst": f_menge = "Hoch (Futterplatz)"

st.write(f"**Menge:** {f_menge} | **Art:** {'Partikel & kleine Pellets' if temp < 12 else 'Boilies & Tigernüsse'}")

st.caption("Hinweis: Diese Empfehlungen basieren auf deinen Angaben. Jedes Gewässer hat eigene Gesetze – bleib flexibel!")
