# divide the subs into chunks for more accurate summarization
# TODO: divide the subs into chunks based on the topics
# summarize each chunk and add it to the markdown file

class legacy_chunker:
    # legacy manual chunker
    def __init__(self, text):
        self.text = text
    def chunker(self, size=1000):
        words = self.text.split()
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

    
    def __sizeof__(self) -> int:
        count = 0
        for _ in self.text:
            count += 1
        return count
            
class LangChainChunker:
    def __init__(self, text):
        self.text = text
    
    def chunker(self, size=1000):
        from langchain.text_splitter import CharacterTextSplitter
        
        text_splitter = CharacterTextSplitter(
            separator=" ",
            chunk_size=size,
            chunk_overlap=0.9,
        )
        
        return text_splitter.split_text(self.text)
    
    def __sizeof__(self) -> int:
        count = 0
        for _ in self.text:
            count += 1
        return count
