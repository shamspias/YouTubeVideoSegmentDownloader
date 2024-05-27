from pytube import YouTube
from moviepy.editor import VideoFileClip
import os


class VideoDownloader:
    def __init__(self, url):
        self.url = url
        self.video_path = None

    def download_video(self, full_download=False):
        yt = YouTube(self.url)
        video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        if full_download:
            self.video_path = video_stream.download(filename='full_video.mp4')
        else:
            self.video_path = video_stream.download()

    def cut_video(self, start_time, end_time, output_filename):
        if start_time and end_time:
            start_seconds = self.convert_to_seconds(start_time)
            end_seconds = self.convert_to_seconds(end_time)
            clip = VideoFileClip(self.video_path).subclip(start_seconds, end_seconds)
            clip.write_videofile(output_filename, codec='libx264')
            clip.close()
        else:
            # Rename the downloaded video to the specified output if no cutting is required
            os.rename(self.video_path, output_filename)

    def convert_to_seconds(self, time_str):
        parts = time_str.split(':')
        seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(parts)))
        return seconds
