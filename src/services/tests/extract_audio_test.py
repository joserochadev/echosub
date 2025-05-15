from pathlib import Path

from model.video import Video

from ..extract_audio_service import ExtractAudioService


class TestExtractAudio:

    def test_it_should_extract_audio_sucessfully(self):
        real_video_path = Path("./videos/video_test.mp4").absolute()

        video = Video(real_video_path)

        output_audio_path = Path(f"output/{video.name}.mp3")

        if output_audio_path.exists():
            output_audio_path.unlink()

        ExtractAudioService.execute(video)

        assert output_audio_path.exists()
        assert output_audio_path.stat().st_size > 0
