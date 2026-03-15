# Document Reading Agent – Wiki

Welcome to the **Document Reading Agent** wiki! This project is an AI-powered command-line tool for reading, parsing, and extracting information from documents using Large Language Models (LLMs).

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Pages](#pages)
6. [Deployment](Deployment.md)

---

## Overview

The Document Reading Agent lets you point it at any supported document file and either:

- Get an **automatic summary** of the document's contents, or
- **Ask a natural-language question** and receive a direct answer grounded in the document.

Under the hood it uses [LangChain](https://www.langchain.com/) and the OpenAI API to power the summarisation and question-answering pipelines.

---

## Features

| Feature | Description |
|---|---|
| Multi-format reading | Supports `.txt`, `.pdf`, and `.docx` files out of the box |
| AI summarisation | Generates concise summaries via LangChain's summarise chain |
| Document Q&A | Answers free-text questions using LangChain's QA chain |
| Extensible design | Modular `DocumentReader` and `Extractor` classes are easy to extend |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/codymayhew11-lang/Document-Reading-Agent.git
cd Document-Reading-Agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# 4. Summarise a document
python main.py --document my_report.pdf

# 5. Ask a question about a document
python main.py --document my_report.pdf --query "What are the key findings?"
```

---

## Project Structure

```
Document-Reading-Agent/
├── docs/                 # Wiki documentation (this directory)
│   ├── Home.md
│   ├── Installation.md
│   ├── Usage.md
│   ├── Architecture.md
│   ├── API-Reference.md
│   └── Contributing.md
├── agent/
│   ├── __init__.py
│   ├── reader.py         # DocumentReader – reads .txt / .pdf / .docx files
│   └── extractor.py      # Extractor – summarises and answers questions via LLM
├── main.py               # CLI entry point
├── requirements.txt
└── README.md
```

---

## Pages

| Page | Description |
|---|---|
| [Installation](Installation.md) | Prerequisites and step-by-step setup guide |
| [Usage](Usage.md) | CLI reference, flags, and worked examples |
| [Architecture](Architecture.md) | Module overview and data-flow diagram |
| [API Reference](API-Reference.md) | Detailed class and method documentation |
| [Contributing](Contributing.md) | How to contribute to the project |
| [Deployment](Deployment.md) | Work instruction for deploying the agent in production or shared-team environments |
