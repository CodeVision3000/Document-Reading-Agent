"""
Document Reading Agent - Main entry point
"""
import argparse
import os
from agent.reader import DocumentReader
from agent.extractor import Extractor
from agent.comparator import DocumentComparator
from agent.knowledge_base import KnowledgeBase
from agent.speech import SpeechProcessor


def _label_for(path: str) -> str:
    """Return a human-readable label for a document based on its file name."""
    return os.path.basename(path)


def _load_documents(reader: DocumentReader, paths: list[str]) -> dict[str, str]:
    doc_contents: dict[str, str] = {}
    for path in paths:
        content = reader.read(path)
        label = _label_for(path)
        doc_contents[label] = content
        print(f"Loaded '{label}': {len(content)} characters")
    return doc_contents


def _resolve_query(
    args: argparse.Namespace,
    speech: SpeechProcessor | None,
    *,
    allow_text_query: bool = True,
) -> str | None:
    if args.audio_query:
        if speech is None:
            speech = SpeechProcessor(
                transcription_model=args.stt_model,
                speech_model=args.tts_model,
                voice=args.tts_voice,
            )
        query = speech.transcribe_file(args.audio_query)
        print(f"Transcribed query: {query}")
        return query

    return args.query if allow_text_query else None


def _emit_speech(args: argparse.Namespace, speech: SpeechProcessor | None, text: str) -> None:
    if not args.tts_output:
        return

    if speech is None:
        speech = SpeechProcessor(
            transcription_model=args.stt_model,
            speech_model=args.tts_model,
            voice=args.tts_voice,
        )

    output_path = speech.synthesize_to_file(text, args.tts_output)
    print(f"\nAudio saved to: {output_path}")


def _format_kb_context(results: list[dict]) -> str:
    if not results:
        return "No matching knowledge-base passages found."

    return "\n\n".join(
        f"Source: {item['source']} (chunk {item['chunk_index']}, score={item['score']:.3f})\n{item['content']}"
        for item in results
    )


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
    parser.add_argument("--audio-query", help="Optional audio file containing a spoken question")
    parser.add_argument("--transcribe-audio", metavar="PATH", help="Transcribe an audio file and exit")
    parser.add_argument("--create-knowledge-base", metavar="PATH", help="Write a document knowledge base to this JSON file")
    parser.add_argument("--knowledge-base", metavar="PATH", help="Path to an existing knowledge base JSON file")
    parser.add_argument("--kb-query", help="Question to answer from a knowledge base")
    parser.add_argument("--kb-top-k", type=int, default=4, help="How many knowledge-base chunks to retrieve (default: 4)")
    parser.add_argument("--tts-output", metavar="PATH", help="Optional audio file path for spoken output")
    parser.add_argument("--tts-voice", default="alloy", help="Voice to use for text-to-speech output")
    parser.add_argument("--tts-model", default="tts-1", help="Model to use for text-to-speech output")
    parser.add_argument("--stt-model", default="whisper-1", help="Model to use for speech-to-text input")
    args = parser.parse_args()

    if args.transcribe_audio:
        if any([args.documents, args.query, args.audio_query, args.create_knowledge_base, args.knowledge_base, args.kb_query]):
            parser.error("--transcribe-audio must be used on its own.")
        transcript = SpeechProcessor(
            transcription_model=args.stt_model,
            speech_model=args.tts_model,
            voice=args.tts_voice,
        ).transcribe_file(args.transcribe_audio)
        print(f"Transcript:\n{transcript}")
        return

    if not args.documents and not args.knowledge_base:
        parser.error("Provide at least one --document argument or a --knowledge-base path.")

    if args.query and args.audio_query:
        parser.error("Use either --query or --audio-query, not both.")

    if args.kb_query and not (args.knowledge_base or args.create_knowledge_base):
        parser.error("--kb-query requires --knowledge-base or --create-knowledge-base.")

    if args.query and (args.knowledge_base or args.create_knowledge_base):
        parser.error("--query is only supported in single-document mode. Use --kb-query for knowledge-base questions.")

    if args.knowledge_base and args.documents and not args.create_knowledge_base:
        parser.error("--knowledge-base cannot be combined with --document unless you are also creating a knowledge base.")

    reader = DocumentReader()
    speech = None
    if args.audio_query or args.tts_output:
        speech = SpeechProcessor(
            transcription_model=args.stt_model,
            speech_model=args.tts_model,
            voice=args.tts_voice,
        )

    doc_contents: dict[str, str] = {}
    if args.documents:
        doc_contents = _load_documents(reader, args.documents)

    if args.create_knowledge_base:
        kb = KnowledgeBase()
        build_result = kb.build(doc_contents, args.create_knowledge_base)
        print(
            "Knowledge base saved to "
            f"{build_result['output_path']} "
            f"with {build_result['chunk_count']} chunks "
            f"({'with embeddings' if build_result['embeddings_added'] else 'lexical only'})."
        )

        kb_query = args.kb_query or _resolve_query(args, speech, allow_text_query=False)
        if not kb_query:
            return

        results = kb.search(build_result["output_path"], kb_query, top_k=args.kb_top_k)
        context = _format_kb_context(results)
        print(f"\nKnowledge base query: {kb_query}")
        print(f"\nTop knowledge base matches:\n{context}")

        try:
            answer = Extractor().answer_question(context, kb_query)
            print(f"\nAnswer: {answer}")
            _emit_speech(args, speech, answer)
        except Exception as exc:
            print(f"\nLLM answer unavailable ({exc}). Showing retrieved knowledge-base passages only.")
            _emit_speech(args, speech, context)
        return

    if args.knowledge_base:
        kb_query = args.kb_query or _resolve_query(args, speech, allow_text_query=False)
        if not kb_query:
            parser.error("A query is required when using --knowledge-base.")

        results = KnowledgeBase().search(args.knowledge_base, kb_query, top_k=args.kb_top_k)
        context = _format_kb_context(results)
        print(f"Knowledge base query: {kb_query}")
        print(f"\nTop knowledge base matches:\n{context}")

        try:
            answer = Extractor().answer_question(context, kb_query)
            print(f"\nAnswer: {answer}")
            _emit_speech(args, speech, answer)
        except Exception as exc:
            print(f"\nLLM answer unavailable ({exc}). Showing retrieved knowledge-base passages only.")
            _emit_speech(args, speech, context)
        return

    query = _resolve_query(args, speech)

    # ------------------------------------------------------------------
    # Comparison mode – two or more documents supplied
    # ------------------------------------------------------------------
    if len(args.documents) >= 2:
        if query:
            parser.error("--query and --audio-query are not supported in comparison mode.")

        print("\nComparing documents…\n")
        comparator = DocumentComparator()
        result = comparator.compare(doc_contents)
        rendered = str(result)
        print(rendered)
        _emit_speech(args, speech, rendered)
        return

    # ------------------------------------------------------------------
    # Single-document mode
    # ------------------------------------------------------------------
    document_path = args.documents[0]
    content = doc_contents[_label_for(document_path)]
    print(f"Document ready: {len(content)} characters")

    extractor = Extractor()
    if query:
        answer = extractor.answer_question(content, query)
        print(f"\nAnswer: {answer}")
        _emit_speech(args, speech, answer)
    else:
        summary = extractor.summarize(content)
        print(f"\nSummary:\n{summary}")
        _emit_speech(args, speech, summary)


if __name__ == "__main__":
    main()
