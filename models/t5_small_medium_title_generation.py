import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def t5model(prompt: str) -> str:
    tokenizer = AutoTokenizer.from_pretrained("fabiochiu/t5-small-medium-title-generation")
    model = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-small-medium-title-generation")
    inputs = tokenizer(
        ["summarize:" + prompt],
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )
    
    outputs = model.generate(
        **inputs,
        num_beams=8,
        do_sample=True,
        min_length=10,
        max_length=64
    )
    
    decoded_output = tokenizer.batch_decode(
        outputs, skip_special_tokens=True
    )[0]
    
    return decoded_output

