import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-RIG Empfehlung", layout="wide")

st.markdown("""
    <style>
    .stSelectbox, .stSlider { margin-bottom: 15px; }
    .hinweis-box { 
        background-color: #e8f4fd; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #2196f3; margin-bottom: 25px;
    }
    .worst-case-warnung {
        background-color: #fff4e5; padding: 10px; border-radius: 5px;
        border: 1px solid #ffa000; color: #663c00; font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎖️ Karpfen-Rig-Konfigurator")

st.markdown("""
    <div class="hinweis-box">
        <strong>💡 Profi-Tipp:</strong> Je mehr Details du angibst, desto präziser wird das Rig. 
        Bei Unsicherheit frage den <strong>Gewässereigentümer</strong>. 
        Wählst du <em>'Weiß ich nicht'</em>, plant das Tool automatisch mit dem <strong>Worst Case</strong>.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 1. PHASE: GEWÄSSER & UMWELT
# ==========================================
st.header("📍 Schritt 1: Gewässer & Umwelt")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    jahreszeit = st.selectbox("Jahreszeit", ["Frühjahr", "Sommer", "Herbst", "Winter"])
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=4)

with c2:
    hindernisse = st.multiselect("Hindernisse am Platz", 
                                ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Weiß ich nicht"], 
                                default="Weiß ich nicht")
    stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"])
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Mittel", "Klar", "Glasklar"])

with c3:
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15)
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leicht", "Mittel", "Stark"])
    windrichtung = "Windstill"
    if windstärke != "Windstill":
        windrichtung = st.selectbox("Windrichtung zum Spot", ["Gegenwind", "Rückenwind", "Seitenwind"])

# ==========================================
# 2. PHASE: TAKTIK & BESTAND
# ==========================================
st.header("🎯 Schritt 2: Taktik & Fischbestand")
t1, t2 = st.columns(2)

with t1:
    ausbringung = st.radio("Ausbringungsmethode", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    wurfweite = st.slider("Wurfweite (m)", 0, 180, 60) if ausbringung != "Boot" else 0
    weissfisch = st.select_slider("Weißfischaufkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"])

with t2:
    aktivitaet = st.select_slider("Fischverhalten / Aktivität", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Max. erwartetes Karpfengewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-LOGIK
# ==========================================

def berechne_pro_logic():
    setup = {
        "rig": "Haar-Rig (Standard)",
        "blei_typ": "Safety-Clip Montage",
        "blei_form": "Birnenform (Smooth)",
        "blei_gewicht": 95,
        "haken": "Gr. 4-6",
        "vorfach": "Ummanteltes Geflecht",
        "taktik": [],
        "unsicher": False
    }

    # --- BLEI & BODEN ---
    if boden_struktur == "Weiß ich nicht" or boden_struktur in ["Schlamm (weich)", "Moder (faulig)"]:
        if boden_struktur == "Weiß ich nicht": setup["unsicher"] = True
        setup["blei_form"] = "Flaches Flächenblei (Flat Pear)"
        setup["blei_gewicht"] = 70
        setup["rig"] = "Helikopter-System (Köder: Pop-Up / Schneemann)"
        setup["taktik"].append("☁️ **Schlamm-Logik:** Wir nutzen Flächenbleie und Helikopter-Rigs, damit nichts im Grund versinkt.")

    # --- HINDERNISSE & SICHERHEIT ---
    if "Weiß ich nicht" in hindernisse or any(h in ["Totholz", "Muschelbänke", "Scharfe Kanten"] for h in hindernisse):
        if "Weiß ich nicht" in hindernisse: setup["unsicher"] = True
        setup["blei_typ"] = "Safety-Clip (Blei verlierend)"
        setup["haken"] = "Gr. 2-4 (Starkdrahtig)"
        setup["vorfach"] = "Mono-Schlagschnur + Snag-Link"
        setup["taktik"].append("🛡️ **Sicherheit:** Bei Hindernisgefahr muss das Blei im Drill sofort abfallen.")

    # --- SCHEUE FISCHE (INLINE) ---
    if aktivitaet in ["Weiß ich nicht", "Vorsichtig"]:
        if aktivitaet == "Weiß ich nicht": setup["unsicher"] = True
        if "Keine" in hindernisse or not hindernisse:
            setup["blei_typ"] = "Inline-Blei (Festmontage)"
            setup["taktik"].append("🤫 **Silent:** Bei scheuen Fischen bietet das Inline-Blei den besten Selbsthak-Effekt.")
        else:
            setup["blei_typ"] = "Inline-Blei mit Sicherheitsclip"
            setup["taktik"].append("⚠️ **Inline-Sicherheit:** Kombiniert Tarnung mit Schutz vor Hängern.")

    # --- STRÖMUNG (GRIPPER & WINKEL) ---
    if stroemung in ["Mittel", "Stark"]:
        setup["blei_form"] = "Krallenblei (Gripper)"
        setup["blei_gewicht"] = 140
        setup["taktik"].append("🌊 **Strömung:** Wirf nie gegen die Strömung! Der Druck schiebt sonst den Köder in die Hauptschnur.")

    # --- WIND & TEMPERATUR ---
    if windrichtung == "Gegenwind":
        setup["taktik"].append("🌬️ **Wind-Tipp:** Der Wind drückt Nahrung ans Ufer. Such den Spot im ufernahen Bereich!")
    if temp < 8:
        setup["haken"] = "Gr. 8-10 (Sehr fein)"
        setup["taktik"].append("❄️ **Kaltwasser:** Wenig Futter, kleine Köder und feinste Haken verwenden.")

    return setup

ergebnis = berechne_pro_logic()

# ==========================================
# 4. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup")

if ergebnis["unsicher"]:
    st.markdown('<div class="worst-case-warnung">⚠️ Hinweis: Da Parameter unbekannt sind, wurde ein Sicherheits-Setup für den Worst Case gewählt.</div>', unsafe_allow_html=True)

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Blei & Montage")
    st.metric("Bleigewicht", f"{ergebnis['blei_gewicht']} g")
    st.success(f"**Typ:** {ergebnis['blei_typ']}")
    st.write(f"**Form:** {ergebnis['blei_form']}")

with o2:
    st.subheader("🪝 Rig & Haken")
    st.success(f"**Rig:** {ergebnis['rig']}")
    st.write(f"**Haken:** {ergebnis['haken']}")
    st.write(f"**Vorfach:** {ergebnis['vorfach']}")

with o3:
    st.subheader("💡 Taktische Infos")
    for t in ergebnis['taktik']:
        st.markdown(f"- {t}")

st.markdown("---")
# Futtermenge Logik
f_menge = "0.5 - 1kg" if temp > 15 else "Händevoll"
if weissfisch == "Extrem": f_menge = "3kg+ (Große Köder)"
st.write(f"**Empfohlene Futterstrategie:** {f_menge} | Fokus: {'Harte Boilies' if weissfisch in ['Hoch', 'Extrem'] else 'Mix'}")
