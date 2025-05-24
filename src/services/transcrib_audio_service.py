from pathlib import Path

import whisper


class TranscribAudioService:
    def execute(audio_path: Path, whisper_model: str) -> dict[str, str | list]:
        model = whisper.load_model(whisper_model)
        print(f"echosub - whisper model {whisper_model} loaded!")

        try:
            print("echosub - Starting trascription")
            transcript = model.transcribe(
                str(audio_path), verbose=False, word_timestamps=True
            )

            print("echosub - Transcription generated successfully! \n")

            audio_path.unlink()  # remove o audio

        except Exception as e:
            raise Exception(f"Error: Unable to generate trascription \n {e}")

        for segment in transcript["segments"]:
            print(
                f"[{segment['start']:.2f}s -> {segment['end']:.2f}s]: {segment['text']}"
            )

        return transcript
