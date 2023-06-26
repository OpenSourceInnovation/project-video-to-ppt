import optparse, copy
from subtitles import getSubsText
from models.distilbart_cnn_12_6 import summarize
from models.t5_small_medium_title_generation import t5model as generate_title
from marp_wrapper import marp
from utils.chunk import LangChainChunker

CHUNK_SIZE  =   512
# Intermediary Markdown file
print("Creating Markdown file...")
md = marp("summary.md")
md.header()

if __name__ == "__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("--chunk-size", dest="chunk_size")
    
    (opts, _) = optparser.parse_args()
    
    if opts.video is None:
        print("Please provide a YouTube video ID")
        exit()
    if opts.chunk_size is not None:
        CHUNK_SIZE = opts.chunks_size

# Get the Subtitles from the YouTube video
print("Getting subtitles...")
video_subs = getSubsText(opts.video)

chunker_init = LangChainChunker(video_subs)
chunks = chunker_init.chunker(size=CHUNK_SIZE)
chunk_len = len(chunks)
print(f"subtitles divided to {chunk_len} chunks")

chunk_num = 1
for chunk in chunks:
    print(f"processing Chunk: {chunk_num}/{chunk_len}")
    summary = summarize(chunk)
    print("\t summary done..")
    title = generate_title(summary)
    print("\t title done..")
    md.addpage(title, summary)
    chunk_num += 1
    continue
