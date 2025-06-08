from pathlib import Path

from moviepy import VideoFileClip


class Video:
    def __init__(self, video_path: Path):
        self.path = str(video_path)
        self.name = video_path.stem
        self.format = video_path.suffix
        self.size = video_path.stat().st_size  # Size in bytes
        self.duration = None

        self.__is_valid_format()
        self.__calc_video_duration()

    def __is_valid_format(self) -> bool:
        valid_formats = [".mp4", ".avi", ".mov", ".mkv"]

        if self.format not in valid_formats:
            raise ValueError(f"Invalid video format: {self.format}")

        return True

    def __calc_video_duration(self):
        try:
            with VideoFileClip(self.path) as video_clip:
                self.duration = video_clip.duration
        except Exception as e:
            raise IOError(f"Could not read video file to get duration: {e}")
