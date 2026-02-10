import streamlit as st


def eingaben():
    """
    Sammelt alle Benutzereingaben über Streamlit
    und gibt sie als Dictionary zurück.
    KEINE Berechnungen hier!
    """

    st.header("🎣 Grundeinstellungen")

    # ----------------------------
    # 1️⃣ Gewässer & Strömung
    # ----------------------------
    st.subheader("1️⃣ Gewässer & Strömung")

    gewaesser_typ = st.radio(
        "Gewässertyp",
        options=["Stillgewässer", "Fließgewässer"]
    )

    if gewaesser_typ == "Stillgewässer":
        stroemung = "keine"
        stroemung_m_s = 0.0
        st.info("ℹ️ Stillgewässer: Keine relevante Strömung")
    else:
        stroemung = st.select_slider(
            "Stärke der Strömung",
            options=["leicht", "mittel", "stark"]
        )
        stroemung_m_s = {
            "leicht": 0.2,
            "mittel": 0.6,
            "stark": 1.4
        }[stroemung]

    # ----------------------------
    # 2️⃣ Angeltechnik & Distanz
    # ----------------------------
    st.subheader("2️⃣ Angeltechnik & Distanz")

    angeltechnik = st.radio(
        "Angeltechnik",
        options=[
            "Uferwurf",
            "Bootwurf",
            "Bootablage",
            "Futterboot"
        ]
    )

    if angeltechnik in ["Uferwurf", "Bootwurf"]:
        wurfweite = st.slider(
            "Wurfweite in Metern",
            min_value=0,
            max_value=200,
            value=50,
            step=5
        )
    else:
        wurfweite = 0
        st.info("ℹ️ Bei Bootablage / Futterboot keine Wurfweite relevant")

    # ----------------------------
    # 3️⃣ Bodenbeschaffenheit
    # ----------------------------
    st.subheader("3️⃣ Bodenbeschaffenheit")

    bodenart = st.radio(
        "Bodenart am Angelplatz",
        options=["weich", "mittel", "hart"]
    )

    # ----------------------------
    # 4️⃣ Zielfisch & Umgebung
    # ----------------------------
    st.subheader("4️⃣ Karpfen & Umgebung")

    karpfen_gewicht = st.slider(
        "Erwartetes Karpfengewicht (kg)",
        min_value=1,
        max_value=40,
        value=10
    )

    karpfen_verhalten = st.radio(
        "Karpfenverhalten",
        options=["aktiv", "scheu", "beide"]
    )

    hindernisse = st.radio(
        "Gibt es Hindernisse (Holz, Kraut, Steine)?",
        options=["ja", "nein"]
    ) == "ja"

    wassertrubung = st.radio(
        "Wassertrübung",
        options=["klar", "leicht trüb", "trüb"]
    )

    # ----------------------------
    # 5️⃣ Jahreszeit & Temperatur
    # ----------------------------
    st.subheader("5️⃣ Jahreszeit & Temperatur")

    jahreszeit = st.selectbox(
        "Jahreszeit",
        options=["Frühling", "Sommer", "Herbst", "Winter"]
    )

    wassertemperatur = st.slider(
        "Wassertemperatur (°C)",
        min_value=0,
        max_value=30,
        value=15
    )

    # ----------------------------
    # 🔁 Rückgabe aller Eingaben
    # ----------------------------
    return {
        "gewaesser_typ": gewaesser_typ,
        "stroemung": stroemung,
        "stroemung_m_s": stroemung_m_s,
        "angeltechnik": angeltechnik,
        "wurfweite": wurfweite,
        "bodenart": bodenart,
        "karpfen_gewicht": karpfen_gewicht,
        "karpfen_verhalten": karpfen_verhalten,
        "hindernisse": hindernisse,
        "wassertrubung": wassertrubung,
        "jahreszeit": jahreszeit,
        "wassertemperatur": wassertemperatur
    }
"""
TEIL 2 – Berechnungslogik für
- Bleigewicht
- Vorfachlänge

KEIN Streamlit!
KEINE Eingaben!
"""

# -------------------------------------------------
# 1️⃣ Basis-Bleigewichte nach Karpfengewicht (kg)
# -------------------------------------------------
BASIS_BLEI = {
    1: 12,
    3: 25,
    5: 35,
    10: 50,
    15: 60,
    20: 70,
    25: 80,
    30: 90,
    35: 100,
    40: 110
}

# -------------------------------------------------
# 2️⃣ Faktoren für Boden & Strömung
# -------------------------------------------------
BODEN_FAKTOR = {
    "weich": 0.9,
    "mittel": 1.0,
    "hart": 1.1
}

