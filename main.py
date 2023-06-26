import optparse, copy
from subtitles import getSubsText
from models.distilbart_cnn_12_6 import summarize
from models.t5_small_medium_title_generation import t5model as generate_title
from marp_wrapper import marp
from utils.chunk import LangChainChunker
from utils.ppt import generate_ppt

CHUNK_SIZE  =   512
VIDEO_ID    =   ""
OUT_PPT_NAME=   "out.pptx"

# Intermediary Markdown file
print("Creating Markdown file...")
md = marp("summary.md")
md.header()

if __name__ == "__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("-v", "--video", dest="video_id", help="YouTube video ID")
    optparser.add_option("--chunk-size", dest="chunk_size")
    optparser.add_option( "-o", "--out", dest="out_ppt_name")
    
    (opts, _) = optparser.parse_args()
    
    if opts.video_id is None:
        print("Please provide a YouTube video ID")
        exit()
    else:
        VIDEO_ID = opts.video_id
    
    if opts.chunk_size is not None:
        CHUNK_SIZE = opts.chunks_size
    
    if opts.out_ppt_name is not None:
        OUT_PPT_NAME = optparse.out_ppt_name

# Get the Subtitles from the YouTube video
print("Getting subtitles...")
video_subs = getSubsText(VIDEO_ID)

chunker_init    = LangChainChunker(video_subs)
chunks          = chunker_init.chunker(size=CHUNK_SIZE)
chunk_len       = len(chunks)

print(f"subtitles divided to {chunk_len} chunks")

chunk_num = 1
for chunk in chunks:
    print(f"processing Chunk: {chunk_num}/{chunk_len}")
    summary = summarize(chunk)
    title = generate_title(summary)
    md.addpage(title, summary)
    chunk_num += 1
    continue

print(f"Generating {OUT_PPT_NAME}..")
md.close_file()
generate_ppt("summary.md", OUT_PPT_NAME)
