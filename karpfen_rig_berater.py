import streamlit as st

# =========================
# Streamlit Setup
# =========================
st.set_page_config(
    page_title="🎣 Profi-Karpfen Rig & Vorfach Berater",
    layout="centered"
)
st.title("🎣 Profi-Karpfen Rig & Vorfach Berater")
st.caption("Detaillierte Baupläne für Carp Rigs – Profi-tauglich und dynamisch angepasst")

# =========================
# Rig-Datenbank (Beispiel 30 Rigs, erweiterbar)
# =========================
RIGS = [
    {"name":"Hair Rig","categories":["boden","allround"],"max_cast":200,"boat_ok":True,"weed_ok":False},
    {"name":"Blowback Rig","categories":["boden","allround"],"max_cast":160,"boat_ok":True,"weed_ok":False},
    {"name":"KD Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"Ronnie Rig","categories":["popup"],"max_cast":130,"boat_ok":True,"weed_ok":True},
    {"name":"Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Slip D Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Wafter Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Helicopter Rig","categories":["boden","kraut"],"max_cast":140,"boat_ok":True,"weed_ok":True},
    {"name":"Multi Rig","categories":["boden","wafter"],"max_cast":160,"boat_ok":True,"weed_ok":False},
    {"name":"Bolt Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"German Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Hinged Stiff Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True},
    {"name":"Line-Aligner Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"Teller Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"Zig Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"Surface Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":False},
    {"name":"Offset Rig","categories":["boden"],"max_cast":150,"boat_ok":True,"weed_ok":False},
    {"name":"KD Mini Rig","categories":["boden"],"max_cast":120,"boat_ok":True,"weed_ok":False},
    {"name":"Mini Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Pop-Up Chod Rig","categories":["popup","kraut"],"max_cast":130,"boat_ok":True,"weed_ok":True},
    {"name":"Anti-Weed Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Floating Wafter Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Heavy Distance Rig","categories":["boden"],"max_cast":200,"boat_ok":True,"weed_ok":False},
    {"name":"Fluoro Rig","categories":["boden"],"max_cast":160,"boat_ok":True,"weed_ok":False},
    {"name":"Stiff Pop Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True},
    {"name":"Long Chod Rig","categories":["popup","kraut"],"max_cast":150,"boat_ok":True,"weed_ok":True},
    {"name":"Leadcore Rig","categories":["boden"],"max_cast":160,"boat_ok":True,"weed_ok":False},
    {"name":"Safety Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True},
    {"name":"Snowman Hair Rig","categories":["wafter"],"max_cast":130,"boat_ok":True,"weed_ok":True},
    {"name":"Multi-Hair Rig","categories":["boden","allround"],"max_cast":180,"boat_ok":True,"weed_ok":False},
    {"name":"Distance Pop-Up Rig","categories":["popup"],"max_cast":200,"boat_ok":True,"weed_ok":True},
]

# =========================
# USER INPUTS
# =========================
st.header("🌊 Gewässer & Umwelt")
gewaesser = st.selectbox("Gewässertyp", ["Teich", "See", "Fluss"],
                         help="Stehendes oder fließendes Gewässer beeinflusst die Rig-Wahl und Strömungsanforderungen.")

truebung = st.slider("Wassertrübung (0 = klar, 10 = trüb)", 0, 10, 3,
                     help="Trübes Wasser erfordert auffälligere Köder und Rigs.")

st.header("🎣 Ausbringung")
ausbringung = st.radio("Methode", ["Wurf", "Boot", "Futterboot"],
                       help="Wählen Sie, ob Sie den Köder werfen oder vom Boot aus auslegen möchten.")

wurf_vom_boot = None
if ausbringung == "Boot":
    wurf_vom_boot = st.radio("Vom Boot aus: auslegen oder Wurf?", ["Auslegen", "Wurf"],
                             help="Entscheidet, ob die Wurfweite relevant ist.")

# Wurfweite nur sichtbar, wenn Wurf oder Boot-Wurf
wurfweite = None
if ausbringung == "Wurf" or wurf_vom_boot == "Wurf":
    wurfweite = st.slider("Wurfweite (m)", 10, 200, 40,
                          help="Entscheidet, welche Rigs für die Entfernung geeignet sind.")

st.header("🏞️ Hindernisse & Pflanzen")
kraut = st.checkbox("Kraut vorhanden 🌿")
muscheln = st.checkbox("Muscheln / Steine vorhanden 🐚")
aeste = st.checkbox("Äste / Unterholz vorhanden 🌳")
andere_hindernisse = st.checkbox("Andere Hindernisse vorhanden ⚠️")

st.header("🌊 Strömung")
stromung = 0.0
if gewaesser == "Fluss":
    stromung = st.slider("Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1,
                         help="0 = kaum Strömung, 2 = starke Strömung. Beeinflusst Rig-Stabilität.")

st.header("🐟 Fisch & Umwelt")
jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"],
                          help="Saison beeinflusst die Aktivität und Köderwahl der Karpfen.")
temperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16,
                       help="Wassertemperatur beeinflusst Beißverhalten und Rig-Auswahl.")
aggro = st.slider("Aggressivität / Beißverhalten der Karpfen (1 = vorsichtig, 10 = aggressiv)", 1, 10, 5,
                  help="Je vorsichtiger die Fische, desto unauffälliger sollten Rig und Köder sein.")
fischgewicht = st.slider("Erwartetes Karpfengewicht (kg)", 5, 35, 15)
weissfisch = st.slider("Weißfisch-Anteil (%)", 0, 10, 4,
                       help="Hoher Weißfischanteil erfordert eventuell Köder, die Weißfische weniger anziehen.")

# =========================
# KÖDER
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
# SCORE-Funktion
# =========================
def score_rig(rig):
    score = 0
    name = rig["name"].lower()
    if "popup" in rig["categories"] and "pop-up" in koeder.lower(): score += 10
    if kraut and rig["weed_ok"]: score += 8
    if muscheln or aeste or andere_hindernisse:
        if name in ["chod rig", "helicopter rig"]: score += 7
    if stromung > 0.8 and "fluss" in rig["categories"]: score += 7
    if aggro <= 4 and name in ["chod rig", "wafter rig", "slip d rig"]: score += 6
    if aggro >= 7 and name in ["hair rig", "blowback rig", "kd rig"]: score += 6
    if "boden" in rig["categories"] and (kraut or muscheln or aeste or andere_hindernisse): score += 3
    if "allround" in rig["categories"]: score += 3
    return score

# =========================
# FILTER UND TOP-RIG
# =========================
def rig_empfehlung():
    scored = []
    for rig in RIGS:
        if wurfweite and wurfweite > rig["max_cast"]:
            continue
        if ausbringung != "Wurf" and not rig["boat_ok"]:
            continue
        if kraut and not rig["weed_ok"]:
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

        st.subheader("🪝 Empfohlenes Rig")
        rig = top_rigs[0]
        st.write(f"**{rig['name']}** ({', '.join(rig['categories'])})")
        vorfach = "15–18 cm, steif" if (wurfweite and wurfweite > 120) else "20–25 cm, weich"
        blei = "Distance Inline 110–130 g" if (wurfweite and wurfweite > 120) else "Inline 90–110 g"
        haken = "Größe 4 Wide Gape" if fischgewicht >= 25 else "Größe 6 Wide Gape"
        if aggro <= 4: haken += " – vorsichtig / kleiner"

        st.write(f"- Vorfach: {vorfach}")
        st.write(f"- Haken: {haken}")
        st.write(f"- Blei: {blei}")
        st.write(f"- Köder anbringen: {koeder}")

        # Optional zweites Rig
        if len(top_rigs) > 1:
            if st.checkbox("Optional: zweites Rig anzeigen"):
                rig2 = top_rigs[1]
                st.write(f"**{rig2['name']}** ({', '.join(rig2['categories'])})")
                vorfach2 = "15–18 cm, steif" if (wurfweite and wurfweite > 120) else "20–25 cm, weich"
                blei2 = "Distance Inline 110–130 g" if (wurfweite and wurfweite > 120) else "Inline 90–110 g"
                haken2 = "Größe 4 Wide Gape" if fischgewicht >= 25 else "Größe 6 Wide Gape"
                if aggro <= 4: haken2 += " – vorsichtig / kleiner"
                st.write(f"- Vorfach: {vorfach2}")
                st.write(f"- Haken: {haken2}")
                st.write(f"- Blei: {blei2}")
                st.write(f"- Köder anbringen: {koeder}")
