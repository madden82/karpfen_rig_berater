import streamlit as st

# =====================================================
# GRUNDLAGEN & HILFSFUNKTIONEN
# =====================================================

def gewaesser_hat_stroemung(gewaesser):
    return gewaesser in ["Fluss", "Strom"]


def stroemungsfaktor(stroemung):
    # entspricht Excel "Faktor für Strömung"
    faktoren = {
        "langsam": 0.5,
        "mittel": 1.0,
        "schnell": 1.5
    }
    return faktoren.get(stroemung, 0.0)


# =====================================================
# BLEI – BLEITYP (nur Boden, Wurfweite, Strömung)
# =====================================================

def bestimme_bleityp(boden, wurfweite, stroemung_label):
    punkte = {
        "Flat Pear": 0,
        "Birnenblei": 0,
        "Distance / Torpedo": 0,
        "Gripper": 0
    }

    # -------------------------
    # Boden (Excel-konform)
    # -------------------------
    if boden == "weich":
        punkte["Flat Pear"] += 1
    elif boden == "mittel":
        punkte["Birnenblei"] += 1
    elif boden == "hart":
        punkte["Distance / Torpedo"] += 1

    # -------------------------
    # Wurfweite
    # -------------------------
    if wurfweite > 90:
        punkte["Distance / Torpedo"] += 1
    elif 50 <= wurfweite <= 90:
        punkte["Birnenblei"] += 1
    else:
        punkte["Flat Pear"] += 1

    # -------------------------
    # Strömung (Priorität)
    # -------------------------
    if stroemung_label == "schnell":
        punkte["Gripper"] += 2
    elif stroemung_label == "mittel":
        punkte["Birnenblei"] += 1

    return max(punkte, key=punkte.get)


# =====================================================
# BLEI – UNTERBLEI
# =====================================================

def bestimme_unterblei(bleityp, stroemung_label):
    if bleityp == "Gripper":
        return "kein Unterblei"
    if stroemung_label in ["mittel", "schnell"]:
        return "Klemmblei"
    return "Schrotblei"


# =====================================================
# BLEI – GEWICHT (mathematisch, reproduzierbar)
# =====================================================

def bestimme_bleigewicht(wurfweite, stroemung_faktor):
    # Basisgewicht
    gewicht = 70

    # Distanz-Einfluss
    gewicht += wurfweite * 0.35

    # Strömungs-Einfluss
    gewicht += stroemung_faktor * 40

    # sinnvolle Grenzen
    gewicht = max(70, min(200, gewicht))

    return round(gewicht, 0)


# =====================================================
# VORFACH
# =====================================================

def bestimme_vorfach(boden, hindernisse, stroemung_label):
    if hindernisse:
        return "beschichtetes Geflecht (25–35 lb)"
    if stroemung_label in ["mittel", "schnell"]:
        return "beschichtetes Geflecht"
    if boden == "weich":
        return "weiches Geflecht (20–25 lb)"
    return "Fluorocarbon / steifes Material"


# =====================================================
# HAKEN (korrekte Nummernlogik!)
# =====================================================

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


# =====================================================
# STREAMLIT UI
# =====================================================

st.title("🎣 Karpfen-Rig-Berater")

# -------------------------
# GEWÄSSER
# -------------------------
gewaesser = st.selectbox(
    "Gewässertyp",
    ["See", "Teich", "Weiher", "Stauer", "Stausee", "Fluss", "Strom"]
)

# -------------------------
# STRÖMUNG
# -------------------------
stroemung_label = "keine"
stroemung_faktor_wert = 0.0

if gewaesser_hat_stroemung(gewaesser):
    stroemung_label = st.radio(
        "Fließgeschwindigkeit",
        ["langsam", "mittel", "schnell"],
        horizontal=True
    )
    stroemung_faktor_wert = stroemungsfaktor(stroemung_label)

# -------------------------
# ANGELART
# -------------------------
angelart = st.selectbox(
    "Angelart",
    ["Ufer – werfen", "Boot – werfen", "Boot – ablegen", "Futterboot"]
)

wurfweite = 0
if "werfen" in angelart:
    wurfweite = st.slider("Wurfweite (m)", 10, 150, 60)

# -------------------------
# BODEN
# -------------------------
boden = st.selectbox("Bodenbeschaffenheit", ["weich", "mittel", "hart"])

# -------------------------
# HINDERNISSE
# -------------------------
hindernisse = st.multiselect(
    "Hindernisse / Störfaktoren",
    [
        "Kraut",
        "Muschelbänke",
        "Steine",
        "Totholz",
        "starker Weißfischbestand",
        "Krebse"
    ]
)

# -------------------------
# KÖDER & FISCH
# -------------------------
koeder_mm = st.selectbox("Ködergröße (mm)", [12, 16, 18, 20, 24])
max_karpfen_kg = st.slider("Max. erwartete Karpfengröße (kg)", 5, 35, 15)

# =====================================================
# BERECHNUNG
# =====================================================

if st.button("Rig berechnen"):
    bleityp = bestimme_bleityp(boden, wurfweite, stroemung_label)
    unterblei = bestimme_unterblei(bleityp, stroemung_label)
    bleigewicht = bestimme_bleigewicht(wurfweite, stroemung_faktor_wert)
    vorfach = bestimme_vorfach(boden, hindernisse, stroemung_label)
    haken = bestimme_hakengroesse(koeder_mm, max_karpfen_kg)

    st.subheader("✅ Empfehlung")

    st.write(f"**Bleityp:** {bleityp}")
    st.write(f"**Unterblei:** {unterblei}")
    st.write(f"**Bleigewicht:** ca. {bleigewicht} g")
    st.write(f"**Vorfach:** {vorfach}")
    st.write(f"**Hakengröße:** {haken}")

    if hindernisse:
        st.info(
            "ℹ️ Bei Hindernissen empfiehlt sich der Einsatz eines "
            "Safety Clips oder Drop-Off-Systems, "
            "damit sich das Blei im Hängerfall lösen kann. "
            "Inline- und Wirbelbleie bleiben weiterhin nutzbar."
        )
