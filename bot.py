import requests
import time
import telebot

TOKEN = "8279285665:AAGRi2DQg3Mu3gJmZrKdub_0oHybZKQOSA0"
CHAT_ID = "959511946"

bot = telebot.TeleBot(TOKEN)

SOFA_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

def get_live_matches():
    try:
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        r = requests.get(url, headers=SOFA_HEADERS, timeout=10)
        data = r.json()
        return data.get("events", [])
    except:
        return []

def get_stats(match_id):
    try:
        url = f"https://api.sofascore.com/api/v1/event/{match_id}/statistics"
        r = requests.get(url, headers=SOFA_HEADERS, timeout=10)
        data = r.json()

        groups = data.get("statistics", [])
        if not groups:
            return None

        try:
            groups = groups[0].get("groups", groups[0])
        except:
            pass

        ataques = 0
        perigosos = 0
        chutes = 0

        for g in groups:
            for item in g.get("statisticsItems", []):
                name = item.get("name", "").lower()

                if "attacks" in name:
                    ataques += (item.get("home") or 0) + (item.get("away") or 0)

                if "dangerous" in name:
                    perigosos += (item.get("home") or 0) + (item.get("away") or 0)

                if "shots" in name:
                    chutes += (item.get("home") or 0) + (item.get("away") or 0)

        return ataques, perigosos, chutes

    except:
        return None

def filtrar_sinal(match, ataques, perigosos, chutes):
    minuto = match.get("time", {}).get("minute", 0) or 0

    prob_gol = perigosos * 3 + chutes * 2
    prob_esc = ataques * 1.6

    prob_gol = min(prob_gol, 98)
    prob_esc = min(prob_esc, 97)

    sinal_gol = (
        perigosos >= 15 and
        chutes >= 10 and
        prob_gol >= 70 and
        15 <= minuto <= 80
    )

    sinal_esc = (
        ataques >= 60 and
        prob_esc >= 75 and
        minuto <= 85
    )

    return sinal_gol, sinal_esc, prob_gol, prob_esc

def enviar_sinal(match, tipo, ataques, perigosos, chutes, prob):
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    minuto = match["time"].get("minute", "N/A")

    msg = f"""
🔔 SINAL FILTRADO — {tipo}
🏟 {home} x {away}

📊 Estatísticas
• Ataques: {ataques}
• Ataques perigosos: {perigosos}
• Chutes: {chutes}

🔥 Probabilidade: {prob}%
⏱ Minuto: {minuto}
"""
    bot.send_message(CHAT_ID, msg)

def run_bot():
    bot.send_message(CHAT_ID, "🚀 BOT FILTRADO SOFASCORE INICIADO!")

    while True:
        jogos = get_live_matches()
        for jogo in jogos:
            stats = get_stats(jogo["id"])
            if not stats:
                continue

            ataques, perigosos, chutes = stats

            sinal_gol, sinal_esc, prob_gol, prob_esc = filtrar_sinal(
                jogo, ataques, perigosos, chutes
            )

            if sinal_gol:
                enviar_sinal(jogo, "GOL", ataques, perigosos, chutes, prob_gol)

            if sinal_esc:
                enviar_sinal(jogo, "ESCANTEIO", ataques, perigosos, chutes, prob_esc)

        time.sleep(30)

run_bot()
