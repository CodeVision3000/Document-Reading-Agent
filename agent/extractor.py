"""
Extractor module - handles summarization and Q&A using LLM
"""


class Extractor:
    """Extracts insights from document content using an LLM."""

    def summarize(self, content: str) -> str:
        """
        Summarize the given document content.

        Args:
            content: The text content of the document.

        Returns:
            A summary of the document.
        """
        try:
            from langchain.chains.summarize import load_summarize_chain
            from langchain_openai import ChatOpenAI
            from langchain.docstore.document import Document

            llm = ChatOpenAI(temperature=0)
            chain = load_summarize_chain(llm, chain_type="stuff")
            docs = [Document(page_content=content)]
            return chain.invoke({"input_documents": docs})["output_text"]
        except ImportError:
            raise ImportError("langchain and langchain-openai are required. Install with: pip install langchain langchain-openai")

    def answer_question(self, content: str, question: str) -> str:
        """
        Answer a question based on the document content.

        Args:
            content: The text content of the document.
            question: The question to answer.

        Returns:
            The answer to the question.
        """
        try:
            from langchain_openai import ChatOpenAI
            from langchain.chains.question_answering import load_qa_chain
            from langchain.docstore.document import Document

            llm = ChatOpenAI(temperature=0)
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = [Document(page_content=content)]
            return chain.invoke({"input_documents": docs, "question": question})["output_text"]
        except ImportError:
            raise ImportError("langchain and langchain-openai are required. Install with: pip install langchain langchain-openai")
