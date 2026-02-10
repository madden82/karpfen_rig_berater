import streamlit as st

# Konfiguration
st.set_page_config(page_title="Karpfen-Rig Kalkulator", layout="centered")

st.title("🎣 Karpfen-Rig Kalkulator")
st.markdown("Beantworte die Fragen, um dein optimales Setup zu berechnen.")

# ==========================================
# SCHRITT 1 - 9: DIE EINGABEMASKE (DEIN ORIGINAL-STIL)
# ==========================================

with st.expander("1️⃣ Gewässer und Strömung", expanded=True):
    gewässertyp = st.radio("Gewässertyp:", 
        ("Keine Strömung (Seen, Teiche, Weiher, Baggerseen, Lagunen)", 
         "Strömung vorhanden (Flüsse, Kanäle, Stauseen, Altarme, Mündungsbereiche)"))
    
    if "Keine Strömung" in gewässertyp:
        strom = "keine"
        strom_m_s = 0.0
    else:
        strom_stufe = st.select_slider("Strömungsgeschwindigkeit:", options=["leicht", "mittel", "stark"])
        strom = strom_stufe
        strom_m_s = {"leicht": 0.2, "mittel": 0.6, "stark": 1.4}[strom]

with st.expander("2️⃣ Angeltechnik & Wurfweite"):
    angeltechnik = st.radio("Angeltechnik:", ("Wurf vom Ufer aus", "Boot: Wurf von Boot aus", "Boot: Ablage von Boot aus", "Futterboot"))
    wurfweite = st.slider("Wurfweite (m):", 0, 200, 50) if "Wurf" in angeltechnik else 0

with st.expander("3️⃣ Bodenbeschaffenheit"):
    boden = st.radio("Bodenart:", ("weich", "mittel", "hart"))
    st.info("Hart: Kies/Lehm | Mittel: Sand/dünner Schlamm | Weich: tiefer Schlamm")

with st.expander("4️⃣ Maximal erwartetes Karpfengewicht"):
    gewicht = st.slider("Gewicht (kg):", 1, 40, 10)

with st.expander("5️⃣ Verhalten der Karpfen"):
    fischverhalten = st.radio("Karpfenverhalten:", ("Aktive Fresser", "Scheue Karpfen", "Beide Typen / weiß nicht genau"))

with st.expander("6️⃣ Hindernisse am Spot"):
    hindernisse_vorhanden = st.radio("Sind Hindernisse vorhanden?", ("Ja", "Nein", "Weiß ich nicht"))
    hindernisse_bool = True if hindernisse_vorhanden == "Ja" else False

with st.expander("7️⃣ Wasserqualität"):
    wasserqualitaet = st.radio("Wasserqualität:", ("klar", "leicht trüb", "trüb"))

with st.expander("8️⃣ Störtiere"):
    störtiere = st.multiselect("Welche Störtiere sind vorhanden?", ["Viele Weißfische", "Krebse", "Keine oder wenige"])

with st.expander("9️⃣ Jahreszeit und Wassertemperatur"):
    season = st.selectbox("Jahreszeit:", ["Frühling", "Sommer", "Herbst", "Winter"])
    temperature = st.slider("Wassertemperatur (°C):", 0, 35, 15)

# ==========================================
# BERECHNUNG DER DATEN
# ==========================================

# 1. Bleigewicht
basis_blei = {1: 12, 5: 35, 10: 50, 15: 60, 20: 70, 30: 90, 40: 110}
basis = min([v for k, v in basis_blei.items() if gewicht <= k] or [110])
boden_f = {"weich": 0.9, "mittel": 1.0, "hart": 1.1}[boden]
strom_f = {"keine": 1.0, "leicht": 1.05, "mittel": 1.10, "stark": 1.20}[strom]
gewicht_effektiv = round(basis * boden_f * strom_f, 1)

# 2. Rigs
rigs = {
    "Line-Aligner": {"boden": ["hart", "mittel"], "max_wurf": 120, "strom_max": 0.85, "grund": "Perfekt auf Kies. Haken kippt sofort."},
    "Snowman": {"boden": ["hart", "mittel", "weich"], "max_wurf": 100, "strom_max": 1.22, "grund": "Leicht auftreibend. Gut bei Schlamm."},
    "Helikopter": {"boden": ["weich", "mittel", "hart"], "max_wurf": 200, "strom_max": 2.0, "grund": "Bestes Rig für alle Böden und weite Würfe."}
}
empfohlene_rigs = [name for name, info in rigs.items() if boden in info["boden"] and wurfweite <= info["max_wurf"] and strom_m_s <= info["strom_max"]]

# ==========================================
# AUSWERTUNG & FINALE SPOTWAHL
# ==========================================
st.markdown("---")
if st.button("JETZT AUSWERTUNG GENERIEREN"):
    
    st.header("📊 Dein optimiertes Setup")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Bleigewicht", f"{gewicht_effektiv} g")
        st.write(f"**Vorfach:** {'ca. 25-40' if boden == 'weich' else 'ca. 15-20'} cm")
    with c2:
        st.write(f"**Empfohlene Rigs:** {', '.join(empfohlene_rigs[:2])}")
        st.write(f"**Technik:** {angeltechnik}")

    st.header("🎯 Strategische Spot-Info")
    
    # Intelligente Spot-Analyse basierend auf ALLEN Daten
    analyse_text = []
    
    # Temperatur & Tiefe
    if temperature < 10:
        analyse_text.append(f"Da es **{season}** ist ({temperature}°C), stehen die Fische tief. Suche nach Mulden. Dein {gewicht_effektiv}g Blei muss präzise liegen, da die Fische wenig ziehen.")
    elif temperature > 20:
        analyse_text.append(f"Bei {temperature}°C im **{season}** ist Sauerstoff alles. Suche Schatten oder Wind-Ufer.")

    # Boden & Störtiere
    if boden == "weich":
        analyse_text.append("Achtung: Auf weichem Boden sinkt das Blei ein. Nutze längere Vorfächer, damit der Köder oben auf dem Schlamm liegt.")
    if "Krebse" in störtiere:
        analyse_text.append("⚠️ Krebse aktiv! Nutze 'Hard Baits' oder schütze deine Boilies mit Schrumpfschlauch.")

    # Strömung & Hindernisse
    if strom != "keine":
        analyse_text.append(f"Bei {strom}er Strömung solltest du den Spot im Strömungsschatten (hinter Kanten) suchen, damit dein Futter liegen bleibt.")
    if hindernisse_bool:
        analyse_text.append("Da Hindernisse vorhanden sind: Nutze ein Safety-Clip System, damit der Fisch das Blei im Drill verlieren kann.")

    # Finale Zusammenfassung
    for t in analyse_text:
        st.info(t)

    st.success("Tipp: Füttere punktgenau, da die Fische bei deinem Setup eine saubere Präsentation brauchen!")
