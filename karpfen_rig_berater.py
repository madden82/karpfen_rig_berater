import streamlit as st

# ==========================================
# KONFIGURATION
# ==========================================
st.set_page_config(page_title="Karpfen-Rig Kalkulator", layout="centered")

st.title("Karpfen-Rig Kalkulator")

# ==========================================
# 1️⃣ EINGABEN (DEIN ORIGINALER ABLAUF)
# ==========================================
st.header("1️⃣ Gewässer und Strömung")
gewässertyp = st.radio(
    "Gewässertyp:",
    ("Keine Strömung (Seen, Teiche, Weiher, Baggerseen, Lagunen)",
     "Strömung vorhanden (Flüsse, Kanäle, Stauseen, Altarme, Mündungsbereiche)")
)

if "Keine Strömung" in gewässertyp:
    strom = "keine"
    strom_m_s = 0.0
else:
    strom_stufe = st.select_slider("Strömungsgeschwindigkeit:", options=["leicht", "mittel", "stark"])
    strom = strom_stufe
    strom_m_s = {"leicht": 0.2, "mittel": 0.6, "stark": 1.4}[strom]

st.header("2️⃣ Angeltechnik & Wurfweite")
angeltechnik = st.radio("Angeltechnik:", ("Wurf vom Ufer aus", "Boot: Wurf von Boot aus", "Boot: Ablage von Boot aus", "Futterboot"))
wurfweite = st.slider("Wurfweite (m):", 0, 200, 50) if "Wurf" in angeltechnik else 0

st.header("3️⃣ Bodenbeschaffenheit")
boden = st.radio("Bodenart:", ("weich", "mittel", "hart"))

st.header("4️⃣ Maximal erwartetes Karpfengewicht")
gewicht = st.slider("Gewicht (kg):", 1, 40, 10)

st.header("5️⃣ Verhalten der Karpfen")
fischverhalten = st.radio("Karpfenverhalten:", ("Aktive Fresser", "Scheue Karpfen", "Beide Typen / weiß nicht genau"))

st.header("6️⃣ Hindernisse am Spot")
hindernisse = st.radio("Sind Hindernisse vorhanden?", ("Ja", "Nein", "Weiß ich nicht"))

st.header("7️⃣ Wasserqualität")
wasserqualitaet = st.radio("Wasserqualität:", ("klar", "leicht trüb", "trüb"))

st.header("8️⃣ Störtiere")
störtiere = st.multiselect("Welche Störtiere sind vorhanden?", ["Viele Weißfische", "Krebse", "Wollhandkrabben", "Keine oder wenige"])

st.header("9️⃣ Jahreszeit und Wassertemperatur")
season = st.selectbox("Jahreszeit:", ["Frühling", "Sommer", "Herbst", "Winter"])
temperature = st.slider("Wassertemperatur (°C):", 0, 35, 15)

st.markdown("---")

# ==========================================
# 2️⃣ BERECHNUNGSLOGIK
# ==========================================
basis_blei_map = {1: 12, 3: 25, 5: 35, 10: 50, 15: 60, 20: 70, 25: 80, 30: 90, 35: 100, 40: 110}
basis = min([v for k, v in basis_blei_map.items() if gewicht <= k] or [110])
gewicht_effektiv = round(basis * {"weich": 0.9, "mittel": 1.0, "hart": 1.1}[boden] * {"keine": 1.0, "leicht": 1.05, "mittel": 1.10, "stark": 1.20}[strom], 1)

vorfach_tabelle = {"hart": (10, 20), "mittel": (15, 30), "weich": (25, 50)}
min_v, max_v = vorfach_tabelle[boden]
vorfach_l = max_v if fischverhalten != "Aktive Fresser" else (min_v + max_v) // 2

