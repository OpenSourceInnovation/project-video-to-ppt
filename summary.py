import requests
from subtitles import getSubsText
from youtube_transcript_api import YouTubeTranscriptApi


# API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL = "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": getSubsText("CrNcnkAtL2I"),
})

print(output)
