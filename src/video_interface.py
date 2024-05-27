import tkinter as tk
from tkinter import filedialog, messagebox
from src.video_downloader import VideoDownloader


class VideoInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Segment Downloader")
        tk.Label(root, text="YouTube Video URL:").pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()
        tk.Label(root, text="Start Time (H:M:S, optional):").pack()
        self.start_time_entry = tk.Entry(root, width=20)
        self.start_time_entry.pack()
        tk.Label(root, text="End Time (H:M:S, optional):").pack()
        self.end_time_entry = tk.Entry(root, width=20)
        self.end_time_entry.pack()
        self.download_button = tk.Button(root, text="Download Video", command=self.process_video)
        self.download_button.pack()

    def process_video(self):
        url = self.url_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if not save_path:
            return
        downloader = VideoDownloader(url)
        full_download = not start_time or not end_time
        downloader.download_video(full_download=full_download)
        downloader.cut_video(start_time, end_time, save_path)
        messagebox.showinfo("Success", f"Video has been saved to {save_path}")
