# Document Reading Agent

An AI-powered agent for reading, parsing, and extracting information from documents.

## Features

- Read and parse various document formats (PDF, DOCX, XLSX, TXT)
- Extract key information using AI/LLM capabilities
- Summarize document content
- Answer questions based on document content
- **Compare multiple construction/bid documents** (specification, scope of work, bid form) and produce a structured analysis including:
  - Differences between what each document says
  - Clarifying questions the bidder should ask before submitting
  - Suggested inclusions, exclusions, and clarifications for the final bid submittal

## Getting Started

### Prerequisites

- Python 3.9+
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
```

#### Comparison mode

Pass two or more documents to compare them and generate a bid analysis:

```bash
python main.py \
  --document spec.pdf \
  --document scope_of_work.pdf \
  --document bid_form.xlsx
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
    ├── reader.py       # Reads PDF, DOCX, XLSX, TXT files
    ├── extractor.py    # Single-document summarization & Q&A
    └── comparator.py   # Multi-document comparison & bid analysis
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

MIT
