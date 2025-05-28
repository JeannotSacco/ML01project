# ML01project
## Overview

**Video Subtitle Translator** is a Python-based application that takes a video—either from a YouTube link or an MP4 file—and automatically adds translated subtitles in either French or English. It uses state-of-the-art AI models and libraries to generate high-quality subtitles and embed them directly into the video.

## Features

- Supports input via YouTube link or local MP4 file
- Automatic speech transcription using OpenAI Whisper
- Subtitle enhancement and foreign language detection
- Automatic translation between English and French
- Embeds subtitles into the video file
- Graphical user interface for ease of use

## How It Works

1. **Launch** the application by running `/code/main.py`.
2. A **GUI** opens allowing the user to input either:
   - A **YouTube URL**
   - A **local MP4 file**
3. On clicking **Submit**:
   - If the input is a YouTube URL, the video is downloaded using `subprocess`.
   - The process then continues as if a local MP4 file had been used.
4. The video is transcribed into an `.srt` subtitle file using **OpenAI Whisper**.
5. The subtitles are then **enhanced**:
   - Quality improvements are applied.
   - Foreign language passages are detected and replaced with `[Foreign]` using **Googletrans**.
6. The enhanced subtitles are then **translated** into the target language.
7. Finally, the `add_subtitles_to_video` function generates a new video file named `videoavecsrt.mp4` in the `dynamicsrt` directory, with the translated subtitles embedded.

## Installation

1. Clone the repository.
2. Install required Python packages.
3. Run the app:
   ```bash
   python /code/main.py

## Requirements

- Python 3.x
- OpenAI Whisper
- googletrans
- subprocess (standard library)
- Tkinter
- ffmeg

## Project Structure  
/ mL01
├── code/
│ └── main.py # Main script to launch the application
├── dynamicsrt/
│ ├── addsrt.py # Module to add subtitles to videos
│ └── videoavecsrt # Output video file with embedded subtitles
├── improved_srt/
│ ├── improve.py # Module to clean and improve subtitle files
│ └── subtitles.srt # Subtitle file before translation
├── transcription/
│ ├── transcrpt.py # Module for transcribing audio/video to subtitles
│ └── video.mp4 # Sample video file used for transcription
├── translated_srt/
│ ├── translate.py # Module to translate subtitle files
│ └── translated.srt # Translated subtitle file
├── youtube_url/
│ ├── urltomp4.py # Module to download YouTube videos as mp4
│ └── video.mp4 # Downloaded YouTube video file
└── README.md # Project documentation
