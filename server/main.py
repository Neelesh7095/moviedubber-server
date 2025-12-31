import threading
import time
def process_job(job_id: str):
    steps = [
        ("transcribing", "Transcribing Speech"),
        ("translating", "Translating Content"),
        ("voice", "Generating AI Voice"),
        ("completed", "Completed")
    ]

    for status, step in steps:
        time.sleep(5)  # 5 sec delay
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


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

JOBS = {}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    JOBS[job_id] = {
        "status": "uploaded",
        "step": "Upload Success"
    }

    return {
        "job_id": job_id,
        "status": "uploaded"
    }

@app.get("/status/{job_id}")
def check_status(job_id: str):
    if job_id not in JOBS:
        return {"error": "Invalid job id"}

    status = JOBS[job_id]["status"]

    if status == "uploaded":
        JOBS[job_id]["status"] = "transcribing"
        JOBS[job_id]["step"] = "Transcribing Speech"
        return JOBS[job_id]

    if status == "transcribing":
        JOBS[job_id]["status"] = "translating"
        JOBS[job_id]["step"] = "Translating Content"
        return JOBS[job_id]

    if status == "translating":
        JOBS[job_id]["status"] = "voice"
        JOBS[job_id]["step"] = "Generating AI Voice"
        return JOBS[job_id]

    if status == "voice":
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["step"] = "Completed"
        return {
            "status": "done",
            "step": "Completed",
            "output_url": "https://example.com/final_video.mp4"
        }

    return JOBS[job_id]

@app.get("/")
def root():
    return {"status": "server running"}

@app.get("/health")
def health():
    return {"health": "ok"}
