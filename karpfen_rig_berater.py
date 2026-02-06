import streamlit as st

# =========================
# Seite konfigurieren
# =========================
st.set_page_config(
    page_title="🎣 Profi-Karpfen Rig Berater",
    layout="centered"
)

st.title("🎣 Profi-Karpfen Rig & Vorfach Berater")
st.caption("Optimiert für Fangquote & Sicherheit – mobil bedienbar")

# =========================
# 1️⃣ Gewässertyp & Umwelt
# =========================
st.header("🌊 Gewässer & Umwelt")

gewaesser_typ = st.selectbox(
    "Gewässertyp", ["Teich", "See", "Fluss", "Strom"],
    help="Art des Gewässers beeinflusst Strömung und Köderwahl."
)

fliessgeschwindigkeit = 0
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider(
        "Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1,
        help="Schnelle Strömung erfordert stabilere Rigs und Vorfächer."
    )

jahreszeit = st.selectbox(
    "Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"],
    help="Karpfen fressen je nach Jahreszeit unterschiedlich aktiv."
)

wasser_truebung = st.slider(
    "Wassertrübung (0=klar, 10=trüb)", 0, 10, 3,
    help="Beeinflusst Köderfarbe und Sichtbarkeit."
)

wassertemperatur = st.slider(
    "Wassertemperatur (°C)", 4, 30, 16,
    help="Aktivität der Karpfen hängt stark von der Temperatur ab."
)

# =========================
# 2️⃣ Boden & Pflanzen
# =========================
st.header("🏞️ Boden & Pflanzen")

boden = st.selectbox(
    "Bodenbeschaffenheit", ["hart", "weich", "schlammig"],
    help="Bodenart beeinflusst, welches Rig am besten aufliegt."
)

kraut = st.checkbox(
    "Kraut vorhanden", help="Kraut kann den Köder verdecken oder verfangen."
)

st.subheader("Hindernisse ⛔")
hindernisse_muscheln = st.checkbox("Muscheln / Steine")
hindernisse_aeste = st.checkbox("Äste / Unterholz")
hindernisse_grund = st.checkbox("Andere Hindernisse")

hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

# =========================
# 3️⃣ Fisch & Angelbedingungen
# =========================
st.header("🐟 Fisch & Angelbedingungen")

angeldruck = st.selectbox("Angeldruck", ["niedrig", "mittel", "hoch"])
vorsichtige_fische = angeldruck == "hoch"

weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)
max_karpfen = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)

modus = st.radio(
    "Ziel",
    ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"],
    help="Maximale Fangquote = sichtbarer Köder, maximale Sicherheit = vorsichtig & unauffällig."
)

wurfweite = st.slider("Wurfweite (Meter)", 10, 120, 40)

# =========================
# 4️⃣ Rig-Logik & Empfehlungen
# =========================

def koeder_empfehlung():
    if wassertemperatur < 10 or jahreszeit == "Winter":
        return "Pop-Up", 14, "Kaltwasser / Winter – leicht & auffällig"
    if weissfisch >= 6:
        return "Harter Boilie", 22, "Schützt vor Weißfisch"
    if vorsichtige_fische:
        return "Wafter", 18, "Unauffällig & effektiv"
    if wasser_truebung > 6:
        return "Leuchtender Pop-Up", 16, "Trübes Wasser – auffälliger Köder"
    return "Boilie", 20, "Bewährter Standardköder"

