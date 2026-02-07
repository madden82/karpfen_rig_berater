import streamlit as st

# =========================
# Setup & Theme
# =========================
st.set_page_config(page_title="Carp Tactical Intelligence Pro", layout="wide")

st.title("🎖️ Carp Tactical Intelligence Pro")
st.caption("Einsatzplanung v3.1 | Fixed Logic & Futter-Modul")

# ==========================================
# 1. PHASE: GEWÄSSER-PROFIL
# ==========================================
st.header("📍 Schritt 1: Gewässer- & Umweltprofil")
c1, c2, c3 = st.columns(3)

with c1:
    gewaesser_typ = st.selectbox("Gewässertyp", 
                                ["See / Weiher", "Baggersee", "Kanal", "Fluss", "Strom", "Stausee"])
    tiefe = st.number_input("Exakte Tiefe am Spot (m)", 0.5, 40.0, 4.0)
    
    stromung = "Keiner"
    if gewaesser_typ in ["Kanal", "Fluss", "Strom"]:
        stromung = st.select_slider("Strömungsdruck", options=["Keiner", "Leicht", "Mittel", "Stark"])

with c2:
    boden_struktur = st.selectbox("Bodenbeschaffenheit", 
                                 ["Sand/Kies (hart)", "Lehm (fest)", "Schlamm (weich)", "Modder (faulig)", "Kraut/Algen"])
    hindernisse = st.multiselect("Hindernisse am Spot", ["Muschelbänke", "Totholz/Äste", "Scharfe Kanten"])

with c3:
    st.markdown("**Atmosphäre & Wasserqualität**")
    wasser_klarheit = st.select_slider("Sichttiefe / Klarheit", options=["Trüb", "Medium", "Klar", "Gin-Clear"])
    windstärke = st.select_slider("Windstärke", options=["Windstill", "Leichte Brise", "Mäßiger Wind", "Starker Wind"])
    temp = st.slider("Wassertemperatur (°C)", 2, 30, 15)

# ==========================================
# 2. PHASE: TAKTIK & AUSBRINGUNG
# ==========================================
st.header("🎯 Schritt 2: Taktik & Ausbringung")
t1, t2 = st.columns(2)

# Initialisierung der Variablen zur Vermeidung von NameErrors
wurfweite = 0
taktik_typ = "Ablegen"

with t1:
    ausbringungs_methode = st.radio("Ausbringung", ["Wurf vom Ufer", "Futterboot", "Boot"], horizontal=True)
    
    if ausbringungs_methode == "Boot":
        boot_taktik = st.radio("Taktik vom Boot:", ["Vom Boot ablegen", "Vom Boot werfen"], horizontal=True)
        if boot_taktik == "Vom Boot werfen":
            taktik_typ = "Wurf"
            wurfweite = st.slider("Wurfweite (m)", 5, 100, 30)
    elif ausbringungs_methode == "Wurf vom Ufer":
        taktik_typ = "Wurf"
        wurfweite = st.slider("Wurfweite (m)", 10, 180, 70)

with t2:
    ziel_gewicht = st.number_input("Erwartetes Gewicht (kg)", 5, 40, 15)
    fisch_aktivitaet = st.select_slider("Fisch-Aktivität", options=["Apathisch", "Vorsichtig", "Normal", "Aggressiv"])
    koeder_typ = st.selectbox("Geplanter Köder", ["Bodenköder / Boilie", "Wafter (ausbalanciert)", "Pop-Up (schwimmend)", "Zigs (Schaumstoff)"])

# ==========================================
# 3. PHASE: DIE ERWEITERTE RIG-ENGINE
# ==========================================