rigs = {
    "Line-Aligner": {"boden": ["hart", "mittel"], "v": ["Aktive Fresser", "Beide Typen / weiß nicht genau"], "w": 120, "s": 0.85, "desc": "Aggressives Eindrehen des Hakens durch Verlängerung des Schenkels."},
    "Snowman": {"boden": ["hart", "mittel", "weich"], "v": ["Aktive Fresser", "Beide Typen / weiß nicht genau"], "w": 100, "s": 1.22, "desc": "Perfekte optische Täuschung und kritisches Balancieren des Hakengewichts."},
    "D-Rig": {"boden": ["hart"], "v": ["Scheue Karpfen", "Beide Typen / weiß nicht genau"], "w": 150, "s": 0.6, "desc": "Maximale Bewegungsfreiheit des Köders auf dem D-Loop, extrem schwer auszuspucken."},
    "KD-Rig": {"boden": ["hart", "mittel", "weich"], "v": ["Aktive Fresser", "Scheue Karpfen", "Beide Typen / weiß nicht genau"], "w": 120, "s": 1.05, "desc": "Der Haken hängt durch den speziellen Haaraustritt extrem kopflastig."},
    "Helikopter": {"boden": ["weich", "mittel", "hart"], "v": ["Aktive Fresser", "Scheue Karpfen", "Beide Typen / weiß nicht genau"], "w": 200, "s": 2.0, "desc": "Ultimative Präsentation auf Schlamm und für maximale Distanzwürfe."}
}
passende = [r for r, i in rigs.items() if boden in i["boden"] and fischverhalten in i["v"] and wurfweite <= i["w"] and strom_m_s <= i["s"]]

# ==========================================
# 3️⃣ AUSGABE & UMFASSENDE STRATEGISCHE INFOS
# ==========================================
st.header("🏁 Analyse & Strategie-Bericht")

st.subheader("⚙️ Setup-Konfiguration")
st.write(f"**Berechnetes Bleigewicht:** {gewicht_effektiv} g")
st.write(f"**Vorfachlänge:** {vorfach_l} cm")
st.info("So kurz als möglich, so lang als nötig!")

st.subheader("🎣 Rig-Empfehlungen")
if passende:
    for p in passende[:2]:
        st.success(f"✅ **{p}**: {rigs[p]['desc']}")
else:
    st.warning("Kein spezielles Rig unter diesen Bedingungen – nutze ein Standard-Helikopter-System.")

st.markdown("---")
st.header("🎯 Tiefgehende Taktik-Analyse für die richtige Spotwahl")

# --- BODEN & STRUKTUR ---
st.write("### 🏗️ Bodenbeschaffenheit & Präsentation")
if boden == "weich":
    st.write(f"- **Detaillierte Analyse:** Da du auf **weichem Boden** angelst, besteht die Gefahr, dass dein {gewicht_effektiv}g Blei im Schlamm versinkt und das Vorfach mitzieht. Nutze zwingend ein Helikopter-System, bei dem du den oberen Stopper weit nach oben schiebst (ca. 2x Schlammtiefe).")
    st.write("- **Köder-Taktik:** Vermeide schwere Sink-Boilies. Nutze 'Wafter' oder Pop-Ups, die das Gewicht des Hakens aufheben. Im weichen Schlamm fressen Karpfen oft durch 'Filtern'. Kleine Partikel wie Hanf und Weizen halten die Fische länger am Platz, ohne sie zu sättigen.")
elif boden == "hart":
    st.write("- **Detaillierte Analyse:** Auf **hartem Grund** (Kies/Lehm) nehmen Fische den Köder oft sehr aggressiv auf. Kurze Vorfächer ({vorfach_l}cm) sorgen hier für einen sofortigen Hakeffekt durch das Bleigewicht.")
    st.write("- **Spot-Tipp:** Suche nach harten Kanten oder Plateaus. Hier ziehen die Fische entlang. Nutze schwere Inline-Bleie für den besten Selbsthakeffekt, da der Widerstand sofort übertragen wird.")
else:
    st.write("- **Detaillierte Analyse:** **Mittlerer Boden** (Sand/dünner Schlamm) erlaubt fast alle Rig-Typen. Achte darauf, ob das Blei beim Einholen Widerstand zeigt oder leicht rutscht.")

