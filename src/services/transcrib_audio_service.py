from pathlib import Path

from faster_whisper import WhisperModel


class TranscribAudioService:
    def execute(audio_path: Path, whisper_model: str) -> dict[str, str | list]:
        model = WhisperModel(whisper_model, device="cpu", compute_type="int8")
        print(f"echosub - whisper model {whisper_model} loaded!")

        transcript_result = {"segments": []}

        try:
            print("echosub - Starting trascription")
            segments, transcript_info = model.transcribe(
                str(audio_path), word_timestamps=True
            )

            for segment in segments:
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s]: {segment.text}")

                segment_dict = {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "words": [word._asdict() for word in segment.words],
                }

                transcript_result["segments"].append(segment_dict)

            print("echosub - Transcription generated successfully! \n")

            audio_path.unlink()  # remove o audio

        except Exception as e:
            raise Exception(f"Error: Unable to generate trascription \n {e}")

        return transcript_result
