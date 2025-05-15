import tempfile
from pathlib import Path

import pytest

from ..load_video_file_service import LoadVideoFileService


@pytest.fixture
def create_temp_video_file():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    yield temp_path

    temp_path.unlink(missing_ok=True)


class TestLoadVideoFile:

    def test_it_should_be_able_to_load_a_video_file(self, create_temp_video_file):
        video_path = create_temp_video_file

        service = LoadVideoFileService()
        video = service.execute(str(video_path))

        assert video.path == str(video_path)
        assert video.name == video_path.stem
        assert video.format == video_path.suffix
        assert video.size == video_path.stat().st_size

    def test_it_should_raise_file_not_found_error(self):
        service = LoadVideoFileService()
        invalid_path = "invalid_path.mp4"

        with pytest.raises(FileNotFoundError) as e:
            service.execute(invalid_path)

        assert str(e.value) == f"File not found: {invalid_path}"
