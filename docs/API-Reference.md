# API Reference

Detailed documentation for every public class and method in the Document Reading Agent codebase.

---

## `agent.reader.DocumentReader`

Reads documents of various formats and returns their plain-text content.

```python
from agent.reader import DocumentReader
```

### Class Attributes

| Attribute | Type | Value | Description |
|---|---|---|---|
| `SUPPORTED_EXTENSIONS` | `set[str]` | `{".txt", ".pdf", ".docx"}` | The set of file extensions the reader accepts |

---

### `DocumentReader.read(file_path)`

Read a document and return its full text content.

**Signature**

```python
def read(self, file_path: str) -> str
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `file_path` | `str` | Absolute or relative path to the document file |

**Returns**

`str` – The complete text content extracted from the document.

**Raises**

| Exception | Condition |
|---|---|
| `FileNotFoundError` | The file at `file_path` does not exist |
| `ValueError` | The file extension is not in `SUPPORTED_EXTENSIONS` |
| `ImportError` | A required optional library (`pypdf` or `python-docx`) is not installed |

**Example**

```python
reader = DocumentReader()
text = reader.read("report.pdf")
print(f"Loaded {len(text)} characters")
```

---

### `DocumentReader._read_txt(file_path)`

*Private.* Reads a plain-text file using UTF-8 encoding.

```python
def _read_txt(self, file_path: str) -> str
```

---

### `DocumentReader._read_pdf(file_path)`

*Private.* Reads a PDF file using the `pypdf` library. Each page's text is joined with a newline.

```python
def _read_pdf(self, file_path: str) -> str
```

Raises `ImportError` if `pypdf` is not installed.

---

### `DocumentReader._read_docx(file_path)`

*Private.* Reads a `.docx` file using the `python-docx` library. Paragraph text is joined with a newline.

```python
def _read_docx(self, file_path: str) -> str
```

Raises `ImportError` if `python-docx` is not installed.

---

## `agent.extractor.Extractor`

Extracts insights from document content using an LLM via LangChain and the OpenAI API.

```python
from agent.extractor import Extractor
```

---

### `Extractor.summarize(content)`

Generate a concise summary of the provided document text.

**Signature**

```python
def summarize(self, content: str) -> str
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `content` | `str` | The full text content of the document |

**Returns**

`str` – An AI-generated summary of the document.

**Raises**

| Exception | Condition |
|---|---|
| `ImportError` | `langchain` or `langchain-openai` is not installed |

**Internals**

Uses `langchain.chains.summarize.load_summarize_chain` with `chain_type="stuff"` and `ChatOpenAI(temperature=0)`.

**Example**

```python
extractor = Extractor()
summary = extractor.summarize(document_text)
print(summary)
```

---

### `Extractor.answer_question(content, question)`

Answer a natural-language question using the document content as context.

**Signature**

```python
def answer_question(self, content: str, question: str) -> str
```

**Parameters**

| Parameter | Type | Description |
|---|---|---|
| `content` | `str` | The full text content of the document |
| `question` | `str` | The natural-language question to answer |

**Returns**

`str` – The LLM's answer to the question, grounded in the document.

**Raises**

| Exception | Condition |
|---|---|
| `ImportError` | `langchain` or `langchain-openai` is not installed |

**Internals**

Uses `langchain.chains.question_answering.load_qa_chain` with `chain_type="stuff"` and `ChatOpenAI(temperature=0)`.

**Example**

```python
extractor = Extractor()
answer = extractor.answer_question(document_text, "What is the conclusion?")
print(answer)
```

---

## `main` module

### `main()`

CLI entry point. Parses arguments, reads the document, and prints the summary or answer.

**Invoked via:**

```bash
python main.py --document <path> [--query <question>]
```

This function is not intended to be called programmatically; use `DocumentReader` and `Extractor` directly instead.
