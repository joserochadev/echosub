from pathlib import Path


class Video:
    def __init__(self, video_path: Path):
        self.path = str(video_path)
        self.name = video_path.stem
        self.format = video_path.suffix
        self.size = video_path.stat().st_size  # Size in bytes

        self.__is_valid_format()

    def __is_valid_format(self) -> bool:
        valid_formats = [".mp4", ".avi", ".mov", ".mkv"]

        if self.format not in valid_formats:
            raise ValueError(f"Invalid video format: {self.format}")

        return True
