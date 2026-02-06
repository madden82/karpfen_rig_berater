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
# 1️⃣ Gewässer & Umwelt
# =========================
st.header("🌊 Gewässer & Umwelt")
gewaesser_typ = st.selectbox("Gewässertyp", ["Teich", "See", "Fluss", "Strom"])
st.caption("Teich → kleine Gewässer, ruhiges Wasser | See → größere Flächen | Fluss/Strom → Strömung beachten")

fliessgeschwindigkeit = 0.0
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider("Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1)
    st.caption("0 = kaum Strömung → normale Rigs | 2 m/s = starke Strömung → stabilere Rigs oder Zusatzblei nötig")

jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
st.caption("Winter → wenig Aktivität, Pop-Ups sinnvoll | Sommer → aktive Fische, Standard-Boilies")

wasser_truebung = st.slider("Wassertrübung (0=klar, 10=trüb)", 0, 10, 3)
st.caption("0 = kristallklar, unauffällige Köder | 10 = trüb, auffällige Köder oder Pop-Ups")

wassertemperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16)
st.caption("Unter 10°C → Kaltwasser-Köder | Über 20°C → Standard-Boilie oder Wafter")

# =========================
# 2️⃣ Boden & Pflanzen
# =========================
st.header("🏞️ Boden & Pflanzen")
boden = st.selectbox("Bodenbeschaffenheit", ["hart", "weich", "schlammig"])
st.caption("Hart → Standard-Rigs | Weich/Schlamm → stabilere Rigs oder Zusatzblei")

kraut = st.checkbox("Kraut vorhanden 🌿")
st.caption("Kraut kann Hänger verursachen → Ronnie Rig oder Hair Rig mit Zusatzblei nutzen")

st.subheader("Hindernisse ⛔")
hindernisse_muscheln = st.checkbox("Muscheln / Steine")
hindernisse_aeste = st.checkbox("Äste / Unterholz")
hindernisse_grund = st.checkbox("Andere Hindernisse")
st.caption("Hindernisse erhöhen Risiko von Hänger. Rigs entsprechend wählen")

hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

# =========================
# 3️⃣ Fisch & Angelbedingungen
# =========================
st.header("🐟 Fisch & Angelbedingungen")
angeldruck = st.selectbox("Angeldruck", ["niedrig", "mittel", "hoch"])
st.caption("Hoch → vorsichtige Fische → unauffällige Rigs (D-Rig, Wafter) empfohlen")

vorsichtige_fische = angeldruck == "hoch"
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)
st.caption("0% → kaum Weißfische, Standardköder | 10% → viele Weißfische, harte Köder oder Pop-Ups sinnvoll")

max_karpfen = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)
st.caption("Je größer der Karpfen, desto stärker der Haken wählen")

modus = st.radio("Ziel", ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"])
st.caption("Maximale Fangquote → aggressive Rigs | Maximale Sicherheit → vorsichtige Rigs")

wurfweite = st.slider("Wurfweite (Meter)", 10, 120, 40)
st.caption("Lange Wurfweite → schwereres Blei oder Distance-Blei nötig")

# =========================
# Köderempfehlung
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

# =========================
# Rig-Empfehlung (maximal 2)
# =========================
def rig_empfehlung(koeder):
    candidate_rigs = []

    # Hair Rig
    if koeder not in ["Pop-Up", "Leuchtender Pop-Up"] and not hindernisse and modus.startswith("🛡"):
        candidate_rigs.append({
            "name": "Hair Rig",
            "aufbau": [
                "1. Haar vorbereiten (1–2 cm)",
                "2. Haken einbinden (angepasst an Karpfen-Größe)",
                "3. Wirbel nur bei Strömung >0.8 m/s oder Hindernissen",
                "4. Köder aufziehen"
            ],
            "vorfach": ("Mono", 25),
        })

    # Ronnie Rig
    if kraut or boden in ["weich", "schlammig"] or koeder in ["Pop-Up", "Leuchtender Pop-Up"]:
        candidate_rigs.append({
            "name": "Ronnie Rig",
            "aufbau": [
                "1. Haar vorbereiten (1,5–2 cm)",
                "2. Haken einbinden (angepasst an Karpfen-Größe)",
                "3. Wirbel einbauen für Abriebschutz bei Hindernissen",
                "4. Zusatzblei bei Pop-Up falls nötig",
                "5. Köder aufziehen"
            ],
            "vorfach": ("Stiff", 25),
        })

    # D-Rig
    if vorsichtige_fische and koeder not in ["Pop-Up", "Leuchtender Pop-Up"]:
        candidate_rigs.append({
            "name": "D-Rig",
            "aufbau": [
                "1. Haar vorbereiten (1 cm)",
                "2. Haken einbinden (angepasst an Karpfen-Größe)",
                "3. Köder aufziehen"
            ],
            "vorfach": ("Stiff", 25),
        })

    # Blowback Rig als Fallback
    if not candidate_rigs:
        candidate_rigs.append({
            "name": "Blowback Rig",
            "aufbau": [
                "1. Haar vorbereiten (1–1,5 cm)",
                "2. Haken einbinden (angepasst an Karpfen-Größe)",
                "3. Köder aufziehen"
            ],
            "vorfach": ("Mono", 25),
        })

    return candidate_rigs[:2]

# =========================
# Haken- und Bleiempfehlung
# =========================
def haken_empfehlung(max_karpfen):
    if max_karpfen >= 25:
        return "Größe 4 Wide Gape", "Für große Karpfen"
    return "Größe 6 Wide Gape", "Standard"

def blei_empfehlung(koeder, wurfweite, hindernisse, fliessgeschwindigkeit):
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
# Ausgabe
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    koeder, groesse, koeder_grund = koeder_empfehlung()
    rigs = rig_empfehlung(koeder)
    haken, haken_grund = haken_empfehlung(max_karpfen)
    blei, blei_form = blei_empfehlung(koeder, wurfweite, hindernisse, fliessgeschwindigkeit)

    st.success("✅ Deine persönliche Empfehlung")

    # Übersicht
    st.subheader("📋 Übersicht")
    rig_namen = ", ".join([r['name'] for r in rigs])
    st.write(f"**Rig:** {rig_namen}")
    st.write(f"**Haken:** {haken}")
    st.write(f"**Vorfachmaterial:** {', '.join([r['vorfach'][0] for r in rigs])}")
    st.write(f"**Vorfachlänge:** {', '.join([str(r['vorfach'][1])+' cm' for r in rigs])}")

    # Köder
    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {groesse} mm")
    st.caption(koeder_grund)

    # Rig-Baupläne
    st.subheader("🪝 Empfohlene Rigs (Bauplan)")
    for rig in rigs:
        st.write(f"**{rig['name']}**")
        for schritt in rig['aufbau']:
            st.write(schritt)

    # Blei
    st.subheader("⚖️ Blei")
    st.write(f"{blei} g – {blei_form}")
    st.caption("Wird benötigt, um Haken & Köder korrekt zu stabilisieren")

    st.info("🎯 Tipp: Passe Rig, Vorfach und Blei regelmäßig an Gewässer, Jahreszeit, Strömung und Fischverhalten an.")
