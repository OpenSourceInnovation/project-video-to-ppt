from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from textwrap import dedent
import os, re

class Model:
    def __init__(self) -> None:
        load_dotenv(dotenv_path=".env")
        self.openai = os.getenv("OPENAI_API_KEY")
    
    def model(self, max_tokens=1000, temperature=0.9):
        llm = ChatOpenAI(
            max_tokens=max_tokens,
            temperature=temperature,
            openai_api_key=self.openai
        )
        
        return llm

class templates:
    def __init__(self):
        # model
        m = Model()
        self.llm = m.model()
    
    def TopicMap(self, text) -> list:
        sys_msg = SystemMessage(context="You are a person creating a presentation\nYour task is to Organize the content into a clear and logical structure. Divide your content into sections or key points. Each section should have a specific purpose and flow naturally into the next. For any given input you will provide the output in the exact specified format below with no explanation or conversion\n\nExample Output:\n1. Introduction: \n1.1 - Definition and explanation of global warming \n1.2 - Importance and relevance of the topic \n\n2. Causes of Global Warming:\n2.1- Greenhouse effect and the role of greenhouse gases\n2.2- Human activities and their contribution to global warming\n2.3- Deforestation and its impact on climate change\n2.4- Fossil fuels and their role in increasing greenhouse gas emissions \n\n3. Effects of Global Warming:\n3.1- Rising global temperatures and extreme weather events\n3.2- Melting polar ice caps and rising sea levels\n3.3- Impact on ecosystems and biodiversity\n3.4- Threats to human health and well-being \n\n4. Mitigation and Adaptation Strategies:\n4.1- The need for reducing greenhouse gas emissions \n4.2- Transition to renewable energy sources \n4.3- Sustainable agriculture and land-use practices \n4.4- Conservation and preservation of forests \n4.5- Adapting to changing climate conditions \n\n6. Conclusion: \n6.1- Recap of key points \n6.2- Urgency for action on an individual and global level \n6.3- Call to action for the audience to take steps towards combating global warming")
  
        messages = [
            sys_msg,
            HumanMessage(content=text)
        ]
        
        res = self.llm(messages).content
        
        T, FT, cc = [], {}, 0
        for line in res.split('\n'):
            match = re.search(r'^\d+\.\s(.*):', line)
            if match:
                cc += 1
                T.append(match.group(0).split('.')[1].split(':')[0].strip())
                FT[T[-1]] = []
                
                for sline in res.split('\n'):
                    match = re.search(rf'^{cc}\.\d*\s-\s(.*)', sline)
                    if match:
                        FT[T[-1]].append(match.group(1).strip())
        
        return FT
    
    def SummarizerChain():
        pass
    
    def Title():
        pass
