from youtube_transcript_api import YouTubeTranscriptApi as ytapi
from youtube_transcript_api.formatters import TextFormatter
import json


def getSubsText(video_id="", getGenerated=False):
    """
    Returns the transcript of a YouTube video as formatted text.

    Args:
        video_id (str): The ID of the YouTube video.
        getGenerated (bool): Whether to get the generated transcript or not.

    Returns:
        str: The formatted transcript text.
    """
    tList = ytapi.list_transcripts(video_id)

    if getGenerated:
        # TODO: implement getGenerated
        pass

    for t in tList:
        data = t.fetch()

    return (TextFormatter().format_transcript(data)).replace("\n", " ")


def getSubs(video_id="", getGenerated=False, chunker=None):
    tList = ytapi.list_transcripts(video_id)

    if getGenerated:
        pass
    for t in tList:
        data = t.fetch()

    return data


class subs:
    """
    A class to represent subtitles of a video.

    Attributes
    ----------
    video_id : str
        The ID of the video.
    generated : bool
        A boolean indicating whether the subtitles were generated or not.
    subs : list
        A list of subtitles.

    Methods
    -------
    __sizeof__() -> int:
        Returns the size of the list of subtitles.
    getText() -> str:
        Returns the formatted transcript of the subtitles.
    getSubs() -> str:
        Returns the subtitles in the format of "text:::duration".
    getSubsRaw() -> list:
        Returns the raw list of subtitles.
    getSubsList(size=100) -> list:
        Returns a list of chunks of subtitles, where each chunk is limited to a certain size.
    """

    def __init__(self, video_id="", generated=False):
        """
        Constructs all the necessary attributes for the subs object.

        Parameters
        ----------
        video_id : str, optional
            The ID of the video, by default "".
        generated : bool, optional
            A boolean indicating whether the subtitles were generated or not, by default False.
        """
        self.video_id = video_id
        self.generated = generated
        self.subs = getSubs(video_id, generated)

    def __sizeof__(self) -> int:
        """
        Returns the size of the list of subtitles.

        Returns
        -------
        int
            The size of the list of subtitles.
        """
        count = 0
        for _ in self.subs:
            count += 1
        return count

    def getText(self) -> str:
        """
        Returns the formatted transcript of the subtitles.

        Returns
        -------
        str
            The formatted transcript of the subtitles.
        """
        return (
            TextFormatter().format_transcript(
                self.subs)).replace(
            "\n", " ")

    def getSubs(self) -> str:
        """
        Returns the subtitles in the format of "text:::duration".

        Returns
        -------
        str
            The subtitles in the format of "text:::duration".
        """
        subs = self.subs
        # [chunk, duration]
        c_d_subs = '\n'.join(
            f"{subs['text']}:::{subs['duration']}" for subs in subs)
        return c_d_subs

    def getSubsRaw(self) -> list:
        """
        Returns the raw list of subtitles.

        Returns
        -------
        list
            The raw list of subtitles.
        """
        return self.subs

    def getSubsList(self, size=100) -> list:
        """
        Returns a list of chunks of subtitles, where each chunk is limited to a certain size.

        Parameters
        ----------
        size : int, optional
            The maximum size of each chunk, by default 100.

        Returns
        -------
        list
            A list of chunks of subtitles.
        """
        subs = json.loads(json.dumps(self.subs))
        chunks = []
        current_chunk = ""  # limited to {size}
        current_duaration = 0  # TODO: add better variable name

        for subline in subs:
            current_duaration = subline["start"]
            if len(current_chunk) + len(subline["text"]) + 1 <= size:
                current_chunk += f"{subline['text']} "
            else:
                chunks.append(
                    [
                        current_chunk.strip(),
                        current_duaration
                    ]
                )
                current_chunk = f"{subline['text']} "

        return chunks
