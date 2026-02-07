import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-Taktik Berater Pro", layout="wide")

st.title("🎖️ Karpfen-Taktik Berater Pro")
st.caption("Präzisions-Einsatzplanung v3.6 | Mit taktischer Entscheidungs-Analyse")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp wählen", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Angelplatz (m)", 0.5, 40.0, 4.0)
    
    stromung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stromung = st.select_slider("Strömungsdruck wählen", options=["Keine", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit wählen", 
                                 ["Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig / weich)"])
    
    hindernisse = st.multiselect("Hindernisse / Gefahren am Platz", [
        "Muschelbänke (scharfkantig)", 
        "Totholz / Versunkene Bäume", 
        "Kraut (vereinzelt)", 
        "Kraut-Dschungel (dicht)",
        "Fadenalgen",
        "Scharfe Kanten / Steinpackung",
        "Zivilisationsmüll (Draht / Unrat)",
        "Seerosenfelder",
        "Krebse / Wollhandkrabben",
        "Starker Schiffsverkehr"
    ], placeholder="Bitte wählen...")

with c3:
    st.markdown("**Umweltfaktoren**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Mittel", "Klar", "Glasklar"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leichte Brise", "Mäßiger Wind", "Starker Wind"])
    temp = st.slider("Wassertemperatur (°C)", 2, 30, 15)

# ==========================================
# 2. PHASE: TAKTIK & BESTAND
# ==========================================
st.header("🎯 Schritt 2: Taktik & Fischbestand")
t1, t2 = st.columns(2)

wurfweite = 0
taktik_typ = "Ablegen"

with t1:
    ausbringungs_methode = st.radio("Ausbringung wählen", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    if ausbringungs_methode == "Boot":
        boot_taktik = st.radio("Taktik vom Boot:", ["Vom Boot ablegen", "Vom Boot werfen"], horizontal=True)
        if boot_taktik == "Vom Boot werfen":
            taktik_typ = "Wurf"
            wurfweite = st.slider("Benötigte Wurfweite (m)", 5, 100, 30)
    elif ausbringungs_methode == "Wurf vom Ufer":
        taktik_typ = "Wurf"
        wurfweite = st.slider("Benötigte Wurfweite (m)", 10, 180, 70)

with t2:
    st.markdown("**Fischbestand & Aktivität**")
    weissfisch_aufkommen = st.select_slider("Weißfisch-Aufkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität (Karpfen)", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Erwartetes Fischgewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE & LOGIK-ERKLÄRUNG
# ==========================================

def berechne_taktik_mit_begruendung():
    setup = {
        "rig": "Haar-Rig (Hair Rig)",
        "haken": "4 bis 6",
        "blei": 95,
        "montage": "Safety Clip",
        "material": "Ummanteltes Geflecht (25lb)",
        "laenge": 18,
        "begruendung": []
    }

    # 1. Rig-Wahl Begründung
    if any("Kraut" in h for h in hindernisse) or boden_struktur == "Moder (faulig / weich)":
        setup["rig"] = "Ronnie-Rig / Chod-Rig"
        setup["begruendung"].append("➔ **Rig:** Pop-Up Montage gewählt, damit der Köder nicht im Kraut/Modder versinkt und sichtbar bleibt.")
    elif wasser_klarheit == "Glasklar":
        setup["rig"] = "D-Rig (Fluorocarbon)"
        setup["begruendung"].append("➔ **Rig:** D-Rig mit FC gewählt, da die Fische bei hoher Sichtweite herkömmliche Geflechte leichter wahrnehmen.")
    else:
        setup["begruendung"].append("➔ **Rig:** Klassisches Haar-Rig gewählt, da der Boden sauber ist und die Mechanik hier am zuverlässigsten arbeitet.")

    # 2. Blei & Montage Begründung
    if stromung != "Keine" or "Starker Schiffsverkehr" in hindernisse:
        setup["blei"] = 240 if stromung == "Stark" else 140
        setup["montage"] = "Grippa-Inliner oder schwerer Safety-Clip"
        setup["begruendung"].append(f"➔ **Blei:** Erhöht auf {setup['blei']}g, um den Montagen-Sitz bei Strömungsdruck/Sog stabil zu halten.")
    elif taktik_typ == "Wurf" and wurfweite > 100:
        setup["blei"] = 115
        setup["montage"] = "Helicopter-System"
        setup["begruendung"].append("➔ **Montage:** Helicopter-System gewählt, um Verwicklungen im Weitwurf physikalisch auszuschließen.")

    # 3. Material & Schutz Begründung
    if any(s in str(hindernisse) for s in ["Muschel", "Kante", "Holz", "Müll"]):
        setup["material"] = "Fluorocarbon-Schlagschnur (50lb+) / Abriebfest"
        setup["haken"] = "2 bis 4 (Dickdrahtig)"
        setup["begruendung"].append("➔ **Schutz:** Dickdrahtige Haken und Schlagschnur gewählt, um Fischverluste durch scharfe Kanten oder Hindernis-Fluchten zu verhindern.")

    return setup

ergebnis = berechne_taktik_mit_begruendung()

# ==========================================
# 4. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup")

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Montage & Blei")
    st.metric("Bleigewicht", f"{ergebnis['blei']} g")
    st.write(f"**System:** {ergebnis['montage']}")

with o2:
    st.subheader("🪝 Rig & Haken")
    st.success(f"**Typ:** {ergebnis['rig']}")
    st.write(f"**Material:** {ergebnis['material']}")
    st.write(f"**Haken:** Gr. {ergebnis['haken']}")

with o3:
    st.subheader("💡 Taktische Analyse (Warum?)")
    for punkt in ergebnis["begruendung"]:
        st.write(punkt)

st.divider()
# Futter-Bereich (vereinfacht für Fokus auf Begründung)
st.subheader("🥣 Futter-Empfehlung")
if weissfisch_aufkommen in ["Hoch", "Extrem"]:
    st.warning("Selektive Fütterung: Nur harte Boilies verwenden (wegen Weißfisch-Konkurrenz).")
else:
    st.info("Attraktive Fütterung: Partikel-Mix und Pellets möglich (wenig Konkurrenz).")
