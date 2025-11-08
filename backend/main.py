from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fetcher import get_leaderboard

app = FastAPI(title="Global Sunshine Leaderboard")
app.mount("/", StaticFiles(directory="static", html=True), name="static")   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust later if goes in cloud
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/leaderboard")
def leaderboard():
    data = get_leaderboard()
    return {"leaderboard": data}


@app.post("/api/refresh")
def refresh():
    data = get_leaderboard(force_refresh=True)
    return {"leaderboard": data, "message": "Cache refreshed"}


@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)