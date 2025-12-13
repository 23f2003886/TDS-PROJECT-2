---
title: Autonomous Quiz Solver Agent
emoji: 🤖
colorFrom: purple
colorTo: pink
sdk: docker
pinned: false
app_port: 7860
short_description: AI agent solving data science quizzes autonomously
tags:
  - langchain
  - langgraph
  - ai-agent
  - autonomous-agent
  - data-science
  - gemini
suggested_hardware: cpu-basic
---
# 🤖 Autonomous Quiz Solver Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.3+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0+-orange.svg)](https://langchain-ai.github.io/langgraph/)

An intelligent, autonomous agent built with **LangGraph** and **LangChain** that solves data-related quizzes involving web scraping, data processing, analysis, and visualization tasks. The system uses **Google Gemini 2.5 Flash** to orchestrate tool usage and make decisions.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Tools &amp; Capabilities](#tools--capabilities)
- [Deployment](#deployment)
- [How It Works](#how-it-works)
- [License](#license)

## 🔍 Overview

This project was developed for the TDS (Tools in Data Science) course project, where the objective is to build an application that can autonomously solve multi-step quiz tasks involving:

- **Data sourcing**: Scraping websites, calling APIs, downloading files
- **Data preparation**: Cleaning text, PDFs, and various data formats
- **Data analysis**: Filtering, aggregating, statistical analysis, ML models
- **Data visualization**: Generating charts, narratives, and presentations

The system receives quiz URLs via a REST API, navigates through multiple quiz pages, solves each task using LLM-powered reasoning and specialized tools, and submits answers back to the evaluation server.

## 🏗️ Architecture

The project uses a **LangGraph state machine** architecture with the following components:

```
┌─────────────┐
│   FastAPI   │  ← Receives POST requests with quiz URLs
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Agent     │  ← LangGraph orchestrator with Gemini 2.5 Flash
│   (LLM)     │
└──────┬──────┘
       │
       ├────────────┬────────────┬─────────────┬──────────────┐
       ▼            ▼            ▼             ▼              ▼
   [Scraper]   [Downloader]  [Code Exec]  [POST Req]  [Add Deps]
```

### Key Components:

1. **FastAPI Server** (`main.py`): Handles incoming POST requests, validates secrets, and triggers the agent
2. **LangGraph Agent** (`agent.py`): State machine that coordinates tool usage and decision-making
3. **Tools Package** (`tools/`): Modular tools for different capabilities
4. **LLM**: Google Gemini 2.5 Flash with rate limiting (9 requests per minute)

## ✨ Features

- ✅ **Autonomous multi-step problem solving** — Chains together multiple quiz pages
- ✅ **Dynamic JavaScript rendering** — Uses Playwright for client-side rendered pages
- ✅ **Code generation & execution** — Writes and runs Python code for data tasks
- ✅ **Flexible data handling** — Downloads files, processes PDFs, CSVs, images, audio
- ✅ **OCR & Image Processing** — Tesseract-based text extraction from images
- ✅ **Audio Transcription** — Supports Whisper, SpeechRecognition, AssemblyAI
- ✅ **Self-installing dependencies** — Automatically adds required Python packages
- ✅ **Robust error handling** — Retries failed attempts within time limits
- ✅ **Docker containerization** — Ready for HuggingFace Spaces deployment
- ✅ **Rate limiting** — Respects API quotas with exponential backoff

## 📁 Project Structure

```
TDS-PROJECT-2/
├── main.py                     # FastAPI server with /solve endpoint
├── agent.py                    # LangGraph state machine & orchestration
├── llm.py                      # LLM client configuration (Gemini)
├── solver_agent.py             # Core solver logic
├── pipeline_manager.py         # Pipeline orchestration
├── scraper.py                  # Web scraping utilities
├── shared_store.py             # Shared state management
├── pyproject.toml              # Project dependencies (uv)
├── Dockerfile                  # Container image with Playwright & FFmpeg
├── tools/
│   ├── web_scraper.py          # Playwright-based HTML renderer
│   ├── run_code.py             # Python code executor
│   ├── download_file.py        # File downloader
│   ├── submit_answer.py        # Answer submission handler
│   ├── add_dependencies.py     # Dynamic package installer
│   ├── audio_transcribing.py   # Audio transcription (Whisper/SpeechRecognition)
│   ├── image_content_extracter.py  # OCR with Tesseract
│   ├── encode_image_to_base64.py   # Image encoding utility
│   ├── send_request.py         # HTTP POST tool
│   └── code_generate_and_run.py    # Code generation & execution
└── README.md
```

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Git
- FFmpeg (for audio processing)

### Step 1: Clone the Repository

```bash
git clone https://github.com/23f2003886/TDS-PROJECT-2.git
cd TDS-PROJECT-2
```

### Step 2: Install Dependencies

#### Option A: Using `uv` (Recommended)

```bash
# Install uv if you don't have it
pip install uv

# Create virtual environment and install dependencies
uv venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install project in editable mode
uv pip install -e .

# Install Playwright browsers
playwright install chromium
```

#### Option B: Using `pip`

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -e .

# Install Playwright browsers
playwright install chromium
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Your credentials from the Google Form submission
EMAIL=your_email
SECRET=your_secret

# AI Pipe API Key 
AIPIPE_KEY=your_aipipe_key
```

### Getting an AIPIPE Key

1. Get your AIPIPE key from the TDS course portal or your instructor
2. Copy it to your `.env` file

## 🚀 Usage

### Local Development

Start the FastAPI server:

```bash
# If using uv
uv run main.py

# If using standard Python
python main.py
```

The server will start on `http://0.0.0.0:7860`

### Testing the Endpoint

Send a POST request to test your setup:

```bash
curl -X POST http://localhost:7860/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your_secret_string",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

Expected response:

```json
{
  "status": "ok"
}
```

The agent will run in the background and solve the quiz chain autonomously.

## 🌐 API Endpoints

### `POST /solve`

Receives quiz tasks and triggers the autonomous agent.

**Request Body:**

```json
{
  "email": "your.email@example.com",
  "secret": "your_secret_string",
  "url": "https://example.com/quiz-123"
}
```

**Responses:**

| Status Code | Description                    |
| ----------- | ------------------------------ |
| `200`     | Secret verified, agent started |
| `400`     | Invalid JSON payload           |
| `403`     | Invalid secret                 |

### `GET /healthz`

Health check endpoint for monitoring.

**Response:**

```json
{
  "status": "ok",
  "uptime_seconds": 3600
}
```

## 🛠️ Tools & Capabilities

The agent has access to the following tools:

### 1. **Web Scraper** (`get_rendered_html`)

- Uses Playwright to render JavaScript-heavy pages
- Waits for network idle before extracting content
- Returns fully rendered HTML for parsing

### 2. **File Downloader** (`download_file`)

- Downloads files (PDFs, CSVs, images, audio, etc.) from direct URLs
- Saves files to `LLMFiles/` directory
- Returns the saved filename

### 3. **Code Executor** (`run_code`)

- Executes arbitrary Python code in an isolated subprocess
- Returns stdout, stderr, and exit code
- Useful for data processing, analysis, and visualization

### 4. **Answer Submitter** (`submit_answer`)

- Submits JSON payloads to quiz submission endpoints
- Parses response for correctness and next URL
- Handles retry logic within time limits

### 5. **Dependency Installer** (`add_dependencies`)

- Dynamically installs Python packages as needed
- Uses `uv add` for fast package resolution
- Enables the agent to adapt to different task requirements

### 6. **Audio Transcription** (`transcribe_audio`)

- Transcribes MP3/WAV audio files to text
- Supports Google Speech Recognition API
- Auto-converts MP3 to WAV using pydub/FFmpeg

### 7. **OCR / Image Text Extraction** (`ocr_image_tool`)

- Extracts text from images using Tesseract OCR
- Supports base64, file path, or PIL.Image input
- Configurable language support

### 8. **Image Encoder** (`encode_image_to_base64`)

- Encodes images to base64 for API payloads
- Used for vision model inputs

## 🚀 Deployment

### Deploy to HuggingFace Spaces

This project is designed to run on HuggingFace Spaces with Docker SDK.

#### Step 1: Create a HuggingFace Space

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in the details:
   - **Space name**: `llm-analysis-quiz-solver` (or your preferred name)
   - **License**: MIT
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free tier works fine)
4. Click **"Create Space"**

#### Step 2: Add Secrets

In your Space settings, add the following secrets:

1. Go to **Settings** → **Repository secrets**
2. Add these secrets:
   - `EMAIL`: Your email from Google Form submission
   - `SECRET`: Your secret string from Google Form submission
   - `AIPIPE_KEY`: Your AIPIPE API key

#### Step 3: Push Your Code

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: LLM Analysis Quiz Solver"

# Add HuggingFace Space as remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to HuggingFace
git push --force space main
```

#### Step 4: Wait for Build

- HuggingFace will automatically build your Docker container
- This may take 5-10 minutes
- Monitor the build logs in the "Build" tab
- Once complete, your Space will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

#### Step 5: Test Your Deployment

```bash
curl -X POST https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space/solve \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your.email@example.com",
    "secret": "your_secret_string",
    "url": "https://tds-llm-analysis.s-anand.net/demo"
  }'
```

#### Updating Your Space

To update your deployed Space:

```bash
git add .
git commit -m "Update: description of changes"
git push space main
```

### Alternative: Push to GitHub First

If you want to maintain the code on GitHub and HuggingFace:

```bash
# Push to GitHub
git remote add origin https://github.com/23f2003886/TDS-PROJECT-2.git
git push -u origin main

# Also push to HuggingFace Space
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
git push space main
```

## 🧠 How It Works

### 1. Request Reception

- FastAPI receives a POST request with quiz URL
- Validates the secret against environment variables
- Returns 200 OK and starts the agent in the background

### 2. Agent Initialization

- LangGraph creates a state machine with two nodes: `agent` and `tools`
- The initial state contains the quiz URL as a user message

### 3. Task Loop

The agent follows this loop:

```
┌─────────────────────────────────────────┐
│ 1. LLM analyzes current state           │
│    - Reads quiz page instructions       │
│    - Plans tool usage                   │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 2. Tool execution                       │
│    - Scrapes page / downloads files     │
│    - Runs analysis code                 │
│    - Submits answer                     │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 3. Response evaluation                  │
│    - Checks if answer is correct        │
│    - Extracts next quiz URL (if exists) │
└─────────────────┬───────────────────────┘
                  ▼
┌─────────────────────────────────────────┐
│ 4. Decision                             │
│    - If new URL exists: Loop to step 1  │
│    - If no URL: Return "END"            │
└─────────────────────────────────────────┘
```

### 4. State Management

- All messages (user, assistant, tool) are stored in state
- The LLM uses full history to make informed decisions
- Recursion limit set to 200 to handle long quiz chains

### 5. Completion

- Agent returns "END" when no new URL is provided
- Background task completes
- Logs indicate success or failure

## 📝 Key Design Decisions

1. **LangGraph over Sequential Execution** — Allows flexible routing and complex decision-making
2. **Background Processing** — Prevents HTTP timeouts for long-running quiz chains
3. **Tool Modularity** — Each tool is independent and can be tested/debugged separately
4. **Rate Limiting** — Prevents API quota exhaustion (9 req/min for Gemini)
5. **Code Execution** — Dynamically generates and runs Python for complex data tasks
6. **Playwright for Scraping** — Handles JavaScript-rendered pages that `requests` cannot
7. **uv for Dependencies** — Fast package resolution and installation
8. **Multi-Modal Support** — OCR, audio transcription, and image encoding built-in

## 🔧 Tech Stack

| Component                  | Technology                       |
| -------------------------- | -------------------------------- |
| **LLM**              | Google Gemini 2.5 Flash          |
| **Orchestration**    | LangGraph + LangChain            |
| **Web Framework**    | FastAPI + Uvicorn                |
| **Web Scraping**     | Playwright (Chromium)            |
| **OCR**              | Tesseract                        |
| **Audio**            | FFmpeg, pydub, SpeechRecognition |
| **Package Manager**  | uv                               |
| **Containerization** | Docker                           |
| **Deployment**       | HuggingFace Spaces               |

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author**: Jaswanth Prasanna V
**Course**: Tools in Data Science (TDS)
**Institution**: IIT Madras

For questions or issues, please open an issue on the [GitHub repository](https://github.com/23f2003886/TDS-PROJECT-2).
