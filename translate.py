import os
import re
from googletrans import Translator
from langdetect import detect
from pathlib import Path

def process_and_translate_srt(input_file_path, output_file_path, num_chars=1000):
    # Detect the language from a portion of the subtitle file
    text = ""
    with open(input_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.isdigit() and '-->' not in line:
                text += line + " "
            if len(text) >= num_chars:
                break

    try:
        detected_lang = detect(text)
        if detected_lang.startswith('fr'):
            target_language = 'en'
        elif detected_lang.startswith('en'):
            target_language = 'fr'
        else:
            target_language = 'en'
    except Exception:
        target_language = 'en'

    # Translation
    translator = Translator()
    translated_lines = []

    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'\n\n+', content.strip())

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = lines[0]
            timecode = lines[1]
            text_lines = lines[2:]
            text = ' '.join(text_lines)

            try:
                translated = translator.translate(text, dest=target_language).text
            except Exception as e:
                print(f"Error during translation: {e}")
                translated = text

            translated_block = f"{index}\n{timecode}\n{translated}\n"
            translated_lines.append(translated_block)
        else:
            translated_lines.append('\n'.join(lines) + '\n')

    # Ensure the output directory exists and save the result
    output_dir = Path(output_file_path).parent
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(translated_lines))
