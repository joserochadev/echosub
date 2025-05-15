from pathlib import Path

import whisper


class TranscribAudioService:
    def execute(audio_path: Path) -> dict[str, str | list]:
        model = whisper.load_model("tiny")
        print("echosub - whisper model Tiny loaded!")

        try:
            print("echosub - Starting trascription")
            transcript = model.transcribe(str(audio_path), verbose=False)

            print("echosub - Transcription generated successfully! \n")

        except Exception as e:
            raise Exception(f"Error: Unable to generate trascription \n {e}")

        for segment in transcript["segments"]:
            print(
                f"[{segment['start']:.2f}s -> {segment['end']:.2f}s]: {segment['text']}"
            )

        return transcript
