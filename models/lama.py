# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("MBZUAI/LaMini-Flan-T5-248M")
model = AutoModelForSeq2SeqLM.from_pretrained("MBZUAI/LaMini-Flan-T5-248M", max_length=200)

def summarize(text):
    instructions = "summarize for better understanding: "
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, min_length=80)
    return pipe(instructions + text)

def generate_title(text):
    instructions = "generate a perfect title for the following text in 6 words: "
    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=40, min_length=20)
    return pipe(instructions + text)
