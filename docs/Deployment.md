# Deployment Work Instruction

This work instruction provides step-by-step guidance for deploying the Document Reading Agent in a production or shared-team environment. Follow each step in order and do not skip verification checkpoints.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Obtain the Source Code](#2-obtain-the-source-code)
3. [Create a Dedicated User Account (Server Deployments)](#3-create-a-dedicated-user-account-server-deployments)
4. [Set Up a Python Virtual Environment](#4-set-up-a-python-virtual-environment)
5. [Install Dependencies](#5-install-dependencies)
6. [Configure the OpenAI API Key](#6-configure-the-openai-api-key)
7. [Verify the Installation](#7-verify-the-installation)
8. [Run the Agent](#8-run-the-agent)
9. [Deploy as a Scheduled Job (Optional)](#9-deploy-as-a-scheduled-job-optional)
10. [Deploy as a systemd Service (Optional)](#10-deploy-as-a-systemd-service-optional)
11. [Updating the Agent](#11-updating-the-agent)
12. [Rollback Procedure](#12-rollback-procedure)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Prerequisites

Confirm all of the following are met before beginning deployment.

| Item | Requirement | How to Check |
|---|---|---|
| Operating System | Linux (Ubuntu 20.04+ recommended), macOS 12+, or Windows 10/11 | `uname -a` (Linux/macOS) or `winver` (Windows) |
| Python | 3.9 or later | `python --version` or `python3 --version` |
| pip | 21.0 or later | `pip --version` |
| Git | Any recent version | `git --version` |
| Internet access | Required to install packages and call the OpenAI API | Ping `api.openai.com` |
| OpenAI API key | A valid key with sufficient quota | Log in at [platform.openai.com](https://platform.openai.com) and confirm available credits |
| Disk space | At least 200 MB free | `df -h .` (Linux/macOS) |

> **Checkpoint:** All items above must be confirmed before proceeding. If any item is missing, resolve it before continuing.

---

## 2. Obtain the Source Code

### Option A – Clone from GitHub (recommended)

```bash
git clone https://github.com/codymayhew11-lang/Document-Reading-Agent.git
cd Document-Reading-Agent
```

### Option B – Download a Release Archive

1. Navigate to the [Releases](https://github.com/codymayhew11-lang/Document-Reading-Agent/releases) page on GitHub.
2. Download the `.zip` or `.tar.gz` asset for the desired version.
3. Extract the archive:

   **Linux / macOS**

   ```bash
   tar -xzf Document-Reading-Agent-vX.Y.Z.tar.gz
   cd Document-Reading-Agent-vX.Y.Z
   ```

   **Windows (PowerShell)**

   ```powershell
   Expand-Archive -Path Document-Reading-Agent-vX.Y.Z.zip -DestinationPath .
   cd Document-Reading-Agent-vX.Y.Z
   ```

> **Checkpoint:** Confirm the directory contains `main.py`, `requirements.txt`, and the `agent/` folder before continuing.

---

## 3. Create a Dedicated User Account (Server Deployments)

Running the agent under a dedicated, non-root user account limits the blast radius of any security incident.

> **Skip this step** if you are deploying on a personal workstation or laptop.

**Linux**

```bash
# Create a system user with no login shell and a home directory
sudo useradd --system --create-home --shell /usr/sbin/nologin docagent

# Move the project directory to the new user's home and set ownership
sudo mv /path/to/Document-Reading-Agent /home/docagent/Document-Reading-Agent
sudo chown -R docagent:docagent /home/docagent/Document-Reading-Agent
```

All subsequent steps that reference the project directory assume it is located at `/home/docagent/Document-Reading-Agent`. Adjust the path if you chose a different location.

> **Checkpoint:** Verify ownership with `ls -la /home/docagent/` and confirm `docagent` is the owner.

---

## 4. Set Up a Python Virtual Environment

A virtual environment isolates the agent's dependencies from the system Python installation.

**Linux / macOS**

```bash
cd /path/to/Document-Reading-Agent

python3 -m venv .venv
source .venv/bin/activate
```

**Windows (Command Prompt)**

```cmd
cd C:\path\to\Document-Reading-Agent

python -m venv .venv
.venv\Scripts\activate.bat
```

**Windows (PowerShell)**

```powershell
cd C:\path\to\Document-Reading-Agent

python -m venv .venv
.venv\Scripts\Activate.ps1
```

> **Checkpoint:** Your shell prompt should now be prefixed with `(.venv)`, confirming the environment is active.

---

## 5. Install Dependencies

With the virtual environment active, install all required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output (abbreviated):**

```
Successfully installed langchain-X.Y.Z langchain-openai-X.Y.Z openai-X.Y.Z \
  pypdf-X.Y.Z python-docx-X.Y.Z openpyxl-X.Y.Z ...
```

> **Checkpoint:** Run `pip list` and confirm `openai`, `langchain`, `langchain-openai`, `pypdf`, `python-docx`, and `openpyxl` are all present.

---

## 6. Configure the OpenAI API Key

The agent requires a valid OpenAI API key. **Never hard-code the key in source files or commit it to version control.**

### Option A – Environment Variable (simplest)

**Linux / macOS – current session only**

```bash
export OPENAI_API_KEY="sk-..."
```

**Linux / macOS – persist across sessions**

Add the following line to `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc` (depending on your shell):

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (Command Prompt) – current session only**

```cmd
set OPENAI_API_KEY=sk-...
```

**Windows (PowerShell) – current session only**

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

**Windows – persist across sessions**

```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

### Option B – `.env` File (recommended for team/server deployments)

1. Create a `.env` file in the project root:

   ```bash
   echo 'OPENAI_API_KEY=sk-...' > .env
   chmod 600 .env        # Linux/macOS: restrict to owner only
   ```

2. Confirm `.env` is listed in `.gitignore` so it is never committed:

   ```bash
   grep '\.env' .gitignore
   ```

   If the output is empty, add it:

   ```bash
   echo '.env' >> .gitignore
   ```

3. The agent will automatically load the key from `.env` if `python-dotenv` is installed:

   ```bash
   pip install python-dotenv
   ```

> **Checkpoint:** Run `echo $OPENAI_API_KEY` (Linux/macOS) or `echo %OPENAI_API_KEY%` (Windows Command Prompt) and confirm the key is printed. If using a `.env` file, confirm the file exists and has restricted permissions.

---

## 7. Verify the Installation

Run the built-in help command to confirm the agent starts correctly:

```bash
python main.py --help
```

**Expected output:**

```
usage: main.py [-h] [--document PATH] [--query QUERY]

Document Reading Agent

options:
  -h, --help        show this help message and exit
  --document PATH   Path to a document to read/compare. Supply once for
                    single-document mode; supply two or more times (e.g.
                    --document spec.pdf --document sow.pdf --document
                    bid.xlsx) to enable comparison mode.
  --query QUERY     Optional question to answer from the document
                    (single-document mode only)
```

> **Checkpoint:** If the command fails with `ModuleNotFoundError`, repeat [Step 5](#5-install-dependencies). If it fails with `openai.AuthenticationError` during a real run, revisit [Step 6](#6-configure-the-openai-api-key).

---

## 8. Run the Agent

### 8.1 Summarise a Single Document

```bash
python main.py --document /path/to/your/document.pdf
```

**Example:**

```bash
python main.py --document reports/annual_report.pdf
```

**Example output:**

```
Document loaded: 14832 characters

Summary:
The annual report highlights a 12% increase in revenue for FY2023 ...
```

### 8.2 Answer a Question About a Document

```bash
python main.py --document /path/to/your/document.pdf --query "Your question here"
```

**Example:**

```bash
python main.py --document reports/annual_report.pdf --query "What was the net profit?"
```

**Example output:**

```
Document loaded: 14832 characters

Answer: The net profit for FY2023 was $4.2 million.
```

### 8.3 Compare Multiple Documents

Supply `--document` two or more times. The agent will compare all provided documents and return a structured analysis.

```bash
python main.py \
  --document spec.pdf \
  --document sow.pdf \
  --document bid.xlsx
```

> **Note:** `--query` is not supported in comparison mode.

> **Checkpoint:** Confirm the agent produces meaningful output without errors before proceeding to optional automation steps.

---

## 9. Deploy as a Scheduled Job (Optional)

Use this section to run the agent automatically on a recurring schedule (e.g., nightly document processing).

### Linux / macOS – cron

1. Create a wrapper script at `/home/docagent/run_agent.sh`:

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   # Load the virtual environment
   source /home/docagent/Document-Reading-Agent/.venv/bin/activate

   # Load the API key if using a .env file
   export OPENAI_API_KEY="$(grep OPENAI_API_KEY /home/docagent/Document-Reading-Agent/.env | cut -d '=' -f2-)"

   # Run the agent
   python /home/docagent/Document-Reading-Agent/main.py \
     --document /data/incoming/report.pdf \
     >> /var/log/docagent/run.log 2>&1
   ```

2. Make the script executable:

   ```bash
   chmod +x /home/docagent/run_agent.sh
   ```

3. Create the log directory:

   ```bash
   sudo mkdir -p /var/log/docagent
   sudo chown docagent:docagent /var/log/docagent
   ```

4. Open the crontab for the `docagent` user:

   ```bash
   sudo crontab -u docagent -e
   ```

5. Add a schedule entry. Example – run every day at 2:00 AM:

   ```
   0 2 * * * /home/docagent/run_agent.sh
   ```

6. Save and exit the editor.

> **Checkpoint:** Run the script manually once (`sudo -u docagent /home/docagent/run_agent.sh`) and confirm it completes without errors and produces output in `/var/log/docagent/run.log`.

### Windows – Task Scheduler

1. Open **Task Scheduler** (search for it in the Start menu).
2. Click **Create Basic Task…** in the right-hand Actions panel.
3. Name the task `Document Reading Agent` and click **Next**.
4. Select a trigger (e.g., **Daily**) and configure the schedule; click **Next**.
5. Select **Start a Program** and click **Next**.
6. Set **Program/script** to:
   ```
   C:\path\to\Document-Reading-Agent\.venv\Scripts\python.exe
   ```
7. Set **Add arguments** to:
   ```
   C:\path\to\Document-Reading-Agent\main.py --document C:\data\report.pdf
   ```
8. Set **Start in** to:
   ```
   C:\path\to\Document-Reading-Agent
   ```
9. Click **Finish**, then right-click the task and select **Run** to test it immediately.

> **Checkpoint:** Check the **History** tab in Task Scheduler to confirm the test run completed with result code `0x0`.

---

## 10. Deploy as a systemd Service (Optional)

Use this section to run the agent as a persistent Linux service managed by systemd (e.g., for a long-running or on-demand server deployment).

1. Create the service unit file at `/etc/systemd/system/docagent.service`:

   ```ini
   [Unit]
   Description=Document Reading Agent
   After=network.target

   [Service]
   Type=oneshot
   User=docagent
   WorkingDirectory=/home/docagent/Document-Reading-Agent
   EnvironmentFile=/home/docagent/Document-Reading-Agent/.env
   ExecStart=/home/docagent/Document-Reading-Agent/.venv/bin/python \
       main.py --document /data/incoming/report.pdf
   StandardOutput=journal
   StandardError=journal

   [Install]
   WantedBy=multi-user.target
   ```

2. Reload the systemd daemon to register the new service:

   ```bash
   sudo systemctl daemon-reload
   ```

3. Test the service by running it once:

   ```bash
   sudo systemctl start docagent.service
   sudo systemctl status docagent.service
   ```

4. View logs:

   ```bash
   sudo journalctl -u docagent.service -n 50
   ```

5. Enable the service to start automatically at boot (if needed):

   ```bash
   sudo systemctl enable docagent.service
   ```

> **Checkpoint:** `systemctl status docagent.service` should report `Active: inactive (dead)` with exit code `0` after a successful oneshot run. If the status shows `failed`, inspect the logs with `journalctl`.

---

## 11. Updating the Agent

Follow these steps whenever a new version of the agent is released.

1. Navigate to the project directory:

   ```bash
   cd /path/to/Document-Reading-Agent
   ```

2. Pull the latest changes:

   ```bash
   git pull origin main
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate      # Linux/macOS
   # or
   .venv\Scripts\activate.bat     # Windows Command Prompt
   ```

4. Update dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Verify the updated installation:

   ```bash
   python main.py --help
   ```

> **Checkpoint:** Confirm the help output is displayed without errors. If a dependency conflict arises, delete the virtual environment and recreate it from scratch (repeat Steps 4–5 of this guide).

---

## 12. Rollback Procedure

If a deployment causes unexpected failures, roll back to the previous working version using the steps below.

1. Identify the last known-good commit hash:

   ```bash
   git log --oneline -10
   ```

2. Check out that commit:

   ```bash
   git checkout <commit-hash>
   ```

3. Reinstall dependencies for that version:

   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Verify the rollback:

   ```bash
   python main.py --help
   ```

5. Once the issue is resolved, return to the main branch:

   ```bash
   git checkout main
   pip install -r requirements.txt
   ```

---

## 13. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `ModuleNotFoundError: No module named 'pypdf'` | Dependencies not installed | Activate `.venv` and run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'docx'` | Dependencies not installed | Run `pip install python-docx` |
| `openai.AuthenticationError` | Missing or invalid API key | Check `OPENAI_API_KEY` is exported correctly (see [Step 6](#6-configure-the-openai-api-key)) |
| `openai.RateLimitError` | API quota exceeded | Check your usage at [platform.openai.com](https://platform.openai.com) and upgrade your plan if needed |
| `FileNotFoundError` | Incorrect document path | Use an absolute path, e.g. `/home/user/docs/report.pdf` |
| `ValueError: Unsupported file extension` | Unsupported document format | Convert the file to `.txt`, `.pdf`, or `.docx` before running the agent |
| `python: command not found` | Python not on PATH | Use `python3` instead, or reinstall Python and add it to PATH |
| Virtual environment not activating | Wrong activation script for your shell | See [Step 4](#4-set-up-a-python-virtual-environment) for shell-specific activation commands |
| cron job produces no output | Script not executable or wrong paths | Run the script manually as the cron user and check for errors |
| systemd service shows `failed` | ExecStart path wrong or API key missing | Check `journalctl -u docagent.service` for the specific error message |
