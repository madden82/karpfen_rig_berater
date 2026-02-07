import streamlit as st

# =========================
# Streamlit Setup
# =========================
st.set_page_config(page_title="🎣 Profi-Karpfen Rig & Vorfach Berater", layout="centered")
st.title("🎣 Profi-Karpfen Rig & Vorfach Berater")
st.caption("Profi-taugliche Rigs mit detaillierten Aufbauanleitungen")

# =========================
# RIG-DATENBANK: Hauptrigs & Unter-Rigs
# =========================
RIGS = [
    # ===== Hauptrigs =====
    {
        "name": "Hair Rig",
        "type": "haupt",
        "categories": ["boden", "allround"],
        "vorfach_material": "Mono 20lb",
        "vorfach_laenge": "20-25 cm",
        "haken": {"min":4,"max":6},  # dynamisch nach Gewicht
        "aufbau": [
            "1. Vorfach zuschneiden (Mono 20lb, 20-25cm)",
            "2. Haken anbinden (Wide Gape, passend zum Karpfengewicht)",
            "3. Haar mit Boiliestopper ausrichten",
            "4. Köder auf Haar aufziehen",
            "5. Blei direkt vor dem Rig fixieren, Stopper positionieren"
        ],
        "bilder": None,
        "max_cast": 200,
        "boat_ok": True,
        "weed_ok": False
    },
    {
        "name": "Ronnie Rig",
        "type": "haupt",
        "categories": ["popup"],
        "vorfach_material": "Stiff 18lb",
        "vorfach_laenge": "15-20 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Vorfach zuschneiden (Stiff 18lb, 15-20cm)",
            "2. Haken anbinden (Wide Gape)",
            "3. Anti-Tangle Sleeve positionieren",
            "4. Pop-Up Köder am Haar fixieren",
            "5. Optional Blei leicht vor dem Rig platzieren"
        ],
        "bilder": None,
        "max_cast": 130,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Chod Rig",
        "type": "haupt",
        "categories": ["popup","kraut"],
        "vorfach_material": "Stiff Short 20lb",
        "vorfach_laenge": "12-15 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Leadermaterial ~90-110cm vorbereiten",
            "2. Ringwirbel auffädeln",
            "3. Kurzes steifes Vorfach zuschneiden (12-15cm)",
            "4. Stopper für Vorfachposition fixieren",
            "5. Haken anbinden & Köder (Pop-Up) anbringen",
            "6. Bei Hindernissen: Fluorocarbon-Vorfach für Abriebschutz"
        ],
        "bilder": None,
        "max_cast": 120,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Wafter Rig",
        "type": "haupt",
        "categories": ["wafter","popup"],
        "vorfach_material": "Stiff 18lb",
        "vorfach_laenge": "15-18 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Kurzes Vorfach zuschneiden",
            "2. Haken anbinden",
            "3. Wafter Köder fixieren (balancieren)"
        ],
        "bilder": None,
        "max_cast": 120,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Helicopter Rig",
        "type": "haupt",
        "categories": ["boden","kraut"],
        "vorfach_material": "Mono 25lb",
        "vorfach_laenge": "20 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Leadcore oder Mono als Basis",
            "2. Wirbel & Perlen auffädeln",
            "3. Kurzes Vorfach anbinden",
            "4. Haken anbinden & Köder platzieren",
            "5. Bei Hindernissen Abriebschutz nutzen"
        ],
        "bilder": None,
        "max_cast": 140,
        "boat_ok": True,
        "weed_ok": True
    },

    # ===== Unter-Rigs (Varianten) =====
    {
        "name": "Slip-D Rig",
        "type": "unter",
        "parent": "D-Rig",
        "categories": ["popup"],
        "vorfach_material": "Stiff 20lb",
        "vorfach_laenge": "20 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Vorfach zuschneiden",
            "2. Ringwirbel auffädeln",
            "3. Haken anbinden & Stopper sauber setzen",
            "4. Pop-Up Köder anbringen"
        ],
        "bilder": None,
        "max_cast": 120,
        "boat_ok": True,
        "weed_ok": True
    },
    {
        "name": "Beehive Rig",
        "type": "unter",
        "parent": "Helicopter Rig",
        "categories": ["boden","kraut"],
        "vorfach_material": "Mono 20lb",
        "vorfach_laenge": "18 cm",
        "haken": {"min":4,"max":6},
        "aufbau": [
            "1. Vorfach zuschneiden (~18cm)",
            "2. Haken anbinden",
            "3. Kleine Perle zum Durchrutschen verhindern",
            "4. Köder auf Haar fixieren"
        ],
        "bilder": None,
        "max_cast": 130,
        "boat_ok": True,
        "weed_ok": True
    }
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

    truebung = st.slider("Wassertrübung (0=klar,10=trüb)",0,10,3,
                         help="Trübes Wasser erfordert auffällige Köder und Rigs.")
    jahreszeit = st.selectbox("Jahreszeit", ["Frühling","Sommer","Herbst","Winter"],
                              help="Saison beeinflusst Aktivität und Köderwahl.")
    temperatur = st.slider("Wassertemperatur (°C)",4,30,16,
                           help="Kalte Temperaturen reduzieren Aktivität der Karpfen.")

