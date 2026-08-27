"""Voice pipeline — mic → STT → NEXUS → TTS → speaker (all local)."""

class VoicePipeline:
    def transcribe(self, audio_path: str) -> str:
        # stub: whisper.cpp
        return "transcribed text"

    def synthesize(self, text: str, out_path: str = "out.wav") -> str:
        # stub: Piper / Kokoro
        return out_path
