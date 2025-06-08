import os
from pathlib import Path

from moviepy import VideoFileClip

from ..model.video import Video


class ExtractAudioService:
    def execute(video: Video) -> Path:
        audio_output_path = Path(f"output/{video.name}.wav")
        audio_output_path.parent.mkdir(parents=True, exist_ok=True)
        num_threads = os.cpu_count()  # quantidade de threads da cpu

        try:
            print(f"echosub - Extracting audio using {num_threads} threads...")

            video = VideoFileClip(video.path)
            audio = video.audio
            audio.write_audiofile(
                str(audio_output_path),
                bitrate="128k",
                ffmpeg_params=["-preset", "ultrafast", "-threads", str(num_threads)],
            )

            print("echosub - Audio extracted successfully! \n")

            return audio_output_path

        except Exception as e:
            raise Exception(f"Error: Unable to extract audio: {e}")
