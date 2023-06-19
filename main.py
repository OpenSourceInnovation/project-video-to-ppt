import optparse, copy
from subtitles import getSubsText
from models.distilbart_cnn_12_6 import summarize
from models.t5_small_medium_title_generation import t5model as generate_title
from marp_wrapper import marp

def chunker(seq, size=1000):
    words = seq.split()
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) + 1 <= size:
            current_chunk += f"{word} "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = f"{word} "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def chunklen(seq):
    count = 0
    for c in seq:
        count += 1
    return count

# Intermediary Markdown file
print("Creating Markdown file...")
md = marp("summary.md")
md.header()

if __name__ == "__main__":
    optparser = optparse.OptionParser()
    optparser.add_option("-v", "--video", dest="video", help="YouTube video ID")
    
    (opts, _) = optparser.parse_args()
    
    if opts.video is None:
        print("Please provide a YouTube video ID")
        exit()

# Get the Subtitles from the YouTube video
print("Getting subtitles...")
video_subs = getSubsText(opts.video)

# divide the subs into chunks for more accurate summarization
# TODO: divide the subs into chunks based on the topics
# summarize each chunk and add it to the markdown file
chunk_len = copy.deepcopy(chunklen(chunker(video_subs, size=200)))
chunk_num = 1
for chunk in chunker(video_subs, size=200):
    print(f"processing Chunk: {chunk_num}/{chunk_len}")
    summary = summarize(chunk)
    print("\t summary done..")
    title = generate_title(summary)
    print("\t title done..")
    md.addpage(title, summary)
    chunk_num += 1
    continue
