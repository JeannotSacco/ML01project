import subprocess
import os
from pathlib import Path

def telecharger_video_youtube(url):
    # Define the current directory where this script is located
    folder = Path(__file__).resolve().parent
    filename = "video.mp4"
    output_path = folder / filename

    os.makedirs(folder, exist_ok=True)

    # Delete the file if it already exists
    if output_path.exists():
        os.remove(output_path)

    try:
        print("Downloading...")
        subprocess.run([
            'yt-dlp',
            '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            '-o', str(output_path),
            url
        ], check=True)
        print(f"Download completed: {output_path}")
    except subprocess.CalledProcessError as e:
        print("An error occurred during download:", e
