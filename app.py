from src.services.extract_audio_service import ExtractAudioService
from src.services.generate_subtitle_service import GenerateSubtitleService
from src.services.load_video_file_service import LoadVideoFileService
from src.services.transcrib_audio_service import TranscribAudioService

video = LoadVideoFileService().execute("./videos/video.mp4")
audio = ExtractAudioService.execute(video)
transcription = TranscribAudioService.execute(audio)

GenerateSubtitleService().execute(video=video, transcript=transcription)
