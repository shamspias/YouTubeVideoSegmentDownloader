# YouTubeVideoSegmentDownloader

YouTubeVideoSegmentDownloader is a Python-based tool that allows users to download specific segments from YouTube videos. This script is useful for extracting and saving parts of YouTube videos quickly and easily.

## Features
- Download full YouTube videos using a URL.
- Extract specific segments of a video based on start and end times.
- Save the segments with unique filenames to avoid overwriting.

## Prerequisites
Before you can use this tool, you need to have Python and pip installed on your system. This project also requires the installation of `pytube` and `moviepy`, Python libraries for handling YouTube video downloads and video processing, respectively.

### Installing Python
- **Linux**: Python is usually pre-installed on Linux. You can check by running `python3 --version` in the terminal. If it is not installed, you can install it using your distribution's package manager (e.g., `sudo apt install python3` for Ubuntu).
- **Windows**: Download and install Python from [python.org](https://www.python.org/downloads/). Ensure that Python is added to the PATH during installation.
- **macOS**: Python 3 can be installed using Homebrew with the command `brew install python`. If Homebrew is not installed, visit [brew.sh](https://brew.sh/) to install it first.

### Installing Dependencies
Once Python is installed, you can install the required libraries using pip:

```bash
pip install pytube moviepy
```

## Usage

1. **Clone the Repository**
   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/shamspias/YouTubeVideoSegmentDownloader.git
   cd YouTubeVideoSegmentDownloader
   ```

2. **Run the Script**
   Use the command line to navigate to the directory containing the script and run it using:

   ```bash
   python main.py -l [LINK] -st [START_TIME] -et [END_TIME]
   ```

   - `[LINK]`: The full YouTube video URL.
   - `[START_TIME]`: Start time of the video segment in H:M:S format (e.g., 0:01:20 for 1 minute and 20 seconds).
   - `[END_TIME]`: End time of the video segment in H:M:S format.

   **Example**:
   ```bash
   python main.py -l https://youtu.be/Sv8BzW01x-Y -st 0:00:06 -et 0:00:17
   ```

   This will download a segment from the specified YouTube video starting at 6 seconds and ending at 17 seconds.

3. **Access the Video**
   The downloaded segment will be saved in the `outputs` directory with a unique filename. Access this directory to find your video.

## Contributing
Contributions to the YouTubeVideoSegmentDownloader are welcome. Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues for bugs or feature requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
