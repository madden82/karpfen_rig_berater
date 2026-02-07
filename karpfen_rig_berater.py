import streamlit as st

# =========================
# Streamlit Setup
# =========================
st.set_page_config(page_title="🎣 Profi-Karpfen Rig & Vorfach Berater", layout="centered")
st.title("🎣 Profi-Karpfen Rig & Vorfach Berater")
st.caption("Detaillierte Baupläne für Carp Rigs – Profi-tauglich und dynamisch angepasst")

# =========================
# Rig-Datenbank
# =========================
RIGS = [
    {
        "name": "Hair Rig",
        "categories": ["boden", "allround"],
        "vorfach_material": "Mono",
        "vorfach_laenge": "20-25 cm",
        "haken": "Größe 6 Wide Gape",
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Haken anbinden",
            "3. Haar mit Boiliestopper ausrichten",
            "4. Köder auf Haar aufziehen"
        ],
        "bilder": None,
        "max_cast": 200,
        "boat_ok": True,
        "weed_ok": False
    },
    {
        "name": "Ronnie Rig",
        "categories": ["popup"],
        "vorfach_material": "Stiff",
        "vorfach_laenge": "15-20 cm",
        "haken": "Größe 4 Wide Gape",
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Haken anbinden (Wide Gape)",
            "3. Anti-Tangle Sleeve positionieren",
            "4. Pop-Up am Haar fixieren"
        ],
        "bilder": None,
        "max_cast": 130,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Chod Rig",
        "categories": ["popup", "kraut"],
        "vorfach_material": "Stiff Short",
        "vorfach_laenge": "12-15 cm",
        "haken": "Größe 4 Wide Gape",
        "aufbau": [
            "1. Leadermaterial ~90-110 cm",
            "2. Ringwirbel auffädeln",
            "3. Kurzes steifes Vorfach",
            "4. Stopper fixieren",
            "5. Haken anbinden und Köder anbringen"
        ],
        "bilder": None,
        "max_cast": 120,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Wafter Rig",
        "categories": ["wafter"],
        "vorfach_material": "Stiff",
        "vorfach_laenge": "15-18 cm",
        "haken": "Größe 6 Wide Gape",
        "aufbau": [
            "1. Kurzes Vorfach zuschneiden",
            "2. Haken anbinden",
            "3. Wafter fixieren"
        ],
        "bilder": None,
        "max_cast": 120,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Helicopter Rig",
        "categories": ["boden", "kraut"],
        "vorfach_material": "Mono",
        "vorfach_laenge": "20 cm",
        "haken": "Größe 6 Wide Gape",
        "aufbau": [
            "1. Leadcore/Mono als Basis",
            "2. Wirbel & Perlen auffädeln",
            "3. Kurzes Vorfach anbinden",
            "4. Haken anbinden und Köder platzieren"
        ],
        "bilder": None,
        "max_cast": 140,
        "boat_ok": True,
        "weed_ok": True
    },
    # … hier weitere Rigs nach Bedarf hinzufügen …
]

# =========================
# USER INPUTS (Spaltenlayout)
# =========================
st.header("Eingaben")

col1, col2 = st.columns(2)

with col1:
    gewaesser = st.selectbox(
        "Gewässertyp",
        ["Teich", "See", "Baggersee", "Weiher", "Kanal", "Fluss", "Strom", "Altwasser"],
        help="Wählen Sie das Gewässer. Fließgewässer erfordern stabile Rigs."
    )

    truebung = st.slider(
        "Wassertrübung (0 = klar, 10 = trüb)",
        0, 10, 3,
        help="Trübes Wasser erfordert auffälligere Köder und Rigs."
    )

    jahreszeit = st.selectbox(
        "Jahreszeit",
        ["Frühling", "Sommer", "Herbst", "Winter"],
        help="Saison beeinflusst Aktivität und Köderwahl."
    )

    temperatur = st.slider(
        "Wassertemperatur (°C)", 4, 30, 16,
        help="Kalte Temperaturen reduzieren die Aktivität der Karpfen."
    )

