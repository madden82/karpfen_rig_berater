import streamlit as st

# ==========================================
# KONFIGURATION
# ==========================================
st.set_page_config(page_title="Karpfen-Rig Kalkulator PRO", layout="wide")

st.title("🎣 Karpfen-Rig Kalkulator & Taktik-Master")
st.markdown("---")

# ==========================================
# 1️⃣ EINGABEN
# ==========================================
st.sidebar.header("📍 Deine Spot-Daten")

gewässertyp = st.sidebar.radio(
    "Gewässertyp:",
    ("Keine Strömung (Seen, Teiche, Weiher, Baggerseen)",
     "Strömung vorhanden (Flüsse, Kanäle, Stauseen)")
)

if gewässertyp.startswith("Keine Strömung"):
    strom = "keine"
    strom_m_s = 0.0
else:
    strom = st.sidebar.select_slider("Strömungsgeschwindigkeit:", options=["leicht", "mittel", "stark"])
    strom_m_s = {"leicht": 0.2, "mittel": 0.6, "stark": 1.4}[strom]

angeltechnik = st.sidebar.radio("Angeltechnik:", ("Wurf vom Ufer aus", "Boot / Futterboot"))
wurfweite = st.sidebar.slider("Wurfweite (m):", 0, 200, 50) if "Wurf" in angeltechnik else 0
boden = st.sidebar.selectbox("Bodenart:", ("weich", "mittel", "hart"))
gewicht = st.sidebar.slider("Max. erwartetes Karpfengewicht (kg):", 1, 40, 12)
fischverhalten = st.sidebar.selectbox("Karpfenverhalten:", ("Aktive Fresser", "Scheue Karpfen", "Beide Typen"))
wasserqualitaet = st.sidebar.selectbox("Wasserqualität:", ("klar", "leicht trüb", "trüb"))
season = st.sidebar.selectbox("Jahreszeit:", ["Frühling", "Sommer", "Herbst", "Winter"])
temperature = st.sidebar.slider("Wassertemperatur (°C):", 0, 30, 15)
störtiere = st.sidebar.multiselect("Störtiere:", ["Viele Weißfische", "Krebse", "Wollhandkrabben"])
hindernisse = st.sidebar.radio("Hindernisse am Spot?", ("Ja", "Nein"))

# ==========================================
# 2️⃣ BERECHNUNGEN (DEINE LOGIK)
# ==========================================
basis_blei_map = {1: 12, 3: 25, 5: 35, 10: 50, 15: 60, 20: 70, 25: 80, 30: 90, 35: 100, 40: 110}
basis = min([v for k, v in basis_blei_map.items() if gewicht <= k] or [110])
gewicht_effektiv = round(basis * {"weich": 0.9, "mittel": 1.0, "hart": 1.1}[boden] * {"keine": 1.0, "leicht": 1.05, "mittel": 1.10, "stark": 1.20}[strom], 1)

vorfach_tabelle = {"hart": (10, 20), "mittel": (15, 30), "weich": (25, 50)}
min_v, max_v = vorfach_tabelle[boden]
vorfach_l = max_v if fischverhalten != "Aktive Fresser" else (min_v + max_v) // 2

# Rig-Auswahl
rigs = {
    "Line-Aligner": {"boden": ["hart", "mittel"], "w": 120, "s": 0.85, "text": "Haken kippt extrem schnell. Ideal für Bodenköder auf festem Grund."},
    "Snowman": {"boden": ["hart", "mittel", "weich"], "w": 100, "s": 1.22, "text": "Kombination aus sinkendem & schwimmendem Boilie. Perfekte Balance."},
    "D-Rig": {"boden": ["hart"], "w": 150, "s": 0.6, "text": "Maximale Köderbeweglichkeit. Sehr unauffällig für misstrauische Großkarpfen."},
    "KD-Rig": {"boden": ["hart", "mittel", "weich"], "w": 120, "s": 1.05, "text": "Durch das tief austretende Haar steht der Haken extrem aggressiv."},
    "Helikopter-Rig": {"boden": ["weich", "mittel", "hart"], "w": 200, "s": 2.0, "text": "Das Vorfach gleitet auf der Schnur hoch. Köder sinkt niemals im Schlamm ein."}
}
passende = [r for r, i in rigs.items() if boden in i["boden"] and wurfweite <= i["w"] and strom_m_s <= i["s"]]

