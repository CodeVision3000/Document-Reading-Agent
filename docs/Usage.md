# Usage

This page covers all the ways you can run the Document Reading Agent from the command line.

---

## Synopsis

```
python main.py --document <path> [--query <question>]
```

---

## Command-Line Options

| Flag | Required | Description |
|---|---|---|
| `--document <path>` | Yes | Path to the document file to process |
| `--query <question>` | No | A natural-language question to answer from the document. If omitted, the agent produces a summary instead. |
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

## Supported Document Formats

| Extension | Format | Required Library |
|---|---|---|
| `.txt` | Plain text | None (built-in) |
| `.pdf` | Portable Document Format | `pypdf` |
| `.docx` | Microsoft Word | `python-docx` |

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
| `OPENAI_API_KEY` | **Required.** Your OpenAI API key, used by LangChain for summarisation and Q&A. |

See [Installation](Installation.md) for instructions on setting this variable.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| Non-zero | An error occurred (file not found, unsupported format, missing API key, etc.) |
