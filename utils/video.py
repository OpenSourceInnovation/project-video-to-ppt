import subprocess
import os
import requests
import json
from utils.log import info
from utils.subtitles import subs


def Popen(cmd: list) -> str:
    """Run a command and return the output as a string

    Args:
        cmd (list): The command to run

    Returns:
        str: The output of the command
    """
    return subprocess.Popen(
        cmd,
        shell=False,
        stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')


class video:
    def __init__(self, id, path):
        """
        Initializes a video object with the given video id and path.

        Args:
            id (str): The video id.
            path (str): The path to save the video.
        """
        self.path = path
        self.url = "https://youtu.be/" + id
        self.video_id = id

        # check if directory exists
        if not os.path.exists(self.path.split("/")[-1]):
            os.mkdir(self.path.split("/")[-1])

    def download(self):
        """
        Downloads the video from the given url and saves it to the specified path.
        """
        if os.path.exists(f"{self.path}.webm"):
            info(f"{self.path}.webm already exists, skipping download")
            return
        info(f"Downloading {self.url}")
        # (
        #     Popen(
        #             ["yt-dlp", self.url, "-o", self.path ]
        #     )
        # )
        os.system(f"yt-dlp {self.url} -o {self.path}")

    def getframe(self, timestamp, out=os.curdir):
        """
        Extracts a frame from the video at the given timestamp and saves it to the specified path.

        Args:
            timestamp (str): The timestamp of the frame to extract.
            out (str, optional): The path to save the extracted frame. Defaults to os.curdir.
        """
        filename = out
        if os.path.exists(filename):
            info(f"{filename} already exists, skipping frame")
            return

        info(f"Getting frame at {timestamp}")
        (
            Popen(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel", "panic",
                    "-ss", timestamp,
                    "-i", f"{self.path}.webm",
                    "-vframes", "1",
                    filename
                ]
            )
        )

    def getAudio(self, out="out.mp3"):
        """
        Extracts the audio from the video and saves it to the specified path.

        Args:
            out (str, optional): The path to save the extracted audio. Defaults to "out.mp3".
        """
        info("Getting audio...")
        (
            Popen(
                [
                    "ffmpeg",
                    "-hide_banner",
                    "-loglevel", "panic",
                    "-i", f"{self.path}.webm",
                    "-vn",
                    "-ar", "44100",
                    "-ac", "2",
                    "-ab", "192K",
                    "-f", "mp3",
                    out
                ]
            )
        )

    def getChapters(self, endpoint: str) -> list:
        """
        Returns the chapters of the video.

        Args:
            endpoint (str): The endpoint to communicate to get chapters. yt.lemnoslife.com recommended.

        Returns:
            list: The chapters of the video.
        """
        res = requests.get(f"{endpoint}")
        chapters = res.json()['items'][0]['chapters']['chapters']
        return chapters

    def getSubtitles(self):
        """
        Returns the raw subtitles directly from youtube.

        Returns:
            list: The subtitles directly from youtube.
        """
        return json.loads(
            json.dumps(
                subs(self.video_id)
                .getSubsRaw()
            )
        )
