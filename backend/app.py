from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from data.run_case import analyze_case

import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

latest_result = None


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    global latest_result
    try:
        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        # Save the uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"FILE SAVED: {file_path}")

        # Verify file exists and is valid JSON
        if not os.path.exists(file_path):
            raise ValueError(f"Uploaded file not found: {file_path}")

        import json
        try:
            with open(file_path, "r") as f_json:
                json.load(f_json)
        except json.JSONDecodeError as json_e:
            raise ValueError(f"Invalid JSON file: {file.filename}. Error: {json_e}")

        state = analyze_case(file_path)
        print("STATE:", state)

        latest_result = {
            "findings": state["verified_findings"],
            "tools": state["tool_recommendations"],
            "evidence": state.get("new_evidence", []),
            "reasoning_log": state["reasoning_log"],
            "benchmark": state["benchmark_results"]
        }

        return latest_result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": "Internal Server Error",
            "message": str(e),
            "detail": traceback.format_exc()
        }, 500

@app.get("/latest")
def latest():

    if latest_result is None:
        return {
            "findings": [],
            "tools": [],
            "evidence": [],
            "reasoning_log": [],
            "benchmark": {
                "precision": 0,
                "recall": 0,
                "detection_rate": 0
            }
        }

    return latest_result
