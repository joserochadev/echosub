from pathlib import Path

from ..model.video import Video


class GenerateSubtitleService:
    def __init__(self):
        pass

    def __format_time(self, seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    def execute(self, video: Video, transcript: dict[str, str | list]):
        subtitle_path = Path(f"output/subtitle/[subtitle] - {video.name}.srt")
        subtitle_path.parent.mkdir(parents=True, exist_ok=True)

        with open(str(subtitle_path), "w", encoding="utf-8") as f:
            for i, segment in enumerate(transcript["segments"], 1):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                f.write(f"{i}\n")
                f.write(f"{self.__format_time(start)} --> {self.__format_time(end)}\n")
                f.write(f"{text}\n\n")
