# Document Reading Agent

An AI-powered agent for reading, parsing, and extracting information from documents.

## Features

- Read and parse various document formats (PDF, DOCX, XLSX, TXT)
- Prefer Docling for richer PDF, DOCX, and XLSX parsing with safe fallback readers
- Extract key information using AI/LLM capabilities
- Summarize document content
- Answer questions based on document content
- Transcribe spoken questions from audio files
- Generate spoken audio responses for summaries, answers, and comparisons
- Create a reusable knowledge base from one or more documents and query it later
- **Compare multiple construction/bid documents** (specification, scope of work, bid form) and produce a structured analysis including:
  - Differences between what each document says
  - Clarifying questions the bidder should ask before submitting
  - Suggested inclusions, exclusions, and clarifications for the final bid submittal

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- An OpenAI API key set in the environment variable `OPENAI_API_KEY`

### Installation

```bash
pip install -r requirements.txt
```

### Usage

#### Single-document mode

Summarize a document or answer a question about it:

```bash
# Summarize
python main.py --document <path-to-document>

# Answer a specific question
python main.py --document <path-to-document> --query "What are the payment terms?"

# Ask a spoken question from an audio file
python main.py --document <path-to-document> --audio-query question.wav

# Save a spoken answer to an MP3 file
python main.py --document <path-to-document> --query "What are the payment terms?" --tts-output answer.mp3
```

#### Comparison mode

Pass two or more documents to compare them and generate a bid analysis:

```bash
python main.py \
  --document spec.pdf \
  --document scope_of_work.pdf \
  --document bid_form.xlsx
```

#### Speech-only transcription

Convert an audio file to text:

```bash
python main.py --transcribe-audio meeting_question.wav
```

#### Knowledge-base mode

Build a reusable knowledge base JSON file from one or more documents:

```bash
python main.py \
  --document spec.pdf \
  --document scope_of_work.pdf \
  --create-knowledge-base kb/project_bid.json
```

Query an existing knowledge base:

```bash
python main.py \
  --knowledge-base kb/project_bid.json \
  --kb-query "Which scope items are excluded?"
```

Build and query a knowledge base in one step, then save the spoken answer:

```bash
python main.py \
  --document spec.pdf \
  --document scope_of_work.pdf \
  --create-knowledge-base kb/project_bid.json \
  --audio-query question.wav \
  --tts-output answer.mp3
```

The agent will print a structured report containing:

- **Differences** – conflicts or gaps between what the documents describe
- **Questions** – items the bidder should clarify before submitting
- **Inclusions** – work that should be explicitly included in the bid
- **Exclusions** – work that should be explicitly excluded from the bid
- **Clarifications** – statements that should accompany the final bid submittal

## Project Structure

```
Document-Reading-Agent/
├── README.md
├── requirements.txt
├── main.py
└── agent/
    ├── __init__.py
    ├── reader.py          # Reads PDF, DOCX, XLSX, TXT files
    ├── extractor.py       # Single-document summarization & Q&A
    ├── comparator.py      # Multi-document comparison & bid analysis
    ├── knowledge_base.py  # Build/query reusable document knowledge bases
    └── speech.py          # Speech-to-text and text-to-speech helpers
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

MIT
