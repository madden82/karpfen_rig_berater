def berechne_taktik():
    s = {
        "blei_form": "Birne",
        "blei_gew": 85,
        "blei_typ": "Safety-Clip",
        "vorfach_mat": "Coated Braid",
        "vorfach_len": 20,
        "h_typ": "Wide Gape",
        "h_farbe": "Dunkel",
        "h_gr": 6,
        "koeder": "Bodenköder",
        "koeder_gr": 20,
        "koeder_h": "Normal",
        "futter": 1.0,
        "begruendungen": []
    }

    score = 50

    # -------------------
    # STRÖMUNG & BLEI
    # -------------------
    if stroemung == "Stark" or gewaesser_typ == "Strom":
        s["blei_form"], s["blei_gew"] = "Grippa", 180
        score += 5
    elif stroemung == "Mittel":
        s["blei_form"], s["blei_gew"] = "Sargblei", 130

    if ausbringung == "Wurf" and wurfweite > 90:
        s["blei_form"] = "Zip-Blei"
        score += 3

    # -------------------
    # TIEFE
    # -------------------
    if tiefe_spot > 10:
        s["blei_gew"] += 30
        s["futter"] *= 0.7
        s["begruendungen"].append("🌊 Tiefe Zone: Weniger Futter, stabilere Montage.")
        score += 5

    if tiefe_spot < 3 and "Nachmittag" in zeit:
        s["h_farbe"] = "Matt"
        score += 3

    # -------------------
    # BODEN & HINDERNISSE
    # -------------------
    if boden == "Schlamm" or "Kraut" in hindernisse:
        s["blei_typ"] = "Heli-Safe"
        s["vorfach_len"] += 10
        score += 5

    if any(h in hindernisse for h in ["Totholz", "Muschelbänke"]):
        s["blei_typ"] = "Drop-Off"
        score -= 5

    # -------------------
    # LUFTDRUCK
    # -------------------
    if druck_tendenz == "Fallend":
        s["vorfach_len"] -= 5
        score += 5
    elif druck_tendenz == "Steigend":
        s["vorfach_len"] += 5
        s["h_gr"] += 1
        score -= 5

    # -------------------
    # FISCHVERHALTEN
    # -------------------
    if aktivitaet == "Vorsichtig":
        s["vorfach_len"] += 10
        s["h_gr"] += 1
        score -= 5
    elif aktivitaet == "Aggressiv":
        s["vorfach_len"] -= 5
        score += 5

    # -------------------
    # WEIßFISCH / KREBSE
    # -------------------
    if weissfisch in ["Hoch", "Extrem"] or "Krebse" in hindernisse:
        s["koeder_gr"] = 24
        s["koeder_h"] = "Extra Hart"
        score -= 5

    # -------------------
    # SCORE CLAMP
    # -------------------
    score = max(0, min(100, score))
    s["score"] = score

    if score >= 75:
        s["ampel"] = "🟢 Sehr hohe Chance"
    elif score >= 50:
        s["ampel"] = "🟡 Solide Bedingungen"
    else:
        s["ampel"] = "🔴 Anspruchsvoll"

    return s
