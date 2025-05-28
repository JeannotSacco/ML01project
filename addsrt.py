import subprocess
import os
from pathlib import Path

def add_subtitles_to_video(video_path: str, subtitle_path: str, output_path: str = None):
    # Define default output path if not provided
    if output_path is None:
        output_path = Path(__file__).resolve().parents[1] / "dynamicsrt" / "videoavecsrt"
    else:
        output_path = Path(output_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"Subtitles not found: {subtitle_path}")

    try:
        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_path}",
            "-c:a", "copy",
            str(output_path)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("An error occurred while adding subtitles:")
        print(e)
