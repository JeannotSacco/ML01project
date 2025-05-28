import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import re
from pathlib import Path

from transcription.transcrpt import transcript_mp4
from youtube_url.urltomp4 import telecharger_video_youtube
from translated_srt.translate import process_and_translate_srt
from dynamicsrt.addsrt import add_subtitles_to_video
from improved_srt.improve import clean_srt

# Simple tkinter window
class InterfaceSRT:
    def __init__(self):
        self.chemin_mp4 = None

        self.fenetre = tk.Tk()
        self.fenetre.title("SRT Processing Tool")
        self.fenetre.geometry("750x400")
        self.fenetre.configure(bg="#f7f7f7")

        for i in range(4):
            self.fenetre.columnconfigure(i, weight=1)

        self.titre = tk.Label(self.fenetre, text="SRT Processing Tool", font=("Helvetica", 18, "bold"), bg="#f7f7f7", fg="#333")
        self.titre.grid(row=0, column=0, columnspan=4, pady=(20, 10))

        self.bouton_mp4 = tk.Button(self.fenetre, text="Choose a .mp4 file", command=self.choisir_fichier_mp4, bg="#d9eaf7", fg="#000", font=("Helvetica", 11), width=25)
        self.bouton_mp4.grid(row=1, column=0, columnspan=4, pady=(10, 5))

        self.label_fichier_mp4 = tk.Label(self.fenetre, text="No file selected", bg="#f7f7f7", fg="#666", font=("Helvetica", 10, "italic"))
        self.label_fichier_mp4.grid(row=2, column=0, columnspan=4, pady=(0, 15))

        self.label_url = tk.Label(self.fenetre, text="YouTube URL:", bg="#f7f7f7", font=("Helvetica", 11))
        self.label_url.grid(row=3, column=0, columnspan=1, sticky="e", padx=(20, 5))

        self.champ_url = tk.Entry(self.fenetre, font=("Helvetica", 11), width=40)
        self.champ_url.grid(row=3, column=1, columnspan=2, pady=5, sticky="w")

        self.bouton_submit = tk.Button(self.fenetre, text="Submit", command=self.traiter_entree, bg="#c8e6c9", fg="#000", font=("Helvetica", 11, "bold"), width=25)
        self.bouton_submit.grid(row=4, column=0, columnspan=4, pady=(20, 5))

        self.bouton_clear = tk.Button(self.fenetre, text="Cancel", command=self.clear, bg="#ffcdd2", fg="#000", font=("Helvetica", 11), width=25)
        self.bouton_clear.grid(row=5, column=0, columnspan=4, pady=5)

        # Define project root once
        self.project_root = Path(__file__).resolve().parents[0]

    def choisir_fichier_mp4(self):
        self.chemin_mp4 = filedialog.askopenfilename(title="Select an MP4 file", filetypes=[("MP4 files", "*.mp4")])
        if self.chemin_mp4:
            self.label_fichier_mp4.config(text=f"{self.chemin_mp4}")

    def traiter_entree(self):
        url = self.champ_url.get().strip()
        champs_remplis = sum(bool(x) for x in [self.chemin_mp4, url])

        if champs_remplis == 0:
            messagebox.showerror("Error", "Please provide one input (MP4 file or URL).")
            return
        if champs_remplis > 1:
            messagebox.showerror("Error", "Only one input should be provided at a time.")
            return

        try:
            if self.chemin_mp4:
                # Setup paths relative to project structure
                transcription_dir = self.project_root / "transcription"
                transcription_dir.mkdir(parents=True, exist_ok=True)
                video_dest = transcription_dir / "video.mp4"

                shutil.copy(self.chemin_mp4, video_dest)

                # Transcription to SRT
                transcript_mp4(str(video_dest))

                # Improve SRT
                improved_srt_path = self.project_root / "improved_srt" / "subtitles.srt"
                clean_srt(str(improved_srt_path), str(improved_srt_path))

                # Translate SRT
                translated_srt_path = self.project_root / "translated_srt" / "translated.srt"
                translated_srt_path.parent.mkdir(exist_ok=True)
                process_and_translate_srt(str(improved_srt_path), str(translated_srt_path))

                # Add subtitles to video
                output_video_path = self.project_root / "dynamicsrt" / "videoavecsrt.mp4"
                output_video_path.parent.mkdir(exist_ok=True)
                add_subtitles_to_video(str(video_dest), str(translated_srt_path), str(output_video_path))

                messagebox.showinfo("Success", f"Transcription completed.\nFile saved at: {output_video_path}")

            elif url:
                # Validate YouTube URL
                if not re.match(r'^https?://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}(&.*)?$', url):
                    messagebox.showerror("Error", "Please enter a valid YouTube URL.")
                    return

                # Download video
                telecharger_video_youtube(url)

                youtube_video_path = self.project_root / "youtube_url" / "video.mp4"
                # Transcription to SRT
                transcript_mp4(str(youtube_video_path))

                # Improve SRT
                improved_srt_path = self.project_root / "improved_srt" / "subtitles.srt"
                clean_srt(str(improved_srt_path), str(improved_srt_path))

                # Translate SRT
                translated_srt_path = self.project_root / "translated_srt" / "translated.srt"
                translated_srt_path.parent.mkdir(exist_ok=True)
                process_and_translate_srt(str(improved_srt_path), str(translated_srt_path))

                # Add subtitles to video
                output_video_path = self.project_root / "dynamicsrt" / "videoavecsrt.mp4"
                output_video_path.parent.mkdir(exist_ok=True)
                add_subtitles_to_video(str(youtube_video_path), str(translated_srt_path), str(output_video_path))

                messagebox.showinfo("Success", f"Transcription completed.\nFile saved at: {output_video_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during processing:\n{str(e)}")

    def clear(self):
        self.chemin_mp4 = None
        self.label_fichier_mp4.config(text="No file selected")
        self.champ_url.delete(0, tk.END)

    def afficher(self):
        self.fenetre.mainloop()


if __name__ == "__main__":
    app = InterfaceSRT()
    app.afficher()
