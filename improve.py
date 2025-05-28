import re
from langdetect import detect, DetectorFactory
from pathlib import Path

DetectorFactory.seed = 0  # Makes language detection deterministic

def clean_srt(input_file_path: str, output_file_path: str) -> None:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'\n\n+', content.strip())  # Each SRT block
    cleaned_blocks = []

    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) < 3:
            cleaned_blocks.append(block)
            continue

        index, time_range, *text_lines = lines
        text = " ".join(text_lines).strip()

        try:
            lang = detect(text)
        except:
            lang = "unknown"

        # Detect if the text is foreign, too short, or non-linguistic
        is_foreign = (
            lang not in ['en', 'fr'] or
            len(text) < 3 or
            re.fullmatch(r"[\W\d_]+", text)  # Only symbols or digits
        )

        if is_foreign:
            cleaned_blocks.append(f"{index}\n{time_range}\n[Foreign]")
        else:
            cleaned_blocks.append(f"{index}\n{time_range}\n" + "\n".join(text_lines))

    # Save the improved subtitle file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(cleaned_blocks))


# Define portable input/output paths relative to the project structure
project_root = Path(__file__).resolve().parents[1]
input_path = project_root / "improved_srt" / "subtitles.srt"
output_path = project_root / "improved_srt" / "subtitles.srt"

clean_srt(str(input_path), str(output_path))
