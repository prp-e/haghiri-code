import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.environ["OPENROUTER_API_KEY"]
)

class Agent:
    def __init__(self, system_prompt):

        self.system_prompt = system_prompt
        self.messages = []

        if self.system_prompt:
            self.messages.append(
                {
                    "role" : "system",
                    "content" : system_prompt
                }
            )
    def __call__(self, message):

        self.messages.append(
            {
                "role" : "user",
                "content" : message
            }
        )

        result = self.execute()

        self.messages.append(
            {
                "role" : "assistant",
                "content" : result
            }
        )
    
    def execute(self):
        
        result = client.chat.completions.create(
            model = os.environ["MODEL"],
            messages = self.messages,
            temperature = 0.0 
        )

        return result.choices[0].message.content