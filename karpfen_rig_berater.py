import streamlit as st
import datetime

# ==========================================
# 1. SETUP & MOBIL-OPTIMIERTES DESIGN
# ==========================================
st.set_page_config(page_title="Karpfen-Taktik Pro v6.0", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size: 1.8rem; color: #1b5e20; font-weight: bold; margin-bottom: 15px; text-align: center; }
    .hinweis-box { background-color: #e8f4fd; padding: 12px; border-radius: 10px; border-left: 5px solid #2196f3; margin-bottom: 20px; font-size: 0.9rem; }
    .section-header { background-color: #2e7d32; color: white; padding: 10px; border-radius: 8px; margin-top: 15px; margin-bottom: 10px; font-weight: bold; font-size: 1.1rem; text-align: center; }
    .taktik-detail { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border-left: 4px solid #2e7d32; margin-bottom: 10px; font-size: 0.95rem; line-height: 1.4; }
    .spot-empfehlung { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 2px dashed #4caf50; font-weight: 500; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">🎖️ Karpfen-Taktik Pro v6.0</div>', unsafe_allow_html=True)

# ==========================================
# 2. EINGABEMASKE: GEWÄSSER & UMWELT
# ==========================================
st.markdown('<div class="section-header">📍 1. Gewässer & Umwelt</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"], help="Bestimmt Montage und Strömungsgefahr.")
    stroemung = "Keine"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stroemung = st.select_slider("Strömungsstärke", options=["Keine", "Leicht", "Mittel", "Stark"], help="Beeinflusst Bleiform (Krallen).")
    tiefe_max = st.number_input("Maximale Gewässertiefe (m)", 1.0, 60.0, 8.0, help="Wichtig für Thermik (Sprungschicht).")
    tiefe_spot = st.number_input("Deine Spottiefe (m)", 0.5, 50.0, 3.5, help="Tiefe am Ablegeplatz.")
    angeltag = st.date_input("Wann fischst du?", datetime.date.today(), help="Berechnet Mondphase & Jahreszeit.")

with c2:
    # JAHRESZEIT AUTOMATIK
    m = angeltag.month
    if m in [3, 4, 5]: jz = "Frühjahr"
    elif m in [6, 7, 8]: jz = "Sommer"
    elif m in [9, 10, 11]: jz = "Herbst"
    else: jz = "Winter"
    st.write(f"**Erkannte Jahreszeit:** {jz}")
    
    temp = st.slider("Wassertemperatur (°C)", 0, 35, 15, help="Einfluss auf Stoffwechsel.")
    luftdruck = st.number_input("Luftdruck (hPa)", 950, 1050, 1013, help="1013 hPa ist Standard.")
    druck_tendenz = st.selectbox("Luftdruck-Tendenz", ["Stabil", "Fallend", "Steigend"], help="Fallend = Beißsignal.")

with c3:
    boden = st.selectbox("Bodenbeschaffenheit", ["-- Bitte wählen --", "Sand / Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Moder (faulig)", "Weiß ich nicht"], index=0)
    zeit = st.multiselect("Wann fischst du?", ["Vormittag", "Nachmittag", "Abend", "Nacht"], placeholder="-- Bitte wählen --")
    hindernisse = st.multiselect("Hindernisse", ["Muschelbänke", "Totholz", "Kraut", "Scharfe Kanten", "Krebse", "Keine Hindernisse"], placeholder="-- Bitte wählen --")
    weissfisch = st.select_slider("Weißfischvorkommen", options=["Niedrig", "Mittel", "Hoch", "Extrem"], value="Mittel")
    ausbringung = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    b_taktik = "Normal"; w_weite = 0
    if ausbringung == "Boot":
        b_taktik = st.selectbox("Boot-Vorgehen", ["Nur Ablegen", "Vom Boot auswerfen"])
    elif ausbringung == "Wurf vom Ufer":
        w_weite = st.slider("Wurfweite (m)", 0, 180, 60)
    
    ziel_kg = st.number_input("Max. Karpfengewicht (kg)", 5, 40, 15)
    aktivitaet = st.select_slider("Vorsicht (Fisch)", options=["Weiß ich nicht", "Apathisch", "Vorsichtig", "Normal", "Aggressiv"], value="Normal")

# ==========================================
# 3. EXPERTEN-LOGIK-ENGINE (VOLLSTÄNDIG)
# ==========================================
def berechne_pro_logic():
    s = {
        "blei_typ": "Safety-Clip Montage", "blei_form": "Birnenform (Smooth)", "blei_gew": 90,
        "rig_typ": "Standard Haar-Rig", "pres": "Bodenköder", "vorfach_mat": "Coated Braid", 
        "vorfach_len": "15-20 cm", "leader": "Leadcore / Tube", "h_typ": "Wide Gape",
        "h_spitze": "Straight Point", "h_oehr": "Gerade", "h_draht": "Standard", "h_gr": 6,
        "k_empf": "Standard 20mm Boilie", "k_h": "Normal", "k_gr": "20mm",
        "f_menge": "Moderat (ca. 1kg)", "f_art": "Mix aus Boilies & Pellets",
        "logik": {"montage": "", "haken": "", "futter": "", "umwelt": ""}
    }

    # MONTAGEN-LOGIK & BEGRÜNDUNG
    if boden in ["Schlamm (weich)", "Moder (faulig)"] or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe System"; s["rig_typ"] = "Helikopter-Rig"
        s["pres"] = "Pop-Up / Schneemann"; s["vorfach_len"] = "25-35 cm"
        s["logik"]["montage"] = "➔ **Weicher Boden/Kraut:** Das Heli-Rig verhindert, dass der Köder mit dem Blei einsinkt. Der Köder bleibt sauber obenauf liegen."
    else:
        s["logik"]["montage"] = "➔ **Harter Boden:** Die Safety-Clip Montage mit kurzem Vorfach liefert den direktesten Selbsthakeffekt, da der Fisch sofort auf das Bleigewicht trifft."

    # HAKEN-LOGIK & BEGRÜNDUNG
    if ziel_kg > 22: s["h_gr"] = 4; s["h_draht"] = "X-Strong"
    if s["pres"] != "Bodenköder": 
        s["h_typ"] = "Curve Shank"; s["h_oehr"] = "Nach innen gebogen"
        s["logik"]["haken"] = f"➔ **Mechanik:** Der Curve Shank Haken (Gr. {s['h_gr']}) dreht sich bei auftreibenden Ködern aggressiver ein und greift sicher in der Unterlippe."
    else:
        s["logik"]["haken"] = f"➔ **Mechanik:** Der Wide Gape Haken (Gr. {s['h_gr']}) ist der beste Allrounder für Bodenköder und bietet maximalen Halt im Drill."

    # FUTTER- & KÖDER-LOGIK
    if weissfisch in ["Hoch", "Extrem"] or "Krebse" in hindernisse:
        s["k_h"] = "Extra Hart / Gepökelt"; s["k_gr"] = "24mm / Doppel-20mm"; s["k_empf"] = "Harte Fisch-Boilies / Tigernüsse"
        s["logik"]["futter"] = "➔ **Selektion:** Wegen hohem Weißfisch-/Krebsdruck nutzen wir große, harte Köder, um Beifänge zu vermeiden und die Nacht durchzufischen."
    else:
        s["logik"]["futter"] = "➔ **Attraktion:** Bei normalem Druck ist ein 20mm Köder ideal, um schnell Akzeptanz am Platz zu finden."

    # UMWELT & LUFTDRUCK
    if druck_tendenz == "Fallend":
        s["f_menge"] = "Aggressiv (ca. 2-3kg)"
        s["logik"]["umwelt"] = "➔ **Luftdruck:** Fallender Druck aktiviert den Stoffwechsel. Die Fische suchen aktiv Nahrung – mehr Futter hält sie länger am Spot."
    elif luftdruck > 1025:
        s["f_menge"] = "Minimal (PVA / Single)"; s["k_empf"] = "Hochattraktiver Pop-Up"
        s["logik"]["umwelt"] = "➔ **Hochdruck:** Fische stehen oft träge im Mittelwasser. Ein einzelner, auffälliger Reizköder bringt hier oft den einzigen Biss."
    else:
        s["logik"]["umwelt"] = f"➔ **Saison:** Im {jz} suchen Fische aktiv nach Energie. Ein moderater Futterteppich ist die sicherste Wahl."

    # BOOT/WURF SPEZIAL
    if ausbringung == "Boot": s["blei_gew"] = 140 if b_taktik == "Nur Ablegen" else 110
    elif ausbringung == "Wurf vom Ufer" and w_weite > 100: s["blei_gew"] = 125; s["blei_form"] = "Zip/Distance"

    return s

ergebnis = berechne_pro_logic()

# ==========================================
# 4. AUSGABE: RESULTATE
# ==========================================
st.markdown("---")
st.markdown('<div class="section-header">🛡️ 2. Deine optimierte Taktik-Empfehlung</div>', unsafe_allow_html=True)
res_c1, res_c2, res_c3 = st.columns(3)

with res_c1:
    st.subheader("🎣 Montage")
    st.info(f"**System:** {ergebnis['blei_typ']}\n\n**Blei:** {ergebnis['blei_form']} ({ergebnis['blei_gew']}g)")
    st.markdown(f"<small>{ergebnis['logik']['montage']}</small>", unsafe_allow_html=True)

with res_c2:
    st.subheader("🧶 Rig & Vorfach")
    st.success(f"**Rig:** {ergebnis['rig_typ']}\n\n**Material:** {ergebnis['vorfach_mat']}\n\n**Länge:** {ergebnis['vorfach_len']}")
    st.markdown(f"<small>➔ **Tarnung:** {ergebnis['vorfach_mat']} wird gewählt, um {aktivitaet.lower()} Fische nicht zu verschrecken.</small>", unsafe_allow_html=True)

with res_c3:
    st.subheader("🪝 Haken-Setup")
    st.warning(f"**Modell:** {ergebnis['h_typ']} (Gr. {ergebnis['h_gr']})\n\n**Draht:** {ergebnis['h_draht']}\n\n**Spitze:** {ergebnis['h_spitze']}")
    st.markdown(f"<small>{ergebnis['logik']['haken']}</small>", unsafe_allow_html=True)

st.markdown('<div class="section-header">🍱 3. Köder- & Futterstrategie</div>', unsafe_allow_html=True)
k_c1, k_c2 = st.columns(2)
with k_c1:
    st.write(f"**Köder:** {ergebnis['k_empf']}\n\n**Größe:** {ergebnis['k_gr']} | **Härte:** {ergebnis['k_h']}")
    st.markdown(f"<small>{ergebnis['logik']['futter']}</small>", unsafe_allow_html=True)
with k_c2:
    st.write(f"**Futtermenge:** {ergebnis['f_menge']}\n\n**Futterart:** {ergebnis['f_art']}")
    st.markdown(f"<small>{ergebnis['logik']['umwelt']}</small>", unsafe_allow_html=True)

st.markdown('<div class="section-header">🔍 4. Spot-Analyse & Natur-Physik</div>', unsafe_allow_html=True)
sa1, sa2 = st.columns(2)
with sa1:
    z_str = ", ".join(zeit) if zeit else "--"
    st.markdown(f'<div class="spot-empfehlung">Tiefe: {tiefe_spot}m | Max: {tiefe_max}m | Zeit: {z_str}</div>', unsafe_allow_html=True)
    if luftdruck > 1022: st.warning("⚖️ **ZIG-Rig Tipp:** Hoher Druck! Fische stehen evtl. im Mittelwasser.")
with sa2:
    if jz == "Winter": st.write(f"📍 Suche tiefste Löcher (ca. {tiefe_max}m).")
    elif "Nacht" in zeit: st.write("📍 Nacht-Tipp: Eine Rute extrem flach (0.5 - 1.5m) ablegen.")
    else: st.write("📍 Suche markante Kanten oder Muschelbänke.")
    if ausbringung == "Boot": st.write("➔ **Profi-Tipp:** Nutze Backleads zum Absenken der Schnur.")

def get_moon(d):
    diff = d - datetime.date(2001, 1, 1); lun = 29.530588853; pos = (diff.days / lun) % 1
    if pos < 0.06: return "🌑 Neumond", "Dunkelheit: Fische ziehen oft furchtlos flach."
    if 0.45 < pos < 0.55: return "🌕 Vollmond", "Vorsicht: Schnurschatten & Silhouette sichtbar!"
    return "🌓 Sichel/Halbmond", "Solide Bedingungen."

mond_n, mond_t = get_moon(angeltag)
st.markdown(f'<div class="taktik-detail">🌙 **Mondphase ({angeltag.strftime("%d.%m.%Y")}):** {mond_n} - {mond_t}</div>', unsafe_allow_html=True)

if boden == "-- Bitte wählen --" or not zeit:
    st.warning("⚠️ Bitte wähle noch Boden und Zeitfenster für eine präzisere Analyse.")
