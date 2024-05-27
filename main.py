import os
import random
import string
import argparse
from pytube import YouTube
from moviepy.editor import VideoFileClip


class YouTubeVideoProcessor:
    def __init__(self, url):
        self.url = url
        self.video_path = None

    def ensure_dir(self, directory):
        """Ensure that a directory exists."""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def generate_random_string(self, length=10):
        """Generate a random alphanumeric string."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def download_video(self):
        """Download the video from YouTube and save it to a specified directory with a unique name."""
        self.ensure_dir('inputs')
        print("Downloading the video...")
        yt = YouTube(self.url)
        video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        filename = video_stream.default_filename
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}{self.generate_random_string()}{ext}"
        self.video_path = os.path.join('inputs', new_filename)
        video_stream.download(output_path='inputs', filename=new_filename)

    def convert_to_seconds(self, time_str):
        """Convert a time string in H:M:S format to seconds."""
        parts = time_str.split(':')
        seconds = int(parts[-1])
        if len(parts) > 1:
            seconds += int(parts[-2]) * 60
        if len(parts) > 2:
            seconds += int(parts[-3]) * 3600
        return seconds

    def cut_video(self, start_time, end_time):
        """Cut the specified part of the video and save it to the output directory."""
        start_seconds = self.convert_to_seconds(start_time)
        end_seconds = self.convert_to_seconds(end_time)
        self.ensure_dir('outputs')
        print("Cutting the video...")
        clip = VideoFileClip(self.video_path).subclip(start_seconds, end_seconds)
        output_filename = os.path.join('outputs', f"cut_{start_time.replace(':', '')}_{end_time.replace(':', '')}.mp4")
        clip.write_videofile(output_filename, codec='libx264')
        clip.close()
        print("Process completed. Saved as:", output_filename)

    def process_video(self, start_time, end_time):
        """Handle the complete process of downloading and cutting the video."""
        try:
            self.download_video()
            self.cut_video(start_time, end_time)
        except Exception as e:
            print(f"An error occurred: {e}")


def show_manual():
    """Display the manual for using this script."""
    manual_text = """
    Usage:
        python main.py -l [LINK] -st [START_TIME] -et [END_TIME]
    Options:
        -l, -link        The full YouTube video URL.
        -st, --start_time Start time of the video segment in H:M:S format.
        -et, --end_time  End time of the video segment in H:M:S format.
        -h, --help       Show the help message and exit.
        -man             Show the manual and usage information.
    Example:
        python main.py -l https://youtu.be/Sv8BzW01x-Y -st 0:00:06 -et 0:00:17
    """
    print(manual_text)


def main():
    parser = argparse.ArgumentParser(description="Download and process a segment of a YouTube video.", add_help=False)
    parser.add_argument("-l", "-link", required=True, help="YouTube video link")
    parser.add_argument("-st", "--start_time", required=True, help="Start time of the video segment (H:M:S)")
    parser.add_argument("-et", "--end_time", required=True, help="End time of the video segment (H:M:S)")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument("-man", action='store_true', help="Show the manual and usage information")

    args = parser.parse_args()

    if args.man:
        show_manual()
        return

    processor = YouTubeVideoProcessor(args.l)
    processor.process_video(args.start_time, args.end_time)


if __name__ == "__main__":
    main()
