import os, torch, accelerate
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, AutoModelForCausalLM

model_id = 'google/flan-t5-large'
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, load_in_8bit=True)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=512,
)

class templates:
    """
    Untested Model
    """
    def __init__(self) -> None:
        self.summaryPipe = None
        self.TitlePipe = None
    
    def ChunkSummarizer(self, text, custom_instruction: str =None, **kwargs):
        default_instruction = "generate a perfect title for the following text in 6 words: "
        instructions = custom_instruction if custom_instruction != None else default_instruction
        pipe = self.summaryPipe
        
        max_length = kwargs.get("max_length", 400)
        
        if pipe is not None:
            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=max_length,
            )
        
        return pipe(instructions + text)[0]["generated_text"]
    
    
    def ChunkTitle(self, text, custom_instruction: str =None, **kwargs):
        default_instruction = "generate a perfect title for the following text in 6 words: "
        instructions = custom_instruction if custom_instruction != None else default_instruction
        pipe = self.summaryPipe
        
        max_length = kwargs.get("max_length", 60)
        
        if pipe is not None:
            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=max_length,
            )
        
        return pipe(instructions + text)[0]["generated_text"]
    
    @staticmethod
    def model():
        return pipe