with col2:
    ausbringung = st.radio(
        "Ausbringung", ["Wurf", "Boot", "Futterboot"],
        help="Methode, wie der Köder ins Wasser kommt."
    )

    wurf_vom_boot = None
    if ausbringung == "Boot":
        wurf_vom_boot = st.radio("Vom Boot aus: Auslegen oder Wurf?", ["Auslegen", "Wurf"])

    wurfweite = None
    if ausbringung == "Wurf" or wurf_vom_boot == "Wurf":
        wurfweite = st.slider(
            "Wurfweite (m)", 10, 200, 40,
            help="Entscheidet, welche Rigs für die Entfernung geeignet sind."
        )
        if wurfweite > 150:
            st.warning("Sehr große Wurfweite: Helicopter-Rig und schweres Blei empfohlen.")

    muscheln = st.checkbox("Muscheln / Steine vorhanden 🐚")
    aeste = st.checkbox("Äste / Unterholz vorhanden 🌳")
    kraut = st.checkbox("Kraut vorhanden 🌿")
    andere_hindernisse = st.checkbox("Andere Hindernisse vorhanden ⚠️")

stromung = 0.0
if gewaesser in ["Fluss", "Strom", "Kanal"]:
    stromung = st.slider("Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1,
                         help="0 = kaum Strömung, 2 = starke Strömung. Beeinflusst Rig-Stabilität.")

aggro = st.slider("Aggressivität / Beißverhalten", 1, 10, 5,
                  help="Je vorsichtiger die Fische, desto unauffälliger Rig und Köder.")
fischgewicht = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4)

# =========================
# KÖDER EMPFEHLUNG
# =========================
def koeder_empfehlung():
    if temperatur < 10 or jahreszeit == "Winter":
        return "Pop-Up", 14, "Kaltwasser & Winter – auffällig"
    if weissfisch >= 6:
        return "Harter Boilie", 22, "Schützt vor Weißfisch"
    if aggro <= 4:
        return "Wafter", 18, "Vorsichtige Fische – unauffällig"
    if truebung > 6:
        return "Leuchtender Pop-Up", 16, "Trübes Wasser – auffällig"
    return "Boilie", 20, "Standardköder – bewährt"

koeder, koeder_mm, koeder_text = koeder_empfehlung()

# =========================
# SCORE-FUNKTION
# =========================
def score_rig(rig):
    score = 0
    name = rig["name"].lower()

    # Köder-Rig-Validierung
    if "pop-up" in koeder.lower() and "popup" not in rig["categories"]:
        score -= 20

    # Hindernisse → Abriebfestigkeit
    if (muscheln or aeste) and rig["vorfach_material"].lower() in ["fluoro", "snagleader"]:
        score += 10
    if kraut and rig["weed_ok"]:
        score += 8
    if stromung > 0.8 and "fluss" in rig["categories"]:
        score += 7
    if aggro <= 4 and name in ["chod rig", "wafter rig", "slip d rig"]:
        score += 6
    if "boden" in rig["categories"]:
        score += 3
    if "allround" in rig["categories"]:
        score += 3
    return score

# =========================
# TOP-RIG FILTER
# =========================
def rig_empfehlung():
    scored = []
    for rig in RIGS:
        if wurfweite and wurfweite > rig["max_cast"]:
            continue
        if ausbringung != "Wurf" and not rig["boat_ok"]:
            continue
        scored.append((score_rig(rig), rig))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for s, r in scored[:2]]  # 1 Rig + optional 2. Rig

# =========================
# AUSGABE
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    top_rigs = rig_empfehlung()
    if not top_rigs:
        st.warning("Keine passenden Rigs gefunden. Bitte Eingaben prüfen.")
    else:
        st.success("✅ Deine persönliche Empfehlung")
        st.subheader("🍡 Köder")
        st.write(f"{koeder} – {koeder_mm} mm")
        st.caption(koeder_text)

        rig = top_rigs[0]
        st.subheader("🪝 Empfohlenes Rig")
        st.write(f"**{rig['name']}** ({', '.join(rig['categories'])})")
        st.write(f"- Vorfach: {rig['vorfach_material']}, {rig['vorfach_laenge']}")
        st.write(f"- Haken: {rig['haken']}")
        if rig["bilder"]:
            st.image(rig["bilder"])
        st.write("**Aufbau:**")
        for schritt in rig["aufbau"]:
            st.write(f"- {schritt}")

        # Optionales Rig
        if len(top_rigs) > 1:
            if st.checkbox("Optional: zweites Rig anzeigen"):
                rig2 = top_rigs[1]
                st.write(f"**{rig2['name']}** ({', '.join(rig2['categories'])})")
                st.write(f"- Vorfach: {rig2['vorfach_material']}, {rig2['vorfach_laenge']}")
                st.write(f"- Haken: {rig2['haken']}")
                if rig2["bilder"]:
                    st.image(rig2["bilder"])
                st.write("**Aufbau:**")
                for schritt in rig2["aufbau"]:
                    st.write(f"- {schritt}")
