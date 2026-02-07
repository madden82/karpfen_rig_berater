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
# Rig-Datenbank 50+ Rigs
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
    {"name":"Top Pop Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True},
    {"name":"Distance Pop-Up Rig","categories":["popup"],"max_cast":200,"boat_ok":True,"weed_ok":True},
    {"name":"Helicopter Distance Rig","categories":["boden","kraut"],"max_cast":200,"boat_ok":True,"weed_ok":True},
]

# =========================
# USER INPUTS
# =========================
st.header("🌊 Gewässer & Umwelt")
gewaesser = st.selectbox("Gewässertyp", ["Teich", "See", "Fluss"])
truebung = st.slider("Wassertrübung (0 = klar, 10 = trüb)", 0, 10, 3)
ausbringung = st.radio("Ausbringungsart", ["Wurf", "Boot", "Futterboot"])
wurfweite = st.slider("Wurfweite (m)", 10, 200, 40)

st.header("🏞️ Hindernisse & Pflanzen")
kraut = st.checkbox("Kraut/Hindernisse vorhanden 🌿")
stromung = 0.0
if gewaesser=="Fluss":
    stromung = st.slider("Fließgeschwindigkeit (m/s)", 0.0, 2.0, 0.5, 0.1)

st.header("🐟 Fisch & Umwelt")
jahreszeit = st.selectbox("Jahreszeit", ["Frühling", "Sommer", "Herbst", "Winter"])
temperatur = st.slider("Wassertemperatur (°C)", 4, 30, 16)
aggro = st.slider("Aggressivität/Beißverhalten der Karpfen",1,10,5)
fischgewicht = st.slider("Erwartetes Karpfengewicht (kg)",5,35,15)
weissfisch = st.slider("Weißfisch-Anteil (%)",0,10,4)

# =========================
# KÖDER
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

koeder, koeder_mm, koeder_text = koeder_empfehlung()

# =========================
# SCORE-Funktion
# =========================
def score_rig(rig):
    score = 0
    name = rig["name"].lower()
    if "popup" in rig["categories"] and "pop-up" in koeder.lower(): score+=10
    if kraut and rig["weed_ok"]: score+=8
    if stromung>0.8 and "fluss" in rig["categories"]: score+=7
    if aggro<=4 and name in ["chod rig","wafter rig","slip d rig"]: score+=6
    if aggro>=7 and name in ["hair rig","blowback rig","kd rig"]: score+=6
    if "boden" in rig["categories"] and kraut: score+=3
    if "allround" in rig["categories"]: score+=3
    return score

# =========================
# FILTER UND TOP-RIGS
# =========================
def rig_empfehlung():
    scored = []
    for rig in RIGS:
        if wurfweite>rig["max_cast"]: continue
        if ausbringung!="Wurf" and not rig["boat_ok"]: continue
        if kraut and not rig["weed_ok"]: continue
        scored.append( (score_rig(rig), rig) )
    scored.sort(key=lambda x:x[0], reverse=True)
    return [r for s,r in scored[:7]]  # Top 7

# =========================
# AUSGABE
# =========================
if st.button("🎣 Empfehlung anzeigen"):
    top_rigs = rig_empfehlung()
    st.success("✅ Deine persönliche Empfehlung")

    st.subheader("🍡 Köder")
    st.write(f"{koeder} – {koeder_mm} mm")
    st.caption(koeder_text)

    st.subheader("🪝 Empfohlene Rigs")
    for rig in top_rigs:
        st.write(f"**{rig['name']}** ({', '.join(rig['categories'])})")
        vorfach = "15–18 cm, steif" if wurfweite>120 else "20–25 cm, weich"
        blei = "Distance Inline 110–130 g" if wurfweite>120 else "Inline 90–110 g"
        haken = "Größe 4 Wide Gape" if fischgewicht>=25 else "Größe 6 Wide Gape"
        if aggro<=4: haken+=" – vorsichtig / kleiner"

        st.write(f"- Vorfach: {vorfach}")
        st.write(f"- Haken: {haken}")
        st.write(f"- Blei: {blei}")
        st.write(f"- Köder anbringen: {koeder}")
        st.caption("Schritt-für-Schritt mit Bildern")
        # Platzhalterbilder, bitte durch echte URLs ersetzen
        st.image("https://www.handlteich.at/wp-content/uploads/vorfach.jpg", caption="Vorfach zuschneiden")
        st.image("https://www.handlteich.at/wp-content/uploads/haken.jpg", caption="Haken anbinden")
        st.image("https://www.handlteich.at/wp-content/uploads/knoten.jpg", caption="Knoten binden")
        st.image("https://www.handlteich.at/wp-content/uploads/blei.jpg", caption="Blei befestigen")
        st.image("https://www.handlteich.at/wp-content/uploads/koeder.jpg", caption="Köder aufziehen")
