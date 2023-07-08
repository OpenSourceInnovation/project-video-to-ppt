import subprocess, os

def Popen(cmd: list) -> str:
    """Run a command and return the output as a string

    Args:
        cmd (list): The command to run

    Returns:
        str: The output of the command
    """
    return subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE).stdout.read().strip().decode('utf-8')

class video:
    def __init__(self,url, path):
        self.path = path
        self.url = url
        
        # check if directory exists
        if not os.path.exists(self.path.split("/")[-1]):
            os.mkdir(self.path.split("/")[-1])
    
    def download(self):
        if os.path.exists(f"{self.path}.webm"):
            print(f"{self.path}.webm already exists, skipping download")
            return
        print(f"Downloading {self.url}")
        # (
        #     Popen(
        #             ["yt-dlp", self.url, "-o", self.path ]
        #     )
        # )
        os.system(f"yt-dlp {self.url} -o {self.path}")
    
    def getframe(self, timestamp):
        filename = f"{self.path}_{timestamp}.png"
        
        if os.path.exists(filename):
            print(f"{filename} already exists, skipping download")
            return
        
        print(f"Getting frame at {timestamp}")
        (
            Popen(
                [
                    "ffmpeg", 
                    "-hide_banner",
                    "-loglevel", "panic",
                    "-ss", timestamp, 
                    "-i", f"{self.path}.webm", 
                    "-vframes", "1", 
                    f"{filename}"
                ]
            )
        )
