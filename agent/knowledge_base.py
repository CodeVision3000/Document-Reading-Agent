"""
Knowledge-base helpers for chunking documents, storing them, and retrieving
relevant passages for later question answering.
"""
from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path
from typing import Dict, List


class KnowledgeBase:
    """Creates and queries lightweight document knowledge bases."""

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 200,
        embedding_model: str = "text-embedding-3-small",
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = embedding_model

    def build(self, documents: Dict[str, str], output_path: str) -> dict:
        if not documents:
            raise ValueError("At least one document is required to build a knowledge base.")

        records: List[dict] = []
        for source, content in documents.items():
            for index, chunk in enumerate(self._chunk_text(content)):
                records.append(
                    {
                        "id": f"{source}:{index}",
                        "source": source,
                        "chunk_index": index,
                        "content": chunk,
                    }
                )

        if not records:
            raise ValueError("No text chunks were produced from the supplied documents.")

        embeddings_added = self._attach_embeddings(records)
        payload = {
            "embedding_model": self.embedding_model if embeddings_added else None,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "documents": list(documents.keys()),
            "chunks": records,
        }

        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        return {
            "output_path": str(destination),
            "chunk_count": len(records),
            "embeddings_added": embeddings_added,
        }

    def search(self, kb_path: str, query: str, top_k: int = 4) -> List[dict]:
        if not query.strip():
            raise ValueError("A non-empty query is required.")

        payload = self.load(kb_path)
        chunks = payload.get("chunks", [])
        if not chunks:
            return []

        has_embeddings = any(chunk.get("embedding") for chunk in chunks[: min(len(chunks), 10)])
        if payload.get("embedding_model") and has_embeddings:
            try:
                query_embedding = self._embed_texts([query])[0]
                return self._semantic_search(chunks, query_embedding, top_k)
            except Exception:
                pass

        return self._lexical_search(chunks, query, top_k)

    def load(self, kb_path: str) -> dict:
        kb_file = Path(kb_path)
        if not kb_file.exists():
            raise FileNotFoundError(f"Knowledge base not found: {kb_path}")
        return json.loads(kb_file.read_text(encoding="utf-8"))

    def _attach_embeddings(self, records: List[dict]) -> bool:
        if not os.getenv("OPENAI_API_KEY"):
            return False

        try:
            embeddings = self._embed_texts([record["content"] for record in records])
        except Exception:
            return False

        for record, embedding in zip(records, embeddings):
            record["embedding"] = embedding
        return True

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        from openai import OpenAI

        response = OpenAI().embeddings.create(
            model=self.embedding_model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    def _semantic_search(self, chunks: List[dict], query_embedding: List[float], top_k: int) -> List[dict]:
        scored = []
        query_norm = math.sqrt(sum(value * value for value in query_embedding))
        for chunk in chunks:
            embedding = chunk.get("embedding")
            if not embedding:
                continue
            score = self._cosine_similarity(query_embedding, query_norm, embedding)
            scored.append({**chunk, "score": score})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def _lexical_search(self, chunks: List[dict], query: str, top_k: int) -> List[dict]:
        scored = []
        query_terms = self._tokenize(query)
        for chunk in chunks:
            score = self._keyword_overlap_score(query_terms, chunk["content"])
            scored.append({**chunk, "score": score})

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def _keyword_overlap_score(self, query_terms: List[str], content: str) -> float:
        if not query_terms:
            return 0.0

        content_terms = self._tokenize(content)
        if not content_terms:
            return 0.0

        content_vocab = set(content_terms)
        matches = sum(1 for term in query_terms if term in content_vocab)
        return matches / len(set(query_terms))

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def _chunk_text(self, text: str) -> List[str]:
        cleaned = text.strip()
        if not cleaned:
            return []

        chunks = []
        start = 0
        text_length = len(cleaned)

        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            if end < text_length:
                split_at = cleaned.rfind(" ", start, end)
                if split_at > start:
                    end = split_at

            chunk = cleaned[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end >= text_length:
                break

            next_start = max(end - self.chunk_overlap, start + 1)
            start = next_start

        return chunks

    def _cosine_similarity(self, left: List[float], left_norm: float, right: List[float]) -> float:
        numerator = sum(a * b for a, b in zip(left, right))
        right_norm = math.sqrt(sum(value * value for value in right))
        if not left_norm or not right_norm:
            return 0.0
        return numerator / (left_norm * right_norm)
