import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-RIG Empfehlung", layout="wide")

st.markdown("""
    <style>
    .stSelectbox, .stSlider { margin-bottom: 15px; }
    .hinweis-box { 
        background-color: #e8f4fd; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #2196f3;
        margin-bottom: 25px;
    }
    .worst-case-warnung {
        background-color: #fff4e5;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ffa000;
        color: #663c00;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Karpfen-Experte: Blei & Rig-Konfigurator")

# --- NEU: EXPERTEN-HINWEIS GANZ OBEN ---
st.markdown("""
    <div class="hinweis-box">
        <strong>💡 Profi-Tipp für maximale Genauigkeit:</strong><br>
        Je präziser du die Parameter unten ausfüllst, desto exakter wird die Rig-Empfehlung. 
        Solltest du dir bei Boden oder Hindernissen unsicher sein, frage am besten den 
        <strong>Gewässereigentümer oder lokale Angler</strong>. 
        Bei der Auswahl <em>'Weiß ich nicht'</em> konfiguriert das Programm automatisch ein 
        <strong>Sicherheits-Setup</strong> für den schwierigsten Fall (Worst Case).
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 1. PHASE: EINGABE
# ==========================================
st.header("📍 Schritt 1: Gegebenheiten am Spot")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"],
                                 index=4)

with c2:
    hindernisse = st.multiselect("Hindernisse am Platz", [
        "Keine", "Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"
    ], default="Weiß ich nicht")
    
    stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])

with c3:
    aktivitaet = st.select_slider("Fischverhalten / Aktivität", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Benötigte Distanz (m)", 0, 180, 60) if ausbringung != "Boot" else 0

# ==========================================
# 2. PHASE: LOGIK-ENGINE
# ==========================================

def berechne_setup():
    setup = {
        "rig": "Haar-Rig (Standard)",
        "blei_typ": "Safety-Clip Montage",
        "blei_form": "Birnenform (Smooth)",
        "blei_gewicht": 90,
        "haken": "Gr. 4-6",
        "vorfach": "Ummanteltes Geflecht",
        "taktik": [],
        "unsicher": False
    }

    # --- BODEN LOGIK ---
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        if boden_struktur == "Weiß ich nicht": setup["unsicher"] = True
        setup["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        setup["blei_gewicht"] = 75
        setup["rig"] = "Helikopter-System mit Pop-Up / Schneemann"
        setup["taktik"].append("☁️ **Boden-Taktik:** Da wir von weichem Grund ausgehen, nutzen wir Flächenbleie gegen das Einsinken.")
        setup["taktik"].append("🍦 **Präsentation:** Pop-Up oder Schneemann-Rig verwenden, damit der Köder nicht im Schlamm verschwindet.")

    # --- HINDERNIS LOGIK ---
    if "Weiß ich nicht" in hindernisse or any(h in ["Totholz", "Muschelbänke", "Scharfe Kanten"] for h in hindernisse):
        if "Weiß ich nicht" in hindernisse: setup["unsicher"] = True
        setup["blei_typ"] = "Safety-Clip (Blei verlierend eingestellt)"
        setup["haken"] = "Gr. 2-4 (Starkdrahtig)"
        setup["taktik"].append("🛡️ **Sicherheit:** Da Hindernisse möglich sind, wird ein Safety-Clip genutzt. Das Blei muss bei einem Hänger sofort abfallen.")

    # --- AKTIVITÄTS LOGIK ---
    if aktivitaet in ["Weiß ich nicht", "Vorsichtig"]:
        if aktivitaet == "Weiß ich nicht": setup["unsicher"] = True
        if "Keine" in hindernisse or (not hindernisse):
            setup["blei_typ"] = "Inline-Blei (Festmontage)"
            setup["taktik"].append("🤫 **Tarnung:** Vorsichtige Fische im Freiwasser? Inline-Blei für maximalen Hak-Effekt nutzen.")
        elif any(h in ["Totholz", "Kraut"] for h in hindernisse) or "Weiß ich nicht" in hindernisse:
            setup["blei_typ"] = "Inline-Blei mit Sicherheitsclip"
            setup["taktik"].append("⚠️ **Kombi-Taktik:** Vorsichtige Fische + Hindernis-Gefahr = Inline-Blei mit Sicherheitsclip.")

    # --- STRÖMUNGS LOGIK ---
    if stroemung in ["Mittel", "Stark"]:
        setup["blei_form"] = "Krallenblei (Gripper)"
        setup["blei_gewicht"] = 140
        setup["taktik"].append("🌊 **Strömungs-Regel:** Wirf im Winkel mit der Strömung, niemals dagegen! Sonst verhakt sich der Köder in der Hauptschnur.")

    # --- WEITWURF / HELI ---
    if wurfweite > 90 and setup["rig"] != "Helikopter-System":
        setup["blei_typ"] = "Helikopter-System"
        setup["taktik"].append("🚀 **Weitwurf:** Das Blei sitzt vorne, was Verhedderungen beim Wurf fast ausschließt.")

    return setup

res = berechne_setup()

# ==========================================
# 3. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup")

if res["unsicher"]:
    st.markdown('<div class="worst-case-warnung">⚠️ Hinweis: Da einige Parameter unbekannt sind, wurde ein <b>Sicherheits-Setup für den schlechtesten Fall</b> berechnet.</div>', unsafe_allow_html=True)

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Blei-Montage")
    st.metric("Gewicht", f"{res['blei_gewicht']} g")
    st.info(f"**System:** {res['blei_typ']}")
    st.write(f"**Bleiform:** {res['blei_form']}")

with o2:
    st.subheader("🪝 Rig-Details")
    st.success(f"**Rig:** {res['rig']}")
    st.write(f"**Haken:** {res['haken']}")
    st.write(f"**Material:** {res['vorfach']}")

with o3:
    st.subheader("💡 Taktische Infos")
    for tipp in res['taktik']:
        st.markdown(f"- {tipp}")

st.markdown("---")
st.caption("Programm-Version 2.0 | Fokus: Blei-Sicherheit & Taktik")