def rig_empfehlung(koeder_typ):
    """
    Alle Rigs prüfen und nur notwendige Komponenten ausgeben
    """
    rigs = []

    # Hair Rig
    if not (koeder_typ in ["Pop-Up", "Leuchtender Pop-Up"]) and modus.startswith("🛡") and not hindernisse:
        rigs.append({
            "name": "Hair Rig",
            "grund": "Allround, sicher für klare Wasserbedingungen",
            "aufbau": [
                "Haarlänge: 1–2 cm",
                "Schrumpfschlauch: optional (bei weichem Boden)",
                "Wirbel: nur bei Strömung >0.8 m/s",
                "Haken: Größe 6 Wide Gape"
            ]
        })

    # Ronnie Rig
    if kraut or boden in ["weich", "schlammig"] or koeder_typ in ["Pop-Up", "Leuchtender Pop-Up"]:
        rigs.append({
            "name": "Ronnie Rig",
            "grund": "Optimal für Kraut und Pop-Up",
            "aufbau": [
                "Haarlänge: 1,5–2 cm",
                "Schrumpfschlauch: nur bei Kraut oder weichem Boden",
                "Wirbel: klein für Abriebschutz",
                "Haken: Größe 6 Wide Gape",
                "Zusatzblei: 20 g bei Pop-Up"
            ],
            "video": "https://www.youtube.com/watch?v=EXAMPLE_RONNIE"
        })

    # D-Rig
    if vorsichtige_fische:
        rigs.append({
            "name": "D-Rig",
            "grund": "Unauffällig für vorsichtige Fische",
            "aufbau": [
                "Haarlänge: 1 cm",
                "Schrumpfschlauch: optional",
                "Wirbel: nicht nötig",
                "Haken: Größe 6 Curve Shank"
            ]
        })

    # Blowback Rig
    if not rigs:
        rigs.append({
            "name": "Blowback Rig",
            "grund": "Allround-Rig mit hoher Hakeffizienz",
            "aufbau": [
                "Haarlänge: 1–1,5 cm",
                "Schrumpfschlauch: optional",
                "Wirbel: nicht nötig",
                "Haken: Größe 6 Wide Gape"
            ]
        })

    return rigs

def vorfach_empfehlung(rig):
    if fliessgeschwindigkeit > 0.8:
        return "Stiff + heavier", 25, 25, "Strömungsbeständiges Vorfach"
    if hindernisse:
        return "Kombi-Vorfach (coated braid + stiff)", 20, 25, "Abriebschutz & Kontrolle"
    if vorsichtige_fische and wasser_truebung < 4:
        return "Fluorocarbon", 30, 15, "Nahezu unsichtbar im klaren Wasser"
    return "Mono", 25, 15, "Unkompliziert & zuverlässig"

def haken_empfehlung():
    if max_karpfen >= 20:
        return "Größe 4 Wide Gape (starker Draht)", "Für große & kampfstarke Karpfen"
    if vorsichtige_fische:
        return "Größe 6 Curve Shank", "Verbessert Hookups bei vorsichtigen Fischen"
    return "Größe 6 Wide Gape", "Allround-Haken"

def blei_empfehlung(koeder):
    gewicht = 80
    form = "Inline"
    if wurfweite > 60:
        gewicht += 20
        form = "Distance"
    if "muscheln/steine" in hindernisse:
        gewicht += 10
    if fliessgeschwindigkeit > 0.8:
        gewicht += 20
    if koeder in ["Pop-Up", "Leuchtender Pop-Up"]:
        gewicht = max(gewicht, 25)
    return gewicht, form

# =========================
# 5️⃣ Ausgabe
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    koeder, groesse, koeder_grund = koeder_empfehlung()
    rigs = rig_empfehlung(koeder)
    vorfach, laenge, staerke, vorfach_grund = vorfach_empfehlung(rigs[0]['name'])
    haken, haken_grund = haken_empfehlung()
    blei, blei_form = blei_empfehlung(koeder)

    st.success("✅ Deine persönliche Empfehlung")

    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {groesse} mm")
    st.caption(koeder_grund)

    st.subheader("🪝 Rigs")
    for rig in rigs:
        st.write(f"**{rig['name']}**")
        st.caption(rig['grund'])
        for zeile in rig['aufbau']:
            st.text(zeile)
        if 'video' in rig:
            st.markdown(f"[🎥 Video Tutorial]({rig['video']})")

    st.subheader("🧵 Vorfach")
    st.write(f"{vorfach}, {laenge} cm, {staerke} lb")
    st.caption(vorfach_grund)

    st.subheader("🎣 Haken")
    st.write(haken)
    st.caption(haken_grund)

    st.subheader("⚖️ Blei")
    st.write(f"{blei} g – {blei_form}")
    st.caption("Wird benötigt, um Haken & Köder korrekt zu stabilisieren")

    st.info("🎯 Tipp: Passe Rig & Vorfach regelmäßig an Gewässer, Jahreszeit, Strömung und Fischverhalten an.")
