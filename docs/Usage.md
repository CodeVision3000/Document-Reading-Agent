# Usage

This page covers all the ways you can run the Document Reading Agent from the command line.

---

## Synopsis

```bash
python main.py --document <path> [--query <question>]
python main.py --document <path> --audio-query <audio-path>
python main.py --transcribe-audio <audio-path>
python main.py --document <path> --create-knowledge-base <kb.json>
python main.py --knowledge-base <kb.json> --kb-query <question>
```

---

## Command-Line Options

| Flag | Required | Description |
|---|---|---|
| `--document <path>` | Yes | Path to the document file to process |
| `--query <question>` | No | A natural-language question to answer from the document. If omitted, the agent produces a summary instead. |
| `--audio-query <path>` | No | Audio file containing a spoken question to transcribe before answering |
| `--transcribe-audio <path>` | No | Transcribe an audio file and exit |
| `--create-knowledge-base <path>` | No | Build a reusable JSON knowledge base from the supplied document(s) |
| `--knowledge-base <path>` | No | Query an existing knowledge base JSON file |
| `--kb-query <question>` | No | The question to ask against a knowledge base |
| `--kb-top-k <int>` | No | Number of knowledge-base chunks to retrieve before answering |
| `--tts-output <path>` | No | Save the final result as spoken audio |
| `--tts-voice <name>` | No | Voice used when generating audio output |
| `--tts-model <name>` | No | OpenAI text-to-speech model |
| `--stt-model <name>` | No | OpenAI speech-to-text model |
| `-h`, `--help` | No | Print usage information and exit |

---

## Modes of Operation

### Summarize Mode

When `--query` is **not** provided the agent reads the document and produces an AI-generated summary.

```bash
python main.py --document reports/annual_report.pdf
```

**Example output:**

```
Document loaded: 14832 characters

Summary:
The annual report highlights a 12% increase in revenue for FY2023, driven
primarily by growth in the cloud services division. Operating costs remained
stable while net profit rose to $4.2 million. The board approved a dividend
increase of 5 cents per share.
```

---

### Question-Answering Mode

When `--query` is provided the agent answers your specific question using the document as context.

```bash
python main.py --document reports/annual_report.pdf --query "What was the net profit?"
```

**Example output:**

```
Document loaded: 14832 characters

Answer: The net profit for FY2023 was $4.2 million.
```

---

### Talk-to-Text / Talk-to-Talk Mode

Use an audio file as the question source:

```bash
python main.py --document reports/annual_report.pdf --audio-query question.wav
```

Generate a spoken answer:

```bash
python main.py \
  --document reports/annual_report.pdf \
  --audio-query question.wav \
  --tts-output answer.mp3
```

To transcribe speech without querying a document:

```bash
python main.py --transcribe-audio question.wav
```

---

### Knowledge-Base Mode

Build a knowledge base from one or more documents:

```bash
python main.py \
  --document spec.pdf \
  --document scope_of_work.pdf \
  --create-knowledge-base kb/project.json
```

Query a saved knowledge base:

```bash
python main.py \
  --knowledge-base kb/project.json \
  --kb-query "Which items are excluded?"
```

---

## Supported Document Formats

| Extension | Format | Required Library |
|---|---|---|
| `.txt` | Plain text | None (built-in) |
| `.pdf` | Portable Document Format | `docling` (preferred), `pypdf` (fallback) |
| `.docx` | Microsoft Word | `docling` (preferred), `python-docx` (fallback) |
| `.xlsx` | Microsoft Excel | `docling` (preferred), `openpyxl` (fallback) |

Passing a file with an unsupported extension raises a `ValueError`.

---

## Examples

**Summarise a plain-text file:**

```bash
python main.py --document notes.txt
```

**Ask a question about a Word document:**

```bash
python main.py --document contract.docx --query "What is the payment schedule?"
```

**Summarise a PDF:**

```bash
python main.py --document whitepaper.pdf
```

**Use a relative or absolute path:**

```bash
python main.py --document /home/user/docs/research.pdf --query "What methodology was used?"
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Required for summarisation, Q&A, speech input/output, and embedding-backed knowledge-base retrieval. |

See [Installation](Installation.md) for instructions on setting this variable.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| Non-zero | An error occurred (file not found, unsupported format, missing API key, etc.) |
