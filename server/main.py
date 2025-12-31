from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
import threading
import time

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

JOBS = {}

def process_job(job_id: str):
    steps = [
        ("transcribing", "Transcribing Speech"),
        ("translating", "Translating Content"),
        ("voice", "Generating AI Voice"),
        ("done", "Completed"),
    ]

    for status, step in steps:
        time.sleep(5)
        JOBS[job_id]["status"] = status
        JOBS[job_id]["step"] = step


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "uploaded",
        "step": "Upload Success"
    }

    threading.Thread(target=process_job, args=(job_id,)).start()

    return {
        "job_id": job_id,
        "status": "uploaded"
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id not in JOBS:
        return {"error": "Invalid job id"}
    return JOBS[job_id]


@app.get("/")
def root():
    return {"status": "server running"}


@app.get("/health")
def health():
    return {"health": "ok"}
