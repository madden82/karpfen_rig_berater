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
st.caption("Teich → kleine Gewässer, ruhiges Wasser | See → große Flächen, evtl. Wind | Fluss/Strom → Strömung beachten")

fliessgeschwindigkeit = 0.0
if gewaesser_typ in ["Fluss", "Strom"]:
    fliessgeschwindigkeit = st.slider("Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1)
    st.caption("0 = kaum Strömung → normale Rigs ausreichend | 2 m/s = starke Strömung → stabilere Rigs oder Zusatzblei nötig")

jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
st.caption("Die Jahreszeit beeinflusst Fressverhalten: Winter → wenig Aktivität, Pop-Ups | Sommer → aktive Fische, Standard-Boilies")

wasser_truebung = st.slider("Wassertrübung (0=klar, 10=trüb)", 0, 10, 3)
st.caption("0 = kristallklar, Köder unauffällig wählen | 10 = stark trüb, auffällige Köder sinnvoll")

wassertemperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16)
st.caption("Unter 10°C → Kaltwasser-Köder (Pop-Up) | Über 20°C → Standard-Boilie oder Wafter")

# =========================
# 2️⃣ Boden & Pflanzen
# =========================
st.header("🏞️ Boden & Pflanzen")
boden = st.selectbox("Bodenbeschaffenheit", ["hart", "weich", "schlammig"])
st.caption("Hart → Standard-Rigs | Weich/Schlamm → stabilere Rigs oder Zusatzblei empfohlen")

kraut = st.checkbox("Kraut vorhanden 🌿")
st.caption("Kraut kann Hänger verursachen → Ronnie Rig oder Hair Rig mit Zusatzblei nutzen")

st.subheader("Hindernisse ⛔")
hindernisse_muscheln = st.checkbox("Muscheln / Steine")
hindernisse_aeste = st.checkbox("Äste / Unterholz")
hindernisse_grund = st.checkbox("Andere Hindernisse")
st.caption("Hindernisse erhöhen Risiko von Hänger. Wähle Rig entsprechend: z.B. Blowback bei glattem Grund, Ronnie bei Kraut/Ästen")

hindernisse = []
if hindernisse_muscheln: hindernisse.append("muscheln/steine")
if hindernisse_aeste: hindernisse.append("äste/unterholz")
if hindernisse_grund: hindernisse.append("andere")

# =========================
# 3️⃣ Fisch & Angelbedingungen
# =========================
st.header("🐟 Fisch & Angelbedingungen")
angeldruck = st.selectbox("Angeldruck", ["niedrig", "mittel", "hoch"])
st.caption("Hoch → vorsichtige Fische, unauffällige Rigs (D-Rig, Wafter) empfohlen | Niedrig → Standard-Rigs möglich")

vorsichtige_fische = angeldruck == "hoch"
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)
st.caption("0% → kaum Weißfisch, Standardköder | 10% → viele Weißfische, harte Köder oder Pop-Ups sinnvoll")

max_karpfen = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)
st.caption("Je größer der Karpfen, desto stärker der Haken wählen (über 25kg → Größe 4 Wide Gape)")

modus = st.radio("Ziel", ["🎯 Maximale Fangquote", "🛡 Maximale Sicherheit"])
st.caption("Maximale Fangquote → aggressive Rigs | Maximale Sicherheit → vorsichtige Rigs")

wurfweite = st.slider("Wurfweite (Meter)", 10, 120, 40)
st.caption("Lange Wurfweite → schwereres Blei oder Distance-Blei nötig")

# =========================
# Köder
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
# Rig-Auswahl
# =========================
def rig_empfehlung(koeder):
    candidate_rigs = []

    if koeder not in ["Pop-Up", "Leuchtender Pop-Up"] and not hindernisse and modus.startswith("🛡"):
        candidate_rigs.append({
            "name": "Hair Rig",
            "aufbau": [
                "Haar vorbereiten (1–2 cm)",
                "Schrumpfschlauch nur bei weichem Boden",
                "Wirbel nur bei Strömung >0.8 m/s",
                "Haken einbinden (angepasst an Karpfengröße)",
                "Köder aufziehen"
            ]
        })

    if kraut or boden in ["weich", "schlammig"] or koeder in ["Pop-Up", "Leuchtender Pop-Up"]:
        candidate_rigs.append({
            "name": "Ronnie Rig",
            "aufbau": [
                "Haar vorbereiten (1,5–2 cm)",
                "Schrumpfschlauch nur bei Kraut oder weichem Boden",
                "Wirbel klein für Abriebschutz",
                "Haken einbinden (angepasst an Karpfengröße)",
                "Zusatzblei bei Pop-Up (falls verwendet)",
                "Köder aufziehen"
            ]
        })

    if vorsichtige_fische and koeder not in ["Pop-Up", "Leuchtender Pop-Up"]:
        candidate_rigs.append({
            "name": "D-Rig",
            "aufbau": [
                "Haar vorbereiten (1 cm)",
                "Schrumpfschlauch optional",
                "Haken einbinden (angepasst an Karpfengröße)",
                "Köder aufziehen"
            ]
        })

    if not candidate_rigs:
        candidate_rigs.append({
            "name": "Blowback Rig",
            "aufbau": [
                "Haar vorbereiten (1–1,5 cm)",
                "Schrumpfschlauch optional",
                "Haken einbinden (angepasst an Karpfengröße)",
                "Köder aufziehen"
            ]
        })

    return candidate_rigs[:2]

# =========================
# Vorfach, Haken, Blei
# =========================
def vorfach_empfehlung(rigs):
    return "Mono", 25

def haken_empfehlung(rigs, max_karpfen):
    if max_karpfen >= 25:
        return "Größe 4 Wide Gape", "Für große Karpfen"
    return "Größe 6 Wide Gape", "Standard"

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
# Ausgabe
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    koeder, groesse, koeder_grund = koeder_empfehlung()
    rigs = rig_empfehlung(koeder)
    vorfach, laenge = vorfach_empfehlung(rigs)
    haken, haken_grund = haken_empfehlung(rigs, max_karpfen)
    blei, blei_form = blei_empfehlung(koeder)

    st.success("✅ Deine persönliche Empfehlung")

    # Übersicht
    st.subheader("📋 Übersicht")
    rig_namen = ", ".join([r['name'] for r in rigs])
    st.write(f"**Rig:** {rig_namen}")
    st.write(f"**Haken:** {haken}")
    st.write(f"**Vorfachmaterial:** {vorfach}")
    st.write(f"**Vorfachlänge:** {laenge} cm")

    # Köder
    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {groesse} mm")
    st.caption(koeder_grund)

    # Rig-Baupläne
    st.subheader("🪝 Empfohlene Rigs (Bauplan)")
    for rig in rigs:
        st.write(f"**{rig['name']}**")
        for i, schritt in enumerate(rig['aufbau'], 1):
            st.write(f"{i}. {schritt}")

    # Blei
    st.subheader("⚖️ Blei")
    st.write(f"{blei} g – {blei_form}")
    st.caption("Wird benötigt, um Haken & Köder korrekt zu stabilisieren")

    st.info("🎯 Tipp: Passe Rig & Vorfach regelmäßig an Gewässer, Jahreszeit, Strömung und Fischverhalten an.")
