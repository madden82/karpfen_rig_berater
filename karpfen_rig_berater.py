import streamlit as st

# =========================
# Setup & Design
# =========================
st.set_page_config(page_title="Karpfen-Taktik Berater Pro", layout="wide")

st.title("🎖️ Karpfen-Taktik Berater Pro")
st.caption("Präzisions-Einsatzplanung v3.4 | Inklusive Weißfisch- & Futter-Modul")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Angelplatz (m)", 0.5, 40.0, 4.0)
    
    stromung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stromung = st.select_slider("Strömungsdruck", options=["Keine", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
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
    ])

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
    ausbringungs_methode = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
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
    weissfisch_aufkommen = st.select_slider("Weißfisch-Aufkommen (Brassen/Rotaugen)", options=["Niedrig", "Mittel", "Hoch", "Extrem"])
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität (Karpfen)", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    ziel_gewicht = st.number_input("Erwartetes Fischgewicht (kg)", 5, 40, 15)

# ==========================================
# 3. PHASE: EXPERTEN-ENGINE
# ==========================================

def berechne_taktik(t_typ, w_weite, h_liste, w_aufkommen, f_aktiv, temp_v):
    setup = {
        "rig": "Haar-Rig (Hair Rig)",
        "haken_range": "4 bis 6",
        "blei_g": 95,
        "montage": "Safety Clip (Sicherheits-Clip)",
        "material_opt": "Ummanteltes Geflecht (25lb)",
        "material_alt": "Weiches Geflecht (20lb) + Anti-Tangle-Hülse",
        "laenge": 18,
        "koeder": "Standard Boilie (20mm)",
        "zusatz": "Standard-Leader"
    }

    # --- KÖDER-LOGIK (Weißfisch & Krebse) ---
    if w_aufkommen in ["Hoch", "Extrem"] or "Krebse / Wollhandkrabben" in h_liste:
        setup["koeder"] = "Harte Boilies (24mm+) oder gesicherte Köder (Tigerside)"
        setup["zusatz"] += " | Köderschutz (Shrink Tube / Mesh) zwingend!"
        setup["rig"] = "D-Rig / Slip-D (Verwickelt seltener bei Weißfisch-Attacken)"
    
    if temp_v < 10:
        setup["koeder"] = "Kleine Köder (12-15mm) / Hochattraktiv"
        setup["haken_range"] = "6 bis 8"

    # --- HINDERNIS- & BLEI-LOGIK ---
    if any("Kraut" in h for h in h_liste):
        setup["montage"] = "Helicopter-System (Abwurf-Blei)"
    
    if any(s in str(h_liste) for s in ["Muschel", "Kante", "Holz"]):
        setup["haken_range"] = "2 bis 4 (X-Strong)"
        setup["zusatz"] += " | Schlagschnur (0.60mm) verwenden!"

    if t_typ == "Wurf":
        setup["blei_g"] = 115 if w_weite > 90 else 90
    if stromung == "Stark" or "Starker Schiffsverkehr" in h_liste:
        setup["blei_g"] = 240

    return setup

ergebnis = berechne_taktik(taktik_typ, wurfweite, hindernisse, weissfisch_aufkommen, fisch_aktivitaet, temp)

# --- FUTTER-KALKULATION ---
def berechne_futter():
    basis = 0.5 # kg pro Tag
    # Temperatur-Faktor
    if temp > 18: basis += 1.5
    elif temp < 10: basis = 0.2
    # Aktivitäts-Faktor
    if fisch_aktivitaet == "Aggressiv": basis *= 2
    # Weißfisch-Faktor (Konkurrenz frisst mit)
    if weissfisch_aufkommen == "Hoch": basis += 1.0
    if weissfisch_aufkommen == "Extrem": basis += 2.5
    
    art = "Boilies (pur)" if weissfisch_aufkommen in ["Hoch", "Extrem"] else "Partikel-Mix & Boilies"
    return round(basis, 1), art

f_menge, f_art = berechne_futter()

# ==========================================
# 4. PHASE: AUSGABE
# ==========================================
st.divider()
st.header("🏁 Dein Taktik-Setup")

o1, o2, o3 = st.columns(3)

with o1:
    st.subheader("📦 Montage & Blei")
    st.metric("Bleigewicht", f"{ergebnis['blei_g']} g")
    st.write(f"**System:** {ergebnis['montage']}")
    st.write(f"**Extras:** {ergebnis['zusatz']}")

with o2:
    st.subheader("🪝 Rig & Material")
    st.success(f"**Rig:** {ergebnis['rig']}")
    st.write(f"**Material:** {ergebnis['material_opt']}")
    st.write(f"**Haken:** {ergebnis['haken_range']}")
    st.info(f"**Köder-Wahl:** {ergebnis['koeder']}")

with o3:
    st.subheader("🥣 Futter-Strategie")
    st.metric("Futtermenge", f"{f_menge} kg / Tag")
    st.write(f"**Futter-Art:** {f_art}")
    if weissfisch_aufkommen in ["Hoch", "Extrem"]:
        st.warning("⚠️ Keine weichen Partikel/Pellets nutzen (lockt Weißfische zu stark an)!")

st.divider()
st.info(f"**Strategischer Tipp:** Bei {temp}°C und {weissfisch_aufkommen} Weißfisch-Konkurrenz liegt der Fokus auf **Selektion**. "
        f"Verwende größere, harte Köder, um die Störfische zu 'überangeln'.")
