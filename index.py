# My First AI-Powered Financial Sidekick! 
# A simple, rule-based cryptocurrency advisor chatbot.
# Run: python chatbot.py

from typing import Dict, Tuple

# 1) Chatbot Personality
BOT_NAME = "CryptoHomeboy"
BOT_TONE = "friendly, emoji-sprinkled, and beginner-friendly"
DISCLAIMER = (
    "⚠️ Disclaimer: Crypto is risky—always do your own research (DYOR). "
    "This bot is educational and NOT financial advice."
)

# 2) Predefined Crypto Data (small, easy-to-edit knowledge base)
crypto_db: Dict[str, Dict] = {
    "Bitcoin": {
        "ticker": "BTC",
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3/10,
    },
    "Ethereum": {
        "ticker": "ETH",
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6/10,
    },
    "Cardano": {
        "ticker": "ADA",
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8/10,
    },
}

def explain_coin(coin: str) -> str:
    d = crypto_db[coin]
    return (
        f"{coin} ({d['ticker']}): trend={d['price_trend']}, market cap={d['market_cap']}, "
        f"energy use={d['energy_use']}, sustainability={d['sustainability_score']*10:.0f}/10"
    )

# 3) Core Rules / Scoring
def profitability_score(coin: str) -> int:
    d = crypto_db[coin]
    score = 0
    if d["price_trend"] == "rising":
        score += 2
    elif d["price_trend"] == "stable":
        score += 1
    if d["market_cap"] == "high":
        score += 2
    elif d["market_cap"] == "medium":
        score += 1
    return score

def sustainability_score(coin: str) -> float:
    d = crypto_db[coin]
    score = d["sustainability_score"] * 10  # 0..10
    if d["energy_use"] == "low":
        score += 2
    elif d["energy_use"] == "medium":
        score += 1
    return score

def top_by_profitability() -> Tuple[str, int]:
    coins = list(crypto_db.keys())
    best = max(coins, key=profitability_score)
    return best, profitability_score(best)

def top_by_sustainability() -> Tuple[str, float]:
    coins = list(crypto_db.keys())
    best = max(coins, key=sustainability_score)
    return best, sustainability_score(best)

def compare(a: str, b: str) -> str:
    a, b = a.title(), b.title()
    if a not in crypto_db or b not in crypto_db:
        return "I can only compare coins in my database. Try: Bitcoin, Ethereum, Cardano."
    pa, pb = profitability_score(a), profitability_score(b)
    sa, sb = sustainability_score(a), sustainability_score(b)
    lines = [
        f"🆚 Comparing {a} vs {b}:",
        f"• Profitability → {a}: {pa} | {b}: {pb}  → {'✅ '+a if pa>pb else ('✅ '+b if pb>pa else 'Tie')}",
        f"• Sustainability → {a}: {sa:.1f} | {b}: {sb:.1f}  → {'✅ '+a if sa>sb else ('✅ '+b if sb>sa else 'Tie')}",
    ]
    return "\n".join(lines)

def handle_query(q: str) -> str:
    q_low = q.lower().strip()

    if q_low in ("hi", "hello", "hey"):
        return f"Hey there! I’m {BOT_NAME}, your {BOT_TONE} crypto sidekick. {DISCLAIMER}"

    if "help" in q_low:
        return (
            "Try asking:\n"
            "• Which crypto is trending up?\n"
            "• What’s the most sustainable coin?\n"
            "• Which coin should I buy for long-term growth?\n"
            "• Compare Bitcoin vs Ethereum\n"
            "• Why do you recommend Cardano?\n"
            "• list (to see all coins) | data (to see raw data)\n"
            "• exit (to quit)\n"
        )

    if q_low == "list":
        return "I know about: " + ", ".join(crypto_db.keys())

    if q_low == "data":
        return "\n".join([f"• {explain_coin(c)}" for c in crypto_db])

    if "sustainable" in q_low or "eco" in q_low or "green" in q_low:
        coin, score = top_by_sustainability()
        return (
            f"🌱 I recommend {coin}! It scores {score:.1f}/10 on sustainability and uses "
            f"{crypto_db[coin]['energy_use']} energy. {DISCLAIMER}"
        )

    if "trend" in q_low or "rising" in q_low or "going up" in q_low or "up?" in q_low:
        ups = [c for c, d in crypto_db.items() if d["price_trend"] == "rising"]
        if ups:
            pretty = ", ".join(ups)
            return f"📈 Trending up: {pretty}. {DISCLAIMER}"
        return "I don't see any coin trending up right now."

    if "long-term" in q_low or "growth" in q_low or "buy" in q_low or "profitable" in q_low:
        coin, score = top_by_profitability()
        return (
            f"🚀 For growth potential, {coin} looks best by my simple rules (profitability score {score}). "
            f"It has price_trend='{crypto_db[coin]['price_trend']}' and market_cap='{crypto_db[coin]['market_cap']}'. "
            f"{DISCLAIMER}"
        )

    if "compare" in q_low and " vs " in q_low:
        parts = q_low.replace("compare", "").strip().split(" vs ")
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            return compare(a, b)

    if q_low.startswith("why") or "why do you recommend" in q_low:
        for coin in crypto_db:
            if coin.lower() in q_low:
                p = profitability_score(coin)
                s = sustainability_score(coin)
                return (
                    f"🤔 I like {coin} because its profitability score is {p} and sustainability is {s:.1f}/10. "
                    f"Details → {explain_coin(coin)}. {DISCLAIMER}"
                )
        return "Tell me which coin (e.g., 'Why Cardano?')."

    for coin in crypto_db:
        if coin.lower() in q_low or crypto_db[coin]["ticker"].lower() in q_low:
            return f"Here’s what I know:\n• {explain_coin(coin)}\n{DISCLAIMER}"

    return (
        "I didn’t catch that. Type 'help' for ideas, or try:\n"
        "• Which crypto is trending up?\n"
        "• What’s the most sustainable coin?\n"
        "• Compare Bitcoin vs Ethereum\n"
    )

def main():
    print(f"👋 {BOT_NAME}: Hey! Let’s find you a green and growing crypto. Type 'help' for examples.")
    print(DISCLAIMER)
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye! 👋")
            break
        if user.lower() in ("exit", "quit", "bye"):
            print("Bye! 👋")
            break
        reply = handle_query(user)
        print(f"{BOT_NAME}: {reply}")

if __name__ == "__main__":
    main()
