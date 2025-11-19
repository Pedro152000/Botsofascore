def gerar_sinal(historico):
    if not historico:
        return None

    N = 6
    ultimos = historico[-N:]
    gg = 0

    for r in ultimos:
        try:
            a, b = map(int, r.split("x"))
        except:
            continue

        if a > 0 and b > 0:
            gg += 1

    if gg <= 2:
        return f"🔥 SINAL GG — últimos {N} jogos tiveram {gg} GG."

    return None
