from fastapi import FastAPI

app = FastAPI(title="MovieDubber Cloud Server")

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "MovieDubber backend is running"
    }

@app.get("/health")
def health():
    return {
        "health": "good"
    }
