# Architecture

This page describes the internal structure of the Document Reading Agent, how its components fit together, and the data flow from CLI invocation to final output.

---

## High-Level Overview

```
User
 │
 │  python main.py --document <file> [--query <question>]
 ▼
main.py  ──────────────────────────────────────────────────────────
 │                                                                  │
 │  DocumentReader.read(file_path)                                  │
 ▼                                                                  │
agent/reader.py                                                     │
 │  Dispatches to the correct reader based on file extension        │
 │  Returns raw text content (str)                                  │
 ▼                                                                  │
main.py  ──────────────────────────────────────────────────────────
 │
 │  If --query provided:  Extractor.answer_question(content, query)
 │  Otherwise:            Extractor.summarize(content)
 ▼
agent/extractor.py
 │  Wraps content in a LangChain Document object
 │  Calls the appropriate LangChain chain (summarise / QA)
 │  Calls the OpenAI API via langchain-openai
 ▼
OpenAI API  →  returns generated text
 │
 ▼
main.py  →  prints result to stdout
```

---

## Module Descriptions

### `main.py`

The CLI entry point. It:

1. Parses command-line arguments using `argparse`.
2. Instantiates `DocumentReader` and calls `read()` to load the document.
3. Instantiates `Extractor` and calls either `summarize()` or `answer_question()` depending on whether `--query` was supplied.
4. Prints the result to standard output.

---

### `agent/reader.py` – `DocumentReader`

Responsible for loading a document from disk and returning its plain-text content.

**Key responsibilities:**

- Validates that the file exists (`FileNotFoundError` otherwise).
- Validates that the file extension is supported (`ValueError` otherwise).
- Dispatches to the appropriate private reader method based on extension.

**Supported extensions and their private methods:**

| Extension | Private Method | External Library |
|---|---|---|
| `.txt` | `_read_txt()` | None |
| `.pdf` | `_read_pdf()` | `pypdf` |
| `.docx` | `_read_docx()` | `python-docx` |

The heavy-weight libraries (`pypdf`, `python-docx`) are imported lazily inside each method so that the agent can still process `.txt` files even if the optional libraries are not installed.

---

### `agent/extractor.py` – `Extractor`

Responsible for all LLM-powered operations on the extracted text.

**Key responsibilities:**

- Wraps raw text in a `langchain.docstore.document.Document` object.
- Loads and runs the appropriate LangChain chain.
- Returns the model's response as a plain string.

**Methods:**

| Method | Chain Used | Purpose |
|---|---|---|
| `summarize(content)` | `load_summarize_chain` (stuff) | Produces a concise summary |
| `answer_question(content, question)` | `load_qa_chain` (stuff) | Answers a specific question |

Both methods import `langchain` and `langchain-openai` lazily so that `ImportError` messages are descriptive.

---

### `agent/__init__.py`

Package marker file. Contains the package docstring and no other logic.

---

## Design Decisions

### Lazy Imports

Optional heavy dependencies (`pypdf`, `python-docx`, `langchain`, `langchain-openai`) are imported inside the methods that use them rather than at the top of each module. This allows the agent to start and validate arguments before failing on a missing optional library, and produces clear, actionable error messages.

### "Stuff" Chain Type

Both LangChain chains use `chain_type="stuff"`, which concatenates all document text into a single prompt. This is the simplest approach and works well for documents that fit within the model's context window. For very large documents a `map_reduce` or `refine` chain type may be more appropriate.

### Stateless Classes

`DocumentReader` and `Extractor` hold no instance state between calls, making them simple to instantiate and easy to test or reuse in different contexts.
