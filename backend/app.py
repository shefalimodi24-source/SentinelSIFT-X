from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data.run_case import analyze_case

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    state = analyze_case(file_path)

    return {
        "findings": state["verified_findings"],
        "tools": state["tool_recommendations"],
        "evidence": state.get("new_evidence", []),
        "reasoning_log": state["reasoning_log"],
        "benchmark": state["benchmark_results"]
    }

    return {
        "findings": state["verified_findings"],
        "tools": state["tool_recommendations"],
        "evidence": state.get("new_evidence", []),
        "reasoning_log": state["reasoning_log"],
        "benchmark": state["benchmark_results"]
    }