STROEMUNG_FAKTOR = {
    "keine": 1.0,
    "leicht": 1.05,
    "mittel": 1.10,
    "stark": 1.20
}

# -------------------------------------------------
# 3️⃣ Vorfachlängen (cm) nach Boden
# (min, max)
# -------------------------------------------------
VORFACH_LAENGEN = {
    "hart": (10, 20),
    "mittel": (15, 30),
    "weich": (25, 50)
}


# =================================================
# 🔩 BLEI-BERECHNUNG
# =================================================
def berechne_bleigewicht(karpfen_gewicht, bodenart, stroemung):
    """
    Berechnet das empfohlene Bleigewicht in Gramm.

    Parameter:
    - karpfen_gewicht (int)
    - bodenart (str)
    - stroemung (str)

    Rückgabe:
    - bleigewicht (float)
    """

    # Basisgewicht anhand der Gewichtsklasse ermitteln
    basis_gewicht = None
    for grenze in sorted(BASIS_BLEI.keys()):
        if karpfen_gewicht <= grenze:
            basis_gewicht = BASIS_BLEI[grenze]
            break

    # Sicherheitsfallback
    if basis_gewicht is None:
        basis_gewicht = BASIS_BLEI[max(BASIS_BLEI.keys())]

    # Faktoren anwenden
    boden_faktor = BODEN_FAKTOR[bodenart]
    stroemung_faktor = STROEMUNG_FAKTOR[stroemung]

    endgewicht = basis_gewicht * boden_faktor * stroemung_faktor

    return round(endgewicht, 1)


# =================================================
# 📏 VORFACH-BERECHNUNG
# =================================================
def berechne_vorfachlaenge(bodenart, karpfen_verhalten):
    """
    Berechnet eine sinnvolle Vorfachlänge in cm.

    Parameter:
    - bodenart (str)
    - karpfen_verhalten (str)

    Rückgabe:
    - vorfachlaenge (int)
    """

    min_laenge, max_laenge = VORFACH_LAENGEN[bodenart]

    if karpfen_verhalten in ["scheu", "beide"]:
        return max_laenge
    else:
        return int((min_laenge + max_laenge) / 2)
"""
TEIL 3 – Rig-Auswahl & Montage-Logik

KEIN Streamlit
KEINE UI
"""

# -------------------------------------------------
# 1️⃣ Definition der verfügbaren Rigs
# -------------------------------------------------
RIGS = {
    "KD-Rig": {
        "beschreibung": "Sehr vielseitiges Allround-Rig mit guter Hakquote",
        "boden": ["hart", "mittel"],
        "verhalten": ["aktiv", "beide"],
        "distanz": "kurz_mittel"
    },
    "D-Rig": {
        "beschreibung": "Ideal für scheue Karpfen bei klarem Wasser",
        "boden": ["hart"],
        "verhalten": ["scheu", "beide"],
        "distanz": "kurz"
    },
    "Helikopter-Rig": {
        "beschreibung": "Perfekt für weichen Boden und schlammige Bereiche",
        "boden": ["weich"],
        "verhalten": ["aktiv", "scheu", "beide"],
        "distanz": "alle"
    },
    "Combi-Pop-Up-Rig": {
        "beschreibung": "Für große Distanzen und schwierige Bedingungen",
        "boden": ["mittel", "hart"],
        "verhalten": ["aktiv"],
        "distanz": "weit"
    }
}

# -------------------------------------------------
# 2️⃣ Hilfsfunktion für Distanzklassifizierung
# -------------------------------------------------
def _distanz_typ(wurfweite):
    if wurfweite == 0:
        return "alle"
    if wurfweite <= 60:
        return "kurz"
    if wurfweite <= 120:
        return "kurz_mittel"
    return "weit"


# =================================================
# 🎣 RIG-AUSWAHL
# =================================================
def waehle_rig(bodenart, karpfen_verhalten, wurfweite):
    """
    Wählt ein passendes Rig basierend auf den Bedingungen.

    Parameter:
    - bodenart (str)
    - karpfen_verhalten (str)
    - wurfweite (int)

    Rückgabe:
    - rig_name (str)
    - rig_beschreibung (str)
    """

    distanz = _distanz_typ(wurfweite)

    # Prioritätslogik (bewusst klar & lesbar)
    if bodenart == "weich":
        rig = "Helikopter-Rig"
        return rig, RIGS[rig]["beschreibung"]

    if karpfen_verhalten == "scheu" and bodenart == "hart":
        rig = "D-Rig"
        return rig, RIGS[rig]["beschreibung"]

    if distanz == "weit":
        rig = "Combi-Pop-Up-Rig"
        return rig, RIGS[rig]["beschreibung"]

    # Fallback / Allround
    rig = "KD-Rig"
    return rig, RIGS[rig]["beschreibung"]
