import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CACHE_FILE = "cache/leaderboard.json"
COUNTRIES_FILE = 'back2/countries.json'
CACHE_TTL = 3600  # seconds (1 hour)


def load_countries():
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_sunny_score(temp, clouds, visibility, description):
    score = (100 - clouds) + (temp / 2) + (visibility / 1000)
    if "clear" in description.lower():
        score += 25
    return round(score, 2)


def fetch_weather(country):
    """Fetch current weather for a single country"""
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": country, "appid": API_KEY, "units": "metric"},
            timeout=5
        )
        data = resp.json()
        if resp.status_code != 200:
            return None

        return {
            "country": country,
            "temp": data["main"]["temp"],
            "clouds": data["clouds"]["all"],
            "visibility": data.get("visibility", 10000),
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        print(f"[WARN] Failed to fetch {country}: {e}")
        return None


def build_leaderboard():
    countries = load_countries()
    results = []
    for c in countries:
        w = fetch_weather(c)
        if not w:
            continue
        score = compute_sunny_score(
            w["temp"], w["clouds"], w["visibility"], w["description"]
        )
        results.append({
            "country": c,
            "temp": w["temp"],
            "clouds": w["clouds"],
            "visibility": w["visibility"],
            "description": w["description"],
            "score": score
        })

    leaderboard = sorted(results, key=lambda x: x["score"], reverse=True)
    return leaderboard[:10]


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if time.time() - data["timestamp"] > CACHE_TTL:
        return None
    return data["leaderboard"]


def save_cache(leaderboard):
    os.makedirs("cache", exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"timestamp": time.time(), "leaderboard": leaderboard}, f, indent=2)


def get_leaderboard(force_refresh=False):
    if not force_refresh:
        cached = load_cache()
        if cached:
            return cached
    leaderboard = build_leaderboard()
    save_cache(leaderboard)
    return leaderboard
