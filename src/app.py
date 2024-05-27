import tkinter as tk
from src.video_interface import VideoInterface


def main():
    root = tk.Tk()
    app = VideoInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
