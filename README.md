# SentinelSIFT-X

SentinelSIFT-X is an autonomous Digital Forensics and Incident Response (DFIR) investigation platform built for the SANS AI Cybersecurity Hackathon.

The system uses a multi-agent architecture inspired by the SIFT methodology to analyze forensic evidence, correlate findings, verify conclusions, and generate investigation reports.

## Architecture

SentinelSIFT-X consists of specialized agents:

* Memory Agent
* Disk Agent
* Log Agent
* Protocol SIFT Agent
* Windows Artifact Agent
* Correlation Agent
* Challenge Agent
* Contradiction Agent
* Verifier Agent
* Tool Selection Agent

Each agent performs a focused forensic task and contributes evidence-backed findings to the final report.

## Features

* Autonomous forensic investigation workflow
* Multi-agent reasoning architecture
* Evidence correlation across artifacts
* Investigation plan generation
* Verification and self-correction pipeline
* Structured reasoning logs
* Benchmark evaluation framework
* REST API for frontend integration

## Technology Stack

* Python
* FastAPI
* LangGraph
* Pydantic
* Uvicorn

## Repository Structure

```text
backend/
graph/
agents/
data/
uploads/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/sentinelsift-x.git

cd sentinelsift-x
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn backend.app:app --reload
```

API will be available at:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

## Example Investigation

Run a sample case:

```bash
python data/run_case.py data/case3.json
```

## API Endpoints

### Upload and Analyze

```http
POST /analyze
```

Upload a forensic case file and start an investigation.

### Latest Investigation

```http
GET /latest
```

Retrieve the latest investigation results.

## Multi-Agent Workflow

```text
Input Evidence
      |
      v
Memory Agent
Disk Agent
Log Agent
      |
      v
Protocol SIFT Agent
      |
      v
Windows Artifact Agent
      |
      v
Correlation Agent
      |
      v
Challenge Agent
      |
      v
Contradiction Agent
      |
      v
Verifier Agent
      |
      v
Tool Selection Agent
      |
      v
Investigation Report
```

## Demo

Frontend:

```text
https://sentinelsift-x-dashboard.vercel.app
```

Backend:

```text
https://sentinelsift-x-production.up.railway.app
```

## License

MIT License

## Acknowledgements

Built for the SANS AI Cybersecurity Hackathon using concepts from the SIFT (SANS Investigative Forensic Toolkit) methodology.