"""
TEIL 4 – Spotwahl & Platzierung
Bezogen auf Gewässertyp, Boden, Strömung UND gewähltes Rig
"""

def spotwahl(
    gewaessertyp,
    boden,
    stroemung,
    fischverhalten,
    rig_name
):
    """
    Gibt Spot- & Platzierungstipps zurück, die zum Rig passen.
    """

    tipps = []

    # --------------------------------------------
    # 1️⃣ Grundlogik: Gewässertyp
    # --------------------------------------------
    if "Keine Strömung" in gewaessertyp:
        tipps.append(
            "Stehendes Gewässer: Karpfen ziehen oft entlang von Kanten, "
            "Plateaus oder Übergängen zwischen hartem und weichem Boden."
        )
    else:
        tipps.append(
            "Fließgewässer: Karpfen stehen selten direkt in der Strömung – "
            "suche strömungsberuhigte Zonen."
        )

    # --------------------------------------------
    # 2️⃣ Bodenabhängige Platzierung
    # --------------------------------------------
    if boden == "hart":
        tipps.append(
            "Harter Boden: Platziere das Rig auf Kies- oder Sandflächen, "
            "ideal sind kleine Erhöhungen oder harte Spots zwischen weichen Zonen."
        )
    elif boden == "mittel":
        tipps.append(
            "Mittlerer Boden: Übergänge sind Schlüsselspots. "
            "Karpfen fressen gern dort, wo sich Nahrung sammelt."
        )
    else:
        tipps.append(
            "Weicher Boden: Vermeide tiefen Faulschlamm. "
            "Suche kleine Erhebungen, Krautränder oder härtere Einschlüsse."
        )

    # --------------------------------------------
    # 3️⃣ Strömungslogik
    # --------------------------------------------
    if stroemung == "keine":
        tipps.append(
            "Ohne Strömung: Karpfen bewegen sich großflächig. "
            "Futterplatz aufbauen und präzise ablegen."
        )
    elif stroemung == "leicht":
        tipps.append(
            "Leichte Strömung: Ideale Spots sind hinter kleinen Hindernissen "
            "oder an der stromabgewandten Seite von Kanten."
        )
    elif stroemung == "mittel":
        tipps.append(
            "Mittlere Strömung: Nur Strömungsschatten befischen – "
            "z. B. Buhnen, Steine, Außenkurven."
        )
    else:
        tipps.append(
            "Starke Strömung: Karpfen stehen sehr lokal. "
            "Exakt hinter großen Hindernissen oder in ruhigen Rückströmungen."
        )

    # --------------------------------------------
    # 4️⃣ Fischverhalten
    # --------------------------------------------
    if fischverhalten == "scheu":
        tipps.append(
            "Scheue Karpfen: Abstand zu stark befischten Plätzen halten. "
            "Leise Ablage, wenig Futter, natürliche Präsentation."
        )
    elif fischverhalten == "aktiv":
        tipps.append(
            "Aktive Karpfen: Suchbewegungen nutzen. "
            "Futterplätze, Zugrouten und offene Bereiche befischen."
        )
    else:
        tipps.append(
            "Gemischtes Verhalten: Kombiniere einen sicheren Spot "
            "mit einem etwas offensiveren Futterplatz."
        )

    # --------------------------------------------
    # 5️⃣ RIG-SPEZIFISCHE SPOT-OPTIMIERUNG
    # --------------------------------------------
    if rig_name == "Helikopter-Rig":
        tipps.append(
            "Helikopter-Rig: Ideal für weichen Boden. "
            "Kann auch auf unbekanntem Untergrund sicher abgelegt werden."
        )

    elif rig_name == "D-Rig":
        tipps.append(
            "D-Rig: Sehr präzise fischen! "
            "Nur auf sauberen, harten Spots einsetzen – kein Kraut, kein Schlamm."
        )

    elif rig_name == "Combi-Pop-Up-Rig":
        tipps.append(
            "Combi-Pop-Up-Rig: Perfekt für Distanz. "
            "Auch leicht verschlammte Bereiche oder Krautlücken befischbar."
        )

    elif rig_name == "KD-Rig":
        tipps.append(
            "KD-Rig: Allrounder. "
            "Ideal auf Futterplätzen, harten Böden oder gemischtem Untergrund."
        )

    # --------------------------------------------
    # 6️⃣ Typische Fehler vermeiden
    # --------------------------------------------
    tipps.append(
        "Typischer Fehler: Zu tief im Schlamm oder direkt in der Hauptströmung ablegen. "
        "Im Zweifel lieber einen halben Meter versetzen."
    )

    return tipps
