import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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
        pass