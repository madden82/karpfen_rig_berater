# ==============================
# KARPEN-RIG BERATER – Profi Version
# ==============================

# ------------------------------
# RIG-DATENBANK (~50+ Rigs)
# ------------------------------
RIGS = [
    {"name":"Hair Rig","categories":["boden","allround"],"max_cast":200,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Blowback Rig","categories":["boden","allround"],"max_cast":160,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"KD Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":False},
    {"name":"German Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":False,"river_ok":False},
    {"name":"Ronnie Rig","categories":["popup"],"max_cast":130,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Spinner Rig","categories":["popup"],"max_cast":150,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Hinged Stiff Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Combi Rig","categories":["boden","wafter"],"max_cast":170,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"River Rig","categories":["boden","fluss"],"max_cast":100,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Wafter Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":True},
    {"name":"Slip D Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Hinged Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Naked Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Helicopter Rig","categories":["boden","kraut"],"max_cast":140,"boat_ok":True,"weed_ok":True,"river_ok":True},
    {"name":"Multi Rig","categories":["boden","wafter"],"max_cast":160,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Stiff D-Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Distance Hair Rig","categories":["boden"],"max_cast":200,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Long Casting KD Rig","categories":["boden"],"max_cast":180,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Snowman Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":True},
    {"name":"Chod-X Rig","categories":["popup","kraut"],"max_cast":130,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Anti-Tangle Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Teflon Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Method Feeder Rig","categories":["boden"],"max_cast":150,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Bolt Rig","categories":["fluss","popup"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Linguine Rig","categories":["fluss"],"max_cast":130,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Beehive Rig","categories":["boden","kraut"],"max_cast":130,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Helicopter Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Surface Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Zig Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":False},
    {"name":"Offset Rig","categories":["boden"],"max_cast":150,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Line-Aligner Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Teller Rig","categories":["boden"],"max_cast":140,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"KD Mini Rig","categories":["boden"],"max_cast":120,"boat_ok":True,"weed_ok":False,"river_ok":False},
    {"name":"Mini Chod Rig","categories":["popup","kraut"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Pop-Up Chod Rig","categories":["popup","kraut"],"max_cast":130,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Anti-Weed Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Floating Wafter Rig","categories":["wafter"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Heavy Distance Rig","categories":["boden"],"max_cast":200,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Fluoro Rig","categories":["boden"],"max_cast":160,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Stiff Pop Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Long Chod Rig","categories":["popup","kraut"],"max_cast":150,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Leadcore Rig","categories":["boden"],"max_cast":160,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Safety Rig","categories":["popup"],"max_cast":120,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Snowman Hair Rig","categories":["wafter"],"max_cast":130,"boat_ok":True,"weed_ok":True,"river_ok":True},
    {"name":"Multi-Hair Rig","categories":["boden","allround"],"max_cast":180,"boat_ok":True,"weed_ok":False,"river_ok":True},
    {"name":"Top Pop Rig","categories":["popup"],"max_cast":140,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Distance Pop-Up Rig","categories":["popup"],"max_cast":200,"boat_ok":True,"weed_ok":True,"river_ok":False},
    {"name":"Helicopter Distance Rig","categories":["boden","kraut"],"max_cast":200,"boat_ok":True,"weed_ok":True,"river_ok":True},
]


# ------------------------------
# EINGABEN
# ------------------------------
def ask_required(prompt, options):
    while True:
        print(prompt)
        for i,opt in enumerate(options,1):
            print(f"{i}: {opt}")
        choice = input("> ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice)-1]
        print("Ungültige Eingabe.\n")

def ask_optional(prompt, default=None):
    val = input(prompt + f" (leer = {default}): ")
    return val if val else default

print("\n🎣 KARPEN-RIG BERATER – Profi Version\n")

gewaesser = ask_required("Gewässertyp wählen:", ["Teich","See","Fluss"])
truebung = ask_required("Wassertrübung wählen:", ["klar","mittel","trüb"])
ausbringung = ask_required("Ausbringungsart:", ["Wurf","Boot","Futterboot"])
wurfweite = int(input("Wurfweite in Metern: "))
kraut = ask_optional("Kraut/Hindernisse vorhanden? ja/nein","unbekannt")
stromung = float(ask_optional("Fließgeschwindigkeit (m/s, leer=0)","0"))
jahreszeit = ask_required("Jahreszeit:", ["Frühling","Sommer","Herbst","Winter"])
temperatur = float(input("Wassertemperatur °C: "))
aggro = int(ask_optional("Aggressivität/Beißverhalten Karpfen (1–10)","5"))
fischgewicht = float(ask_optional("Erwartetes Karpfengewicht (kg)","15"))
weissfisch = float(ask_optional("Weißfischanteil %","4"))

# ------------------------------
# KÖDER-Empfehlung
# ------------------------------
def koeder_empfehlung():
    if temperatur < 10 or jahreszeit=="Winter":
        return "Pop-Up", 14, "Kaltwasser & Winter – auffällig"
    if weissfisch >= 6:
        return "Harter Boilie", 22, "Schützt vor Weißfisch"
    if aggro <= 4:
        return "Wafter", 18, "Vorsichtige Fische – unauffällig"
    if truebung=="trüb":
        return "Leuchtender Pop-Up",16,"Trübes Wasser – auffällig"
    return "Boilie",20,"Standardköder – bewährt"

koeder, koeder_mm, koeder_text = koeder_empfehlung()

# ------------------------------
# SCORE-Funktion für Rigs
# ------------------------------
def score_rig(rig):
    score = 0
    name = rig["name"].lower()

    # Pop-Up-Köder
    if "pop-up" in koeder.lower() and "popup" in rig["categories"]:
        score += 10

    # Kraut
    if kraut=="ja" and rig["weed_ok"]:
        score += 8

    # Strömung
    if stromung > 0.8 and rig["river_ok"]:
        score += 7

    # Vorsichtige Fische
    if aggro <= 4 and name in ["chod rig","wafter rig","slip d rig"]:
        score += 6

    # Aggressive Fische
    if aggro >= 7 and name in ["hair rig","blowback rig","kd rig"]:
        score += 6

    # Boden weich / Kraut
    if "boden" in rig["categories"] and kraut=="ja":
        score += 3

    # Allrounder
    if "allround" in rig["categories"]:
        score += 3

    return score

# ------------------------------
# FILTER & TOP-RIGS
# ------------------------------
def rig_empfehlung():
    scored = []
    for rig in RIGS:
        # harte Filter
        if wurfweite > rig["max_cast"]:
            continue
        if ausbringung!="Wurf" and not rig["boat_ok"]:
            continue
        if gewaesser=="Fluss" and not rig["river_ok"]:
            continue
        if kraut=="ja" and not rig["weed_ok"]:
            continue
        scored.append( (score_rig(rig), rig) )
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for s,r in scored[:7]]  # Top 7 Rigs

top_rigs = rig_empfehlung()

# ------------------------------
# AUSGABE
# ------------------------------
print("\n✅ Deine persönliche Rig-Empfehlung:\n")
print("Köder:", koeder, f"({koeder_mm} mm)")
print("Hinweis:", koeder_text)
print("\nGeeignete Rigs:")
for i,rig in enumerate(top_rigs,1):
    print(f"{i}: {rig['name']}")

# ------------------------------
# BAUPLAN-GENERATOR (mit Bilder-Links)
# ------------------------------
def rig_bauplan(rig):
    print("\n📋 BAUPLAN:", rig["name"])
    print("-"*40)

    # Vorfach
    if wurfweite>120:
        vorfach="15–18 cm, steif"
        blei="Distance Inline 110–130 g"
    else:
        vorfach="20–25 cm, weich"
        blei="Inline / Safety Clip 90–110 g"

    # Haken
    if fischgewicht >=25:
        haken="Größe 4 Wide Gape"
    else:
        haken="Größe 6 Wide Gape"
    if aggro<=4:
        haken += " – vorsichtig / kleiner"

    # Schritt-für-Schritt
    schritte = [
        f"1. Vorfach zuschneiden ({vorfach}) – [Bild](https://example.com/vorfach.jpg)",
        f"2. Haken anbinden ({haken}) – [Bild](https://example.com/haken.jpg)",
        "3. Knoten: Knotenloser Knoten / Achterknoten – [Bild](https://example.com/knoten.jpg)",
        f"4. Blei befestigen ({blei}) – [Bild](https://example.com/blei.jpg)",
        f"5. Köder anbringen ({koeder}) – [Bild](https://example.com/koeder.jpg)",
        "6. Rig testen im Wasser – [Bild](https://example.com/test.jpg)"
    ]
    for s in schritte:
        print(s)

# ------------------------------
# BAUPLAN FÜR AUSGEWÄHLTES RIG
# ------------------------------
if top_rigs:
    rig_auswahl = ask_required("\nWähle ein Rig für detaillierten Bauplan:", [r["name"] for r in top_rigs])
    rig_obj = next(r for r in top_rigs if r["name"]==rig_auswahl)
    rig_bauplan(rig_obj)

print("\n🎯 Ende des Profi-Rig-Beraters\n")
