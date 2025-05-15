from pathlib import Path

from moviepy import VideoFileClip

from ..model.video import Video


class ExtractAudioService:
    def execute(video: Video):
        audio_output_path = Path(f"output/{video.name}.mp3")
        audio_output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            video = VideoFileClip(video.path)
            audio = video.audio
            audio.write_audiofile(str(audio_output_path))

        except Exception as e:
            raise Exception(f"Error: Unable to extract audio: {e}")
