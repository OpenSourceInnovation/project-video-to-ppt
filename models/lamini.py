# Load model directly
from langchain.llms import HuggingFacePipeline
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
    GenerationConfig
)

model_id = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id, device_map="cuda:0")
gen_config = GenerationConfig.from_pretrained(model_id)

class lamini:
    def __init__(self) -> None:
        pass
    
    def load_model(
        task="text2text-generation",
        **kwargs
    ):
        """Returns a pipeline for the model
        - model: MBZUAI/LaMini-Flan-T5-248M
        
        Returns:
            _type_: _description_
        """
        
        max_length = kwargs.get("max_length", 512)
        temperature = kwargs.get("temperature", 0)
        top_p = kwargs.get("top_p", 0.95)
        repetition_penalty = kwargs.get("repetition_penalty", 1.15)
        
        pipe = pipeline( 
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                generation_config=gen_config,
                max_length=max_length,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
        )
        
        llm = HuggingFacePipeline(pipeline=pipe)
        return llm
    
    class templates:
        def __init__(self) -> None:
            pass
        
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
        