with col2:
    ausbringung = st.radio("Ausbringung", ["Wurf","Boot","Futterboot"],
                           help="Methode, wie der Köder ins Wasser kommt.")

    wurf_vom_boot = None
    if ausbringung=="Boot":
        wurf_vom_boot = st.radio("Vom Boot aus: Auslegen oder Wurf?", ["Auslegen","Wurf"])

    wurfweite = None
    if ausbringung=="Wurf" or wurf_vom_boot=="Wurf":
        wurfweite = st.slider("Wurfweite (m)",10,200,40)
        if wurfweite>150:
            st.warning("Sehr große Wurfweite: Helicopter-Rig und schweres Blei empfohlen.")

    muscheln = st.checkbox("Muscheln / Steine vorhanden 🐚")
    aeste = st.checkbox("Äste / Unterholz vorhanden 🌳")
    kraut = st.checkbox("Kraut vorhanden 🌿")
    andere_hindernisse = st.checkbox("Andere Hindernisse vorhanden ⚠️")

stromung = 0.0
if gewaesser in ["Fluss","Strom","Kanal"]:
    stromung = st.slider("Fließgeschwindigkeit (m/s)",0.0,2.0,0.5,0.1,
                         help="Beeinflusst Rig-Stabilität.")

aggro = st.slider("Aggressivität / Beißverhalten",1,10,5)
fischgewicht = st.slider("Erwartetes Karpfengewicht (kg)",5,35,15)
weissfisch = st.slider("Weißfisch-Anteil (%)",0,10,4)

# =========================
# KÖDER-EMPFEHLUNG
# =========================
def koeder_empfehlung():
    if temperatur<10 or jahreszeit=="Winter":
        return "Pop-Up",14,"Kaltwasser & Winter – auffällig"
    if weissfisch>=6:
        return "Harter Boilie",22,"Schützt vor Weißfisch"
    if aggro<=4:
        return "Wafter",18,"Vorsichtige Fische – unauffällig"
    if truebung>6:
        return "Leuchtender Pop-Up",16,"Trübes Wasser – auffällig"
    return "Boilie",20,"Standardköder – bewährt"

koeder,koeder_mm,koeder_text = koeder_empfehlung()

# =========================
# SCORE & FILTER
# =========================
def score_rig(rig):
    score=0
    # Köder-Rig Match
    if "pop-up" in koeder.lower() and "popup" not in rig["categories"]:
        score-=20
    # Hindernisse
    if (muscheln or aeste) and rig["vorfach_material"].lower() in ["fluoro","snagleader"]:
        score+=10
    if kraut and rig["weed_ok"]:
        score+=8
    if stromung>0.8 and "fluss" in rig["categories"]:
        score+=7
    if aggro<=4 and rig["name"].lower() in ["chod rig","wafter rig","slip-d rig"]:
        score+=6
    if "boden" in rig["categories"]:
        score+=3
    if "allround" in rig["categories"]:
        score+=3
    return score

def rig_empfehlung():
    # Step1: Hauptrigs filtern
    hauptrigs=[r for r in RIGS if r["type"]=="haupt"]
    filtered=[]
    for rig in hauptrigs:
        if wurfweite and wurfweite>rig["max_cast"]:
            continue
        if ausbringung!="Wurf" and not rig["boat_ok"]:
            continue
        filtered.append((score_rig(rig),rig))
    filtered.sort(key=lambda x:x[0],reverse=True)
    # Top Rig
    top_rigs=[r for s,r in filtered[:1]]
    # Unter-Rig nur wenn Haupt-Rig passt
    for rig in RIGS:
        if rig["type"]=="unter" and any(rig["parent"]==tr["name"] for tr in top_rigs):
            top_rigs.append(rig)
    return top_rigs

# =========================
# AUSGABE
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    rigs=rig_empfehlung()
    if not rigs:
        st.warning("Keine passenden Rigs gefunden.")
    else:
        st.success("✅ Deine persönliche Empfehlung")
        st.subheader("🍡 Köder")
        st.write(f"{koeder} – {koeder_mm} mm")
        st.caption(koeder_text)

        rig=rigs[0]
        st.subheader("🪝 Empfohlenes Rig (Hauptrig)")
        st.write(f"**{rig['name']}** ({', '.join(rig['categories'])})")
        st.write(f"- Vorfach: {rig['vorfach_material']}, {rig['vorfach_laenge']}")
        # Dynamische Hakengröße nach Karpfengewicht
        if fischgewicht>=25:
            hakengröße=rig["haken"]["min"]
        else:
            hakengröße=rig["haken"]["max"]
        st.write(f"- Haken: Größe {hakengröße} Wide Gape")
        if rig["bilder"]:
            st.image(rig["bilder"])
        st.write("**Aufbau:**")
        for s in rig["aufbau"]:
            st.write(f"- {s}")

        # Unter-Rig optional
        if len(rigs)>1:
            if st.checkbox("Optional: Unter-Rig anzeigen"):
                rig2=rigs[1]
                st.subheader("🪝 Optionales Rig (Unter-Rig)")
                st.write(f"**{rig2['name']}** ({', '.join(rig2['categories'])})")
                st.write(f"- Vorfach: {rig2['vorfach_material']}, {rig2['vorfach_laenge']}")
                if fischgewicht>=25:
                    hakengröße2=rig2["haken"]["min"]
                else:
                    hakengröße2=rig2["haken"]["max"]
                st.write(f"- Haken: Größe {hakengröße2} Wide Gape")
                if rig2["bilder"]:
                    st.image(rig2["bilder"])
                st.write("**Aufbau:**")
                for s in rig2["aufbau"]:
                    st.write(f"- {s}")
