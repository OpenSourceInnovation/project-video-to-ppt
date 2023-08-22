import subprocess, os, requests, json
from utils.log import info
from utils.subtitles import subs

def Popen(cmd: list) -> str:
    """Run a command and return the output as a string

    Args:
        cmd (list): The command to run

    Returns:
        str: The output of the command
    """
    return subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')

class video:
    def __init__(self,id, path):
        self.path = path
        self.url = "https://youtu.be/" + id
        self.video_id = id
        
        # check if directory exists
        if not os.path.exists(self.path.split("/")[-1]):
            os.mkdir(self.path.split("/")[-1])
    
    def download(self):
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
        """return the chapters of the video

        Args:
            endpoint (str): endpoint to communicate to get chapters
                            yt.lemnoslife.com recommended
        Returns:
            list: chapters
        """
        res = requests.get(f"{endpoint}")
        chapters = res.json()['items'][0]['chapters']['chapters']
        return chapters
    
    def getSubtitles(self):
        """return the raw subtitles

        Returns:
            list: subtitles directly from youtube
        """
        return json.loads(
            json.dumps(
                subs(self.video_id)
                .getSubsRaw()
            )
        )
