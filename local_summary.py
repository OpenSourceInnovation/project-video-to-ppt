from transformers import pipeline
from subtitles import getSubsText
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from marp_wrapper import marp
import nltk
nltk.download('punkt')

summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum")

tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-small-medium-title-generation")

content = getSubsText("vsIGAQU72Ys")

def chunker(seq, size=1000):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def chunk_len(chunk):
    return len(chunk.split(" "))

md = marp("summary.md")
md.header()

for chunk in chunker(content):
    summary = summarizer(chunk)[0]['summary_text']
    inputs = ["summarize:"+ summary]
    inputs = tokenizer.batch_encode_plus(inputs, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=64)
    decoded_output = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    gen_title = nltk.sent_tokenize(decoded_output.strip())[0]
    print("Title:", gen_title, "\n")
    print("Summary:", summary, "\n")
    md.addpage(gen_title, summary)

