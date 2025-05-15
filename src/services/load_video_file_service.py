from pathlib import Path

from ..model.video import Video


class LoadVideoFileService:
    def __init__(self):
        pass

    def execute(self, file_path: str) -> Video:
        video_path = Path(file_path)

        if not video_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        video = Video(video_path=video_path)

        return video
