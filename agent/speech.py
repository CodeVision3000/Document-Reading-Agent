"""
Speech input/output helpers backed by the OpenAI audio APIs.
"""
from __future__ import annotations

import os
from pathlib import Path


class SpeechProcessor:
    """Transcribes audio files and generates spoken output."""

    def __init__(
        self,
        transcription_model: str = "whisper-1",
        speech_model: str = "tts-1",
        voice: str = "alloy",
    ) -> None:
        self.transcription_model = transcription_model
        self.speech_model = speech_model
        self.voice = voice

    def transcribe_file(self, file_path: str, model: str | None = None) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        from openai import OpenAI

        client = OpenAI()
        with open(file_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model=model or self.transcription_model,
                file=audio_file,
            )

        text = getattr(response, "text", "").strip()
        if not text:
            raise ValueError(f"No transcript returned for audio file: {file_path}")
        return text

    def synthesize_to_file(
        self,
        text: str,
        output_path: str,
        voice: str | None = None,
        model: str | None = None,
    ) -> str:
        if not text.strip():
            raise ValueError("Text-to-speech requires non-empty text.")

        from openai import OpenAI

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        client = OpenAI()
        response = client.audio.speech.create(
            model=model or self.speech_model,
            voice=voice or self.voice,
            input=text,
        )

        audio_content = getattr(response, "content", None)
        if audio_content is None and hasattr(response, "read"):
            audio_content = response.read()
        if not audio_content:
            raise ValueError("No audio bytes returned from text-to-speech request.")

        output.write_bytes(audio_content)
        return str(output)
