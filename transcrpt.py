import whisper
from pathlib import Path

def transcript_mp4(chemin_mp4):
    model = whisper.load_model("base")
    video_path = chemin_mp4
    result = model.transcribe(video_path)
    segments = result["segments"]

    # Format timestamp to hh:mm:ss,ms (SRT format)
    def format_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

    # Define the output SRT path relative to this script
    output_path = Path(__file__).resolve().parents[1] / "improved_srt" / "subtitles.srt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    return f
