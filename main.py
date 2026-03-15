"""
Document Reading Agent - Main entry point
"""
import argparse
import os
from agent.reader import DocumentReader
from agent.extractor import Extractor
from agent.comparator import DocumentComparator


def _label_for(path: str) -> str:
    """Return a human-readable label for a document based on its file name."""
    return os.path.basename(path)


def main():
    parser = argparse.ArgumentParser(description="Document Reading Agent")
    parser.add_argument(
        "--document",
        action="append",
        dest="documents",
        metavar="PATH",
        help=(
            "Path to a document to read/compare. "
            "Supply once for single-document mode; "
            "supply two or more times (e.g. --document spec.pdf --document sow.pdf "
            "--document bid.xlsx) to enable comparison mode."
        ),
    )
    parser.add_argument("--query", help="Optional question to answer from the document (single-document mode only)")
    args = parser.parse_args()

    if not args.documents:
        parser.error("At least one --document argument is required.")

    reader = DocumentReader()

    # ------------------------------------------------------------------
    # Comparison mode – two or more documents supplied
    # ------------------------------------------------------------------
    if len(args.documents) >= 2:
        if args.query:
            parser.error("--query is not supported in comparison mode.")

        doc_contents: dict[str, str] = {}
        for path in args.documents:
            content = reader.read(path)
            label = _label_for(path)
            doc_contents[label] = content
            print(f"Loaded '{label}': {len(content)} characters")

        print("\nComparing documents…\n")
        comparator = DocumentComparator()
        result = comparator.compare(doc_contents)
        print(result)
        return

    # ------------------------------------------------------------------
    # Single-document mode
    # ------------------------------------------------------------------
    document_path = args.documents[0]
    content = reader.read(document_path)
    print(f"Document loaded: {len(content)} characters")

    extractor = Extractor()
    if args.query:
        answer = extractor.answer_question(content, args.query)
        print(f"\nAnswer: {answer}")
    else:
        summary = extractor.summarize(content)
        print(f"\nSummary:\n{summary}")


if __name__ == "__main__":
    main()
