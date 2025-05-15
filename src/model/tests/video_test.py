from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from ..video import Video


@pytest.fixture
def create_temp_video_file():
    with NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    yield temp_path

    temp_path.unlink(missing_ok=True)


@pytest.fixture
def create_wrong_temp_video_file():
    with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    yield temp_path

    temp_path.unlink(missing_ok=True)


class TestVideoModel:

    def test_it_should_be_able_to_create_a_video(self, create_temp_video_file):
        video_path = create_temp_video_file

        video = Video(video_path=video_path)

        assert video.name == video_path.stem
        assert video.format == video_path.suffix

    def test_it_should_raise_invalid_video_format_error(
        self, create_wrong_temp_video_file
    ):
        invalid_video_path = create_wrong_temp_video_file

        with pytest.raises(ValueError) as e:
            video = Video(video_path=invalid_video_path)

        assert str(e.value) == f"Invalid video format: {invalid_video_path.suffix}"