# ==========================================
# 3️⃣ AUSGABE & ERWEITERTE TAKTIK
# ==========================================
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🏁 Das Setup")
    st.metric("Berechnetes Blei", f"{gewicht_effektiv} g")
    st.info(f"**Vorfachlänge:** {vorfach_l} cm")
    st.write("👉 *So kurz wie möglich, so lang wie nötig!*")
    
    st.subheader("Empfohlene Rigs")
    for p in passende[:2]:
        st.success(f"**{p}**")
        st.caption(rigs[p]["text"])

with col2:
    st.header("🎯 Taktische Master-Strategie")
    
    # --- BODEN & PRÄSENTATION ---
    st.subheader("🏗️ Boden & Präsentation")
    if boden == "weich":
        st.write("- **Taktik:** Im Schlamm sammeln sich Zuckmückenlarven. Die Fische wühlen tief. Nutze ein langes Haar oder Pop-Ups (1-2cm über Grund), damit der Köder nicht im Faulschlamm verschwindet.")
        st.write("- **Futter:** Nutze leichte Partikel (Hanf) und Pellets, die langsam einsinken.")
    elif boden == "hart":
        st.write("- **Taktik:** Die Fische fressen hier oft hart am Grund. Kurze Vorfächer sind hier tödlich, da der Haken sofort greift, sobald der Fisch den Kopf hebt.")
    
    # --- STRÖMUNG & LOCKWIRKUNG ---
    st.subheader("🌊 Strömung & Futter")
    if strom == "keine":
        st.write("- **Strategie:** Ohne Strömung ist die Lockwirkung geringer. Nutze 'Liquids' oder 'PVA-Sticks', um eine punktuelle Duftwolke direkt am Hakenköder zu erzeugen.")
    else:
        st.write(f"- **Strategie:** Bei {strom}er Strömung wird Futter abgetrieben. Lege deine Futterspur stromaufwärts vom Hakenköder an. Schwere Boilies (24mm+) oder Clay-Bälle nutzen.")

    # --- JAHRESZEIT & THERMIK ---
    st.subheader("🌡️ Temperatur & Fischzug")
    if temperature < 10:
        st.write(f"- **Spotwahl:** Winter/Frühjahr ({temperature}°C). Karpfen sind wechselwarm. Suche die 'Thermocline' (Sprungschicht). Oft stehen sie im Winter im tieferen Freiwasser oder in geschützten Mulden.")
        st.write("- **Köder:** Hochattraktive, kleine Köder (12-14mm). Wenig Öl (da Öl im kalten Wasser zähflüssig wird).")
    elif temperature > 20:
        st.write(f"- **Spotwahl:** Sommerhitze! Sauerstoff ist der Schlüssel. Suche Einläufe, Sprudelsteine oder die windzugewandte Seite (Auflandiger Wind).")

    # --- STÖRTIERE & GEFAHREN ---
    if störtiere:
        st.subheader("🦀 Störtiere & Sicherheit")
        if "Krebse" in störtiere or "Wollhandkrabben" in störtiere:
            st.warning("- **Krebs-Alarm:** Nutze 'Armabraid' (Schrumpfschlauch) für deine Boilies oder Tigernüsse. Vermeide fischige Aromen, nutze eher süße/fruchtige Köder, die Krebse weniger anlocken.")
        if "Viele Weißfische" in störtiere:
            st.write("- **Weißfische:** Erhöhe den Köderdurchmesser auf 24mm oder 30mm, um Brassen und Rotaugen zu selektieren.")

    # --- HINDERNISSE ---
    if hindernisse == "Ja":
        st.subheader("🪵 Hindernis-Management")
        st.write("- **Sicherheit:** 'Safety First'. Nutze unbedingt ein Safety-Clip System, damit das Blei im Falle eines Abrisses sofort abfällt. Verwende eine Schlagschnur (min. 0.50mm Mono) auf den letzten 10-15 Metern.")

st.markdown("---")
st.success("Tipp: Beobachte das Wasser! Ein einzelnes Rollen oder Springen eines Karpfens sagt mehr aus als jede Theorie. Petri Heil!")
