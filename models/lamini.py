# Load model directly
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
    GenerationConfig
)

model_id = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
gen_config = GenerationConfig.from_pretrained(model_id)


def summarize(text):
    instructions = "summarize for better understanding: "
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=400,
        generation_config=gen_config,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15
    )
    return pipe(instructions + text)


def generate_title(text):
    instructions = "generate a perfect title for the following text in 6 words: "

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=60,
        generation_config=gen_config,
        temperature=0,
        top_p=0.95,
        repetition_penalty=1.15
    )

    return pipe(instructions + text)
