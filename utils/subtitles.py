from youtube_transcript_api import YouTubeTranscriptApi as ytapi
from youtube_transcript_api.formatters import TextFormatter
import json

def getSubsText(video_id="", getGenerated=False):
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
    def __init__(self, video_id="", generated=False):
        self.video_id = video_id
        self.generated = generated
        self.subs = getSubs(video_id, generated)
    
    def __sizeof__(self) -> int:
        count = 0
        for _ in self.subs:
            count += 1
        return count
    
    def getText(self):
        return (TextFormatter().format_transcript(self.subs)).replace("\n", " ")
    
    def getSubs(self):
        subs = self.subs
        # [chunk, duration]
        c_d_subs = '\n'.join(f"{subs['text']}:::{subs['duration']}" for subs in subs)
        return c_d_subs
    
    def getSubsRaw(self):
        return self.subs
    
    def getSubsList(self, size=100):
        subs = json.loads(json.dumps(self.subs))
        chunks = []
        current_chunk = "" # limited to {size}
        current_duaration = 0  # TODO: add better variable name
        c_d_target = 2
        c_d_count = 0
        
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
