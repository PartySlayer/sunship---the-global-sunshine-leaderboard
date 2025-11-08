# 🌞 Sunship — The Global Sunshine Leaderboard

> The world’s only real-time, unbiased, scientifically questionable ranking of nations by current sunlight exposure.

Our sophisticated systems calculate the **Sunny Score** for ten capital cities, based on the world’s most viral countries - totally, *definitely* not hardcoded inside `countries.json`.)

**Data source:** [OpenWeatherMap](https://openweathermap.org/api)  
**Algorithm:** proprietary chaos flubber™

---

### 🗣️ What they say about us

> “Finally, a competitive ranking for the world.”  
> “We didn’t know we needed it, but we always did.”

---

## ⚙️ Technical Bits

- **Application logic:** `fetcher.py` — handles API calls, caching, and scoring.
- **Business logic:** `main.py` — orchestrates leaderboard updates and presentation.
- **Cache system:** JSON dump of leaderboard response (`cache/leaderboard.json`)  
  Default TTL: **1 hour** (based on timestamp).

### 🧮 Scoring Formula

The Sunny Score is a top-secret* function combining:

- temperature,
- cloudiness,
- visibility,
- a mysterious “clear sky” bonus.

> \* okay fine: `(100 - clouds) + (temp / 2) + (visibility / 1000) [+25 if clear sky]`

---

## 🚀 How to Run

1. **Clone the repo**

   ```bash
   git clone https://github.com/PartySlayer/sunship---the-global-sunshine-leaderboard.git
   cd sunship
   ```

2. **Install dependencies**

    ```bash
   pip install -r requirements.txt
    ```

3. **Create .env inside the project dir**

    ```bash
   echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
    ```

4. **Run it!**

    ```bash
   python main.py
        or
   python3 main.py

    ```

## Customize it and have fun

Try to modify the json file adding new cities and refresh the leaderboard!
New data will be retrieved from /api/leaderboard GET request:
