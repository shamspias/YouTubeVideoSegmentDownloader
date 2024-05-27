import tkinter as tk
from tkinter import filedialog, messagebox
from src.video_downloader import VideoDownloader
import os
from moviepy.editor import VideoFileClip


class VideoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Segment Downloader")

        # YouTube Video URL Entry
        tk.Label(root, text="YouTube Video URL:").pack(pady=10)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack(pady=10)

        # Radio Buttons for Selecting Download Mode
        self.download_mode = tk.StringVar(value="full")  # Default set to full download
        tk.Radiobutton(root, text="Download Full Video", variable=self.download_mode, value="full").pack()
        tk.Radiobutton(root, text="Download Specific Time Range", variable=self.download_mode, value="range").pack()

        # Time Range Entries (Initially disabled, enabled only for specific time range)
        self.start_time_entry = tk.Entry(root, width=20, state='disabled')
        self.end_time_entry = tk.Entry(root, width=20, state='disabled')

        # Enable time entries only if the specific time range is selected
        def enable_time_entries():
            if self.download_mode.get() == 'range':
                self.start_time_entry.config(state='normal')
                self.end_time_entry.config(state='normal')
            else:
                self.start_time_entry.config(state='disabled')
                self.end_time_entry.config(state='disabled')

        # Updating entry fields based on radio button change
        self.download_mode.trace_add('write', lambda *args: enable_time_entries())

        tk.Label(root, text="Start Time (H:M:S, optional):").pack(pady=5)
        self.start_time_entry.pack(pady=5)

        tk.Label(root, text="End Time (H:M:S, optional):").pack(pady=5)
        self.end_time_entry.pack(pady=5)

        # Download Button
        self.download_button = tk.Button(root, text="Download Video", command=self.process_video)
        self.download_button.pack(pady=20)

    def process_video(self):
        url = self.url_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

        if not save_path:
            return

        downloader = VideoDownloader(url)
        if self.download_mode.get() == "full":
            downloader.download_video(full_download=True)
            os.rename(downloader.video_path, save_path)
            messagebox.showinfo("Success", f"Full video has been saved to {save_path}")
        else:
            downloader.download_video(full_download=False)
            if not start_time:
                start_time = "0:0:0"
            if not end_time:
                video = VideoFileClip(downloader.video_path)
                end_time = str(int(video.duration))
                video.close()
            downloader.cut_video(start_time, end_time, save_path)
            messagebox.showinfo("Success",
                                f"Video segment from {start_time} to {end_time} has been saved to {save_path}")
