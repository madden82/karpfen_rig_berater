import streamlit as st
import pandas as pd

# -------------------------------
# BLEI – mathematische Bewertung
# -------------------------------

def bestimme_bleityp(boden, distanz, stroemung, wind, tiefe):
    scores = {
        "Birnenblei": 0,
        "Flat Pear": 0,
        "Distance / Torpedo": 0,
        "Gripper": 0
    }

    # Boden
    if boden == "weich":
        scores["Flat Pear"] += 3
    elif boden == "mittel":
        scores["Birnenblei"] += 2
    else:
        scores["Distance / Torpedo"] += 2

    # Distanz
    if distanz >= 100:
        scores["Distance / Torpedo"] += 3
    elif distanz >= 60:
        scores["Birnenblei"] += 2

    # Strömung
    if stroemung >= 0.7:
        scores["Gripper"] += 4
    elif stroemung >= 0.3:
        scores["Birnenblei"] += 2

    # Wind
    if wind >= 5:
        scores["Distance / Torpedo"] += 2

    # Tiefe
    if tiefe >= 8:
        scores["Birnenblei"] += 1

    return max(scores, key=scores.get)


# -------------------------------
# UNTERBLEI
# -------------------------------

def bestimme_unterblei(bleityp, stroemung):
    if bleityp == "Gripper":
        return "kein Unterblei"
    if stroemung >= 0.5:
        return "Klemmblei"
    return "Schrotblei"


# -------------------------------
# BLEIGEWICHT (mathematisch)
# -------------------------------

def bestimme_bleigewicht(distanz, stroemung, tiefe):
    gewicht = 70

    gewicht += distanz * 0.3
    gewicht += stroemung * 40
    gewicht += tiefe * 2

    return round(min(max(gewicht, 70), 200), 0)


# -------------------------------
# VORFACH
# -------------------------------

def bestimme_vorfach(boden, hindernisse, stroemung):
    if hindernisse:
        return "beschichtetes Geflecht (25–35 lb)"
    if stroemung >= 0.4:
        return "beschichtetes Geflecht"
    if boden == "weich":
        return "weiches Geflecht (20–25 lb)"
    return "Fluorocarbon / steifes Material"


# -------------------------------
# HAKEN (korrekte Nummernlogik!)
# -------------------------------

def basis_haken_nach_koeder(koeder_mm):
    if koeder_mm <= 16:
        return (8, 6)
    elif koeder_mm <= 20:
        return (6, 4)
    else:
        return (4, 2)


def bestimme_hakengroesse(koeder_mm, max_karpfen_kg):
    haken_gross, haken_klein = basis_haken_nach_koeder(koeder_mm)

    if max_karpfen_kg >= 20:
        haken_gross -= 2
        haken_klein -= 2
    elif max_karpfen_kg >= 10:
        haken_gross -= 1
        haken_klein -= 1

    haken_gross = max(haken_gross, 2)
    haken_klein = max(haken_klein, 2)

    return f"Größe {haken_gross}–{haken_klein}"


# -------------------------------
# STREAMLIT UI
# -------------------------------

st.title("🎣 Karpfen Rig Berater")

st.header("Gewässer & Bedingungen")

boden = st.selectbox("Bodenhärte", ["weich", "mittel", "hart"])
distanz = st.slider("Wurfweite (m)", 20, 150, 70)
stroemung = st.slider("Strömung (m/s)", 0.0, 1.5, 0.0)
wind = st.slider("Wind (m/s)", 0, 15, 3)
tiefe = st.slider("Wassertiefe (m)", 1, 20, 5)
hindernisse = st.checkbox("Hindernisse vorhanden?")

st.header("Köder & Fisch")

koeder_mm = st.selectbox("Ködergröße (mm)", [12, 16, 18, 20, 24])
max_karpfen_kg = st.slider("Max. erwartete Karpfengröße (kg)", 5, 35, 15)

if st.button("Rig berechnen"):
    bleityp = bestimme_bleityp(boden, distanz, stroemung, wind, tiefe)
    unterblei = bestimme_unterblei(bleityp, stroemung)
    bleigewicht = bestimme_bleigewicht(distanz, stroemung, tiefe)
    vorfach = bestimme_vorfach(boden, hindernisse, stroemung)
    haken = bestimme_hakengroesse(koeder_mm, max_karpfen_kg)

    st.subheader("✅ Empfehlung")

    st.write(f"**Bleityp:** {bleityp}")
    st.write(f"**Unterblei:** {unterblei}")
    st.write(f"**Bleigewicht:** ca. {bleigewicht} g")
    st.write(f"**Vorfach:** {vorfach}")
    st.write(f"**Hakengröße:** {haken}")
