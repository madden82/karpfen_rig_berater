import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen Rig & Blei Experte", layout="wide")

st.markdown("""
    <style>
    .stSlider { padding-bottom: 20px; }
    .stHeader { font-size: 1.5rem !important; }
    .taktik-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Karpfen Rig & Blei Empfehlung")

# ==========================================
# 1. PHASE: GEWÄSSER & UMWELT
# ==========================================
st.header("📍 Schritt 1: Gewässer & Umwelt")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp wählen", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Aktuelle Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    tiefe_spot = st.number_input("Tiefe an deinem Angelplatz (m)", 0.5, 40.0, 3.0, step=0.1)

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit wählen", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)"])
    hindernisse = st.multiselect("Hindernisse / Gefahren am Platz", [
        "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse"
    ])

with c3:
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Mittel", "Klar", "Glasklar"])
    stroemung = st.select_slider("Strömung / Zug", options=["Keine", "Leicht", "Mittel", "Stark"])
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)

# ==========================================
# 2. PHASE: TAKTIK & BESTAND
# ==========================================
st.header("🎯 Schritt 2: Taktik & Fischbestand")
t1, t2 = st.columns(2)

with t1:
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Wurfweite (m)", 0, 180, 50) if ausbringung != "Boot" else 0

with t2:
    aktivitaet = st.select_slider("Aktivität der Karpfen", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Max. erwartetes Karpfengewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE (LOGIK)
# ==========================================

def berechne_blei_logik():
    blei_setup = {
        "typ": "Blei mit Wirbel & Safety Clip",
        "gewicht": 90,
        "form": "Birnenform / Torpedo",
        "hinweis": ""
    }
    
    taktik_tipps = []

    # 1. Logik: Vorsichtige Fische & Hindernisse
    if aktivitaet == "Vorsichtig":
        if not hindernisse:
            blei_setup["typ"] = "Inline-Blei (fest)"
            taktik_tipps.append("⚠️ **Inline-Blei bevorzugt:** Da kaum Hindernisse vorhanden sind, bietet das Inline-Blei den direktesten Widerstand bei vorsichtigen Fischen.")
        else:
            blei_setup["typ"] = "Inline-Blei mit Sicherheitsclip"
            taktik_tipps.append("⚠️ **Safety Inline:** Bei vorsichtigen Fischen im Holz/Kraut nutzt du den Sicherheitsclip, damit das Blei bei Hängern abfällt.")

    # 2. Logik: Bodenbeschaffenheit
    if boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        blei_setup["typ"] = "Helikopter-Montage (Blei vorne)"
        blei_setup["form"] = "Flaches Tellermeißel / Square-Lead"
        taktik_tipps.append("☁️ **Schlamm-Taktik:** Helikopter-Rigs verhindern das Einsinken des Vorfachs. Benutze Bleie mit viel Fläche.")
        if wurfweite > 80:
            taktik_tipps.append("🚀 **Wurf-Tipp:** Helikopter-Montagen sind am aerodynamischsten für Weitwürfe.")
        
        # Köder-Tipp für Schlamm
        taktik_tipps.append("🍦 **Präsentation:** Nutze ein Pop-Up oder Schneemann-Rig, um den Köder perfekt über dem Schlamm zu halten.")

    elif boden_struktur in ["Sand / Kies (hart)", "Lehm (fest)"]:
        blei_setup["typ"] = "Safety-Clip Montage (Standard)"
        blei_setup["form"] = "Kantiges Blei (Gripper)"

    # 3. Logik: Strömung
    if stroemung in ["Mittel", "Stark"]:
        blei_setup["form"] = "Krallenblei / Big Gripper"
        blei_setup["gewicht"] = 140
        taktik_tipps.append("🌊 **Strömungs-Regel:** Niemals gegen die Strömung werfen! Wirf im Winkel mit der Strömung, damit das Vorfach nicht in die Hauptschnur gedrückt wird und verheddert.")

    # Gewichts-Anpassung nach Wurfweite
    if wurfweite > 100:
        blei_setup["gewicht"] = 120
        blei_setup["form"] = "Distance Lead (Projektilform)"

    return blei_setup, taktik_tipps

# Berechnungen ausführen
blei_ergebnis, tipps = berechne_blei_logik()

# ==========================================
# 4. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein optimiertes Setup")

o1, o2 = st.columns(2)

with o1:
    st.subheader("📦 Empfohlene Blei-Montage")
    st.info(f"**System:** {blei_ergebnis['typ']}")
    st.write(f"**Blei-Form:** {blei_ergebnis['form']}")
    st.metric("Empf. Gewicht", f"{blei_ergebnis['gewicht']} g")

with o2:
    st.subheader("💡 Taktische Informationen")
    if tipps:
        for tipp in tipps:
            st.markdown(tipp)
    else:
        st.write("Keine besonderen taktischen Anpassungen für diese Bedingungen nötig.")

st.markdown("---")
st.caption("Dieses Programm berechnet Empfehlungen basierend auf modernen Karpfenangel-Standards.")
