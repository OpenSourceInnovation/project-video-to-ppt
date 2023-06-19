from youtube_transcript_api import YouTubeTranscriptApi as ytapi
from youtube_transcript_api.formatters import TextFormatter

def getSubsText(video_id="", getGenerated=False):
    tList = ytapi.list_transcripts(video_id)
    
    if getGenerated:
        # TODO: implement getGenerated
        pass
    
    for t in tList:
        data = t.fetch()
    
    return (TextFormatter().format_transcript(data)).replace("\n", " ")

# # write subs to file
# subs = getSubsText("CrNcnkAtL2I")
# with open("subs.txt", "w") as f:
#     f.write(subs)
