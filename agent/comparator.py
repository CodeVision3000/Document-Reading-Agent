"""
Comparator module - compares multiple construction/bid documents and generates
a structured analysis with differences, questions, and bid recommendations.
"""
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ComparisonResult:
    """Structured result returned by DocumentComparator.compare()."""

    differences: List[str] = field(default_factory=list)
    questions: List[str] = field(default_factory=list)
    inclusions: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)
    clarifications: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        sections = []

        sections.append("=== DOCUMENT COMPARISON ANALYSIS ===\n")

        sections.append("--- DIFFERENCES BETWEEN DOCUMENTS ---")
        if self.differences:
            for item in self.differences:
                sections.append(f"  • {item}")
        else:
            sections.append("  No significant differences found.")

        sections.append("\n--- QUESTIONS TO ASK FOR MORE INFORMATION ---")
        if self.questions:
            for item in self.questions:
                sections.append(f"  • {item}")
        else:
            sections.append("  No questions generated.")

        sections.append("\n--- SUGGESTED INCLUSIONS FOR BID SUBMITTAL ---")
        if self.inclusions:
            for item in self.inclusions:
                sections.append(f"  • {item}")
        else:
            sections.append("  No inclusions suggested.")

        sections.append("\n--- SUGGESTED EXCLUSIONS FOR BID SUBMITTAL ---")
        if self.exclusions:
            for item in self.exclusions:
                sections.append(f"  • {item}")
        else:
            sections.append("  No exclusions suggested.")

        sections.append("\n--- SUGGESTED CLARIFICATIONS FOR BID SUBMITTAL ---")
        if self.clarifications:
            for item in self.clarifications:
                sections.append(f"  • {item}")
        else:
            sections.append("  No clarifications suggested.")

        return "\n".join(sections)


class DocumentComparator:
    """
    Compares multiple documents (e.g. a specification PDF, a scope-of-work PDF,
    and an XLSX bid form) and produces a structured analysis containing:

    - Differences between what each document describes
    - Questions the user should ask to obtain missing or conflicting information
    - Suggested inclusions, exclusions, and clarifications for the final bid submittal

    Args:
        max_chars_per_doc: Maximum number of characters to send to the LLM for each
            document. Documents that exceed this limit are truncated with a notice.
            Defaults to 12000 characters (~3000 tokens), which keeps the combined
            prompt well within GPT-4o's context window for typical bid documents.
    """

    _COMPARISON_PROMPT = """You are a construction bid analyst. You have been given {n} documents:

{documents}

Analyze these documents and respond with a JSON object that has exactly the following keys:
- "differences": a list of strings describing meaningful differences or conflicts between what the documents say
- "questions": a list of strings with clarifying questions the bidder should ask before submitting
- "inclusions": a list of strings for items that should be explicitly included in the bid
- "exclusions": a list of strings for items that should be explicitly excluded from the bid
- "clarifications": a list of strings for clarifying statements the bidder should include in the bid submittal

Be thorough but concise. Return ONLY valid JSON, no additional text."""

    def __init__(self, max_chars_per_doc: int = 12_000) -> None:
        self.max_chars_per_doc = max_chars_per_doc

    def compare(self, documents: Dict[str, str]) -> ComparisonResult:
        """
        Compare two or more documents and return a structured analysis.

        Args:
            documents: A mapping of document label (e.g. file name or role such as
                       "Specification", "Scope of Work", "Bid Form") to its text content.

        Returns:
            A :class:`ComparisonResult` with differences, questions, inclusions,
            exclusions, and clarifications.

        Raises:
            ValueError: If fewer than two documents are provided.
        """
        if len(documents) < 2:
            raise ValueError("At least two documents are required for comparison.")

        doc_sections_parts = []
        for i, (label, content) in enumerate(documents.items()):
            if len(content) > self.max_chars_per_doc:
                content = (
                    content[: self.max_chars_per_doc]
                    + f"\n[... content truncated to {self.max_chars_per_doc} characters ...]"
                )
            doc_sections_parts.append(f"Document {i + 1} - {label}:\n{content}")

        doc_sections = "\n\n".join(doc_sections_parts)

        prompt = self._COMPARISON_PROMPT.format(
            n=len(documents),
            documents=doc_sections,
        )

        raw = self._call_llm(prompt)
        return self._parse_response(raw)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        try:
            from langchain_openai import ChatOpenAI
            from langchain.schema import HumanMessage

            llm = ChatOpenAI(temperature=0, model="gpt-4o")
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except ImportError:
            raise ImportError(
                "langchain and langchain-openai are required. "
                "Install with: pip install langchain langchain-openai"
            )

    def _parse_response(self, raw: str) -> ComparisonResult:
        import json
        import re

        # Strip markdown code fences if present
        cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip(), flags=re.MULTILINE)
        cleaned = re.sub(r"\s*```$", "", cleaned.strip(), flags=re.MULTILINE)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM returned a response that could not be parsed as JSON.\n"
                f"Raw response:\n{raw}"
            ) from exc

        return ComparisonResult(
            differences=data.get("differences", []),
            questions=data.get("questions", []),
            inclusions=data.get("inclusions", []),
            exclusions=data.get("exclusions", []),
            clarifications=data.get("clarifications", []),
        )
