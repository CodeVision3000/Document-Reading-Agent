"""
Document Reading Agent - Main entry point
"""
import argparse
from agent.reader import DocumentReader
from agent.extractor import Extractor


def main():
    parser = argparse.ArgumentParser(description="Document Reading Agent")
    parser.add_argument("--document", required=True, help="Path to the document to read")
    parser.add_argument("--query", help="Optional question to answer from the document")
    args = parser.parse_args()

    reader = DocumentReader()
    content = reader.read(args.document)
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
