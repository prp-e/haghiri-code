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
    