# Installation

This page walks you through every step needed to get the Document Reading Agent running on your machine.

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|---|---|---|
| Python | 3.10 | Required by Docling |
| pip | 21.0 | Comes bundled with Python 3.10+ |
| OpenAI API key | – | Required for summarisation, Q&A, and audio features |

---

## 1. Clone the Repository

```bash
git clone https://github.com/codymayhew11-lang/Document-Reading-Agent.git
cd Document-Reading-Agent
```

---

## 2. (Recommended) Create a Virtual Environment

Using a virtual environment keeps project dependencies isolated from your global Python installation.

```bash
# Create the environment
python -m venv .venv

# Activate it – macOS / Linux
source .venv/bin/activate

# Activate it – Windows (Command Prompt)
.venv\Scripts\activate.bat

# Activate it – Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file pins the following packages:

| Package | Version Range | Purpose |
|---|---|---|
| `openai` | `>=1.0.0,<2.0.0` | OpenAI API client |
| `langchain` | `>=0.2.0,<1.0.0` | LLM orchestration framework |
| `langchain-openai` | `>=0.1.0,<1.0.0` | LangChain ↔ OpenAI integration |
| `docling` | `>=2.120.1,<3.0.0` | Rich PDF, DOCX, and XLSX parsing |
| `pypdf` | `>=4.0.0,<5.0.0` | PDF reading support |
| `python-docx` | `>=1.0.0,<2.0.0` | DOCX reading support |
| `openpyxl` | `>=3.1.0,<4.0.0` | XLSX fallback reader |

---

## 4. Set Your OpenAI API Key

The agent uses OpenAI models via LangChain. You must provide a valid API key before running the tool.

**macOS / Linux (current session only)**

```bash
export OPENAI_API_KEY="sk-..."
```

**macOS / Linux (persist across sessions – add to `~/.bashrc` or `~/.zshrc`)**

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (Command Prompt)**

```cmd
set OPENAI_API_KEY=sk-...
```

**Windows (PowerShell)**

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

> **Tip:** Never commit your API key to source control. Consider using a `.env` file with a library such as `python-dotenv` to manage secrets locally.

---

## 5. Verify the Installation

```bash
python main.py --help
```

You should see output similar to:

```text
usage: main.py [-h] [--document PATH] [--query QUERY]
               [--audio-query AUDIO_QUERY] [--transcribe-audio PATH]
               [--create-knowledge-base PATH] [--knowledge-base PATH]
               [--kb-query KB_QUERY] [--kb-top-k KB_TOP_K] [--tts-output PATH]
               [--tts-voice TTS_VOICE] [--tts-model TTS_MODEL]
               [--stt-model STT_MODEL]
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'docling'` | Run `pip install docling` and ensure you are on Python 3.10+ |
| `ModuleNotFoundError: No module named 'pypdf'` | Run `pip install pypdf` |
| `ModuleNotFoundError: No module named 'docx'` | Run `pip install python-docx` |
| `openai.AuthenticationError` | Check that `OPENAI_API_KEY` is set and valid |
| Python version errors | Ensure you are using Python 3.10 or later (`python --version`) |