# --- WASSER & TEMPERATUR ---
st.write(f"### 🌡️ Umweltfaktoren & Thermik ({season})")
if temperature <= 10:
    st.write(f"- **Winter/Kaltwasser-Strategie:** Bei {temperature}°C ist der Stoffwechsel der Karpfen auf ein Minimum reduziert. Die Fische bewegen sich kaum. Du musst den Köder zum Fisch bringen, nicht umgekehrt.")
    st.write("- **Spotwahl:** Suche die tiefsten Bereiche des Gewässers oder Plätze mit Totholz, die Restwärme speichern. Südhanglagen, die tagsüber Sonne abbekommen, sind ebenfalls Top-Spots.")
    st.write("- **Futter:** Nutze hochattraktive, wasserlösliche Lockstoffe (Alkohollöslich). Wenig Öl verwenden, da dieses bei Kälte stockt.")
elif temperature >= 20:
    st.write(f"- **Sommer-Strategie:** Bei {temperature}°C herrscht oft Sauerstoffmangel in tiefen Schichten. Die Fische stehen flacher oder im Freiwasser (Zigs!).")
    st.write("- **Spotwahl:** Windzugewandte Ufer (auflandiger Wind) bringen Sauerstoff und Nahrung. Einläufe oder sauerstoffreiches Kraut sind jetzt Magneten.")

# --- STRÖMUNG ---
if strom != "keine":
    st.write(f"### 🌊 Strömungsmanagement ({strom})")
    st.write(f"- **Taktik:** In der **{strom}en Strömung** musst du den Strömungsdruck auf die Schnur minimieren. Nutze 'Backleads' (Absenkbleie), um die Schnur am Boden zu halten.")
    st.write("- **Futter-Strategie:** Füttere in einer langgezogenen Spur stromaufwärts. Die Fische folgen der Duftspur gegen die Strömung bis zu deinem Spot. Nutze schwere, grobe Partikel wie Tigernüsse oder Pellets, die nicht sofort weggespült werden.")

# --- FISCHVERHALTEN & SICHT ---
st.write("### 👁️ Fischpsychologie & Sicht")
if wasserqualitaet == "klar":
    st.write("- **Tarnung:** In **klarem Wasser** sehen Karpfen alles. Nutze Fluorocarbon-Vorfächer und bleifreie Leader, die sich unsichtbar an den Boden schmiegen. Vermeide glänzende Bleie.")
if fischverhalten == "Scheue Karpfen":
    st.write("- **Strategie:** Misstrauische Fische meiden Futterberge. Nutze die 'Single Hookbait' Taktik oder nur ganz wenig Beifutter (PVA-Stick). Weniger ist hier oft mehr.")

# --- STÖRTIERE & HINDERNISSE ---
if "Krebse" in störtiere or "Wollhandkrabben" in störtiere:
    st.write("### 🦀 Störtier-Abwehr")
    st.warning("- **Achtung:** Krebse zerlegen normale Boilies in kurzer Zeit. Nutze 'Hard-Baits' (extremer getrocknet) oder Tigernüsse. Schütze den Köder mit 'Shrink Tube' (Schrumpfschlauch) oder nutze künstliche Plastikköder als Stopper.")
if hindernisse == "Ja":
    st.write("### 🪵 Hindernis-Taktik")
    st.error("- **Sicherheit:** In der Nähe von Hindernissen gibt es keine Kompromisse. Nutze eine Schlagschnur von mindestens 0.50mm - 0.60mm Durchmesser. Die Ruten müssen gesichert sein (Snag Ears), damit sie beim Run nicht ins Wasser gerissen werden. Nutze Safety-Clips, damit das Blei bei einem Hänger sofort auslöst.")

st.markdown("---")
st.success("Diese Analyse basiert auf deinen individuellen Daten. Viel Erfolg beim Ansitz und Petri Heil!")