def get_advanced_setup(t_typ, w_weite, f_aktiv):
    setup = {
        "rig": "Hair Rig",
        "hook_range": "4 - 6",
        "lead_w": 95,
        "lead_sys": "Safety Clip",
        "optimum": "Coated Braid (25lb)",
        "braid_alt": "Soft Braid (20lb) + Anti Tangle Sleeve",
        "length": 18,
        "desc": "Klassische Allround-Präsentation."
    }

    if koeder_typ == "Zigs (Schaumstoff)":
        setup["rig"] = "Zig Rig"
        setup["optimum"] = "Monofilament (0.28mm - 0.30mm)"
        setup["braid_alt"] = "Nicht empfohlen für Zigs!"
        setup["length"] = int(tiefe * 0.75 * 100)
        setup["lead_sys"] = "Blei-Freigabe-System (Adjustable)"
        setup["desc"] = "Präsentation im Mittelwasser."
        return setup

    if koeder_typ == "Pop-Up (schwimmend)":
        if boden_struktur in ["Sand/Kies (hart)", "Lehm (fest)"]:
            setup["rig"] = "Ronnie Rig"
            setup["optimum"] = "Stiff Mono / Boom (0.50mm)"
            setup["braid_alt"] = "Stiff Coated Braid (35lb)"
        else:
            setup["rig"] = "Chod Rig"
            setup["optimum"] = "Rigid Mouthtrap (0.50mm)"
            setup["length"] = 6
            setup["lead_sys"] = "Helicopter (Naked)"

    elif koeder_typ == "Wafter (ausbalanciert)":
        setup["rig"] = "German Rig"
        if wasser_klarheit in ["Klar", "Gin-Clear"]:
            setup["rig"] = "Slip-D Rig"
            setup["optimum"] = "Fluorocarbon (0.40mm)"

    # Blei Logik
    if t_typ == "Wurf":
        setup["lead_w"] = 115 if w_weite > 90 else 85
        if w_weite > 115: setup["lead_sys"] = "Helicopter"
    
    if stromung == "Stark":
        setup["lead_w"] = 220
        setup["lead_sys"] = "Grippa-Inliner"

    return setup

# Aufruf der Engine mit Übergabe der UI-Variablen
res = get_advanced_setup(taktik_typ, wurfweite, fisch_aktivitaet)

# ==========================================
# 4. PHASE: FUTTER-STRATEGIE (Neu)
# ==========================================
def get_feeding_strategy():
    amount = 0.5 # kg pro Tag Basis
    if temp > 15: amount += 1.5
    if temp > 20: amount += 2.0
    if fisch_aktivitaet == "Aggressiv": amount *= 2
    if fisch_aktivitaet == "Apathisch": amount *= 0.2
    
    art = "Partikel & kleine Pellets" if temp < 12 else "Boilies & große Pellets"
    return round(amount, 1), art

f_menge, f_art = get_feeding_strategy()

# ==========================================
# 5. PHASE: OUTPUT
# ==========================================
st.divider()
st.header("🏁 Dein Taktisches Setup")

c_out1, c_out2, c_out3 = st.columns(3)

with c_out1:
    st.subheader("📦 Hardware")
    st.metric("Blei", f"{res['lead_w']} g")
    st.write(f"**Montage:** {res['lead_sys']}")
    st.write(f"**Haken-Range:** Gr. {res['hook_range']}")

with c_out2:
    st.subheader("🪝 Rig & Material")
    st.success(f"**Architektur:** {res['rig']}")
    st.write(f"**Optimum:** {res['optimum']}")
    st.info(f"**Alternative:** {res['braid_alt']}")
    st.write(f"**Länge:** {res['length']} cm")

with c_out3:
    st.subheader("🥣 Futter-Strategie")
    st.metric("Menge ca.", f"{f_menge} kg / Tag")
    st.write(f"**Hauptfutter:** {f_art}")
    st.caption("Basierend auf Temp. & Aktivität")

st.divider()
with st.expander("🛠️ Bauanleitung anzeigen"):
    st.write(f"1. Nutze {res['optimum']} in {res['length']}cm Länge.")
    st.write(f"2. Binde Haken Gr. {res['hook_range']} mit Knotless-Knot.")
    st.write(f"3. Montage am {res['lead_sys']}-System.")
