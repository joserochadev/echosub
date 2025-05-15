from src.services.load_video_file_service import LoadVideoFileService

video = LoadVideoFileService().execute("./videos/video.mp4")

print(f"Video Name: {video.name}")
