from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the DistilBART-CNN-12-6 model
# loading the model outside of the function makes it faster
SUMMARIZATION_MODEL = "sshleifer/distilbart-cnn-12-6"
tokenizer   = AutoTokenizer.from_pretrained(SUMMARIZATION_MODEL)
model       = AutoModelForSeq2SeqLM.from_pretrained(SUMMARIZATION_MODEL, device_map="cuda:0")

def summarize(text, max_len=20):
    """
    Summarizes the given text using the DistilBART-CNN-12-6 model.

    Args:
        text (str): The text to be summarized.
        max_length (int, optional): The maximum length of the summary. Defaults to 20.

    Returns:
        str: The summarized text.
    """
    
    inputs = tokenizer(text, 
                       return_tensors="pt",
                       max_length=max_len,
                       truncation=True,
    ).input_ids
    
    # Move the inputs tensor to the same device as the model tensor
    inputs = inputs.cuda()
    
    outputs = model.generate(inputs, 
                            max_new_tokens=100, 
                            num_beams=8, 
                            length_penalty=0.2, 
                            early_stopping=False
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def summarizePipeline(text):
    from transformers import pipeline
    
    pipe = pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
    )
    
    return pipe(text)[0]["summary_text"]

class templates:
    def __init__(self):
        pass
    
    @staticmethod
    def ChunkSummarizer(text):
        return summarize(text)
    
    @staticmethod
    def ChunkTitle(text, ovveride):
        if ovveride:
            return summarize(text)
        else:
            raise Exception("Model only trained for summarization")
    
    @staticmethod
    def model():
        return summarize
