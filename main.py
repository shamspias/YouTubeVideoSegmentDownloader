import os
import random
import string
import argparse
import uuid
from pytube import YouTube
from moviepy.editor import VideoFileClip


class YouTubeVideoProcessor:
    def __init__(self, url):
        self.url = url
        self.video_path = None

    def ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def generate_random_string(self, length=10):
        # Generate a random string of letters and digits
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_unique_id(self, length=14):
        # Generate a random UUID and convert to a string, taking the first 'length' characters
        return str(uuid.uuid4())[:length]

    def download_video(self):
        self.ensure_dir('inputs')
        print("Downloading the video...")
        yt = YouTube(self.url)
        video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        filename = video_stream.default_filename
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}_{self.generate_unique_id()}{ext}"  # Append UUID to the filename
        self.video_path = os.path.join('inputs', new_filename)
        video_stream.download(output_path='inputs', filename=new_filename)

    def convert_to_seconds(self, time_str):
        if time_str is None:
            return None
        parts = time_str.split(':')
        seconds = int(parts[-1])
        if len(parts) > 1:
            seconds += int(parts[-2]) * 60
        if len(parts) > 2:
            seconds += int(parts[-3]) * 3600
        return seconds

    def cut_video(self, start_time, end_time):
        clip = VideoFileClip(self.video_path)
        video_length = clip.duration

        start_seconds = self.convert_to_seconds(start_time) if start_time else 0
        end_seconds = self.convert_to_seconds(end_time) if end_time else video_length

        if start_seconds >= video_length or (end_seconds and end_seconds > video_length):
            print(f"Cannot cut this timeframe; video is shorter ({video_length} seconds) than the requested end time.")
            clip.close()
            return False

        self.ensure_dir('outputs')
        print("Cutting the video...")
        output_clip = clip.subclip(start_seconds, end_seconds)
        output_filename = os.path.join('outputs',
                                       f"cut_{self.generate_unique_id()}.mp4")
        output_clip.write_videofile(output_filename, codec='libx264')
        output_clip.close()
        print("Process completed. Saved as:", output_filename)
        return True

    def process_video(self, start_time=None, end_time=None):
        try:
            self.download_video()
            if not self.cut_video(start_time, end_time):
                os.remove(self.video_path)  # Delete downloaded video if cutting fails
            else:
                os.remove(self.video_path)  # Delete downloaded video after successful cutting
        except Exception as e:
            print(f"An error occurred: {e}")
            if os.path.exists(self.video_path):
                os.remove(self.video_path)  # Delete downloaded video if there's an error


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
    parser.add_argument("-st", "--start_time", default=None, help="Start time of the video segment (H:M:S)")
    parser.add_argument("-et", "--end_time", default=None, help="End time of the video segment (H:M:S)")
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
