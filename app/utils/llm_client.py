import json
from app.core.config import settings
from openai import OpenAI
import openai
from groq import Groq


class LLMClient:
    def __init__(self):
        self.api_type = settings.API_TYPE
        self.openai_model_name = settings.OPENAI_MODEL_NAME
        self.groq_model_name = settings.GROQ_MODEL_NAME
        if self.api_type == "openai":
            openai.api_key = settings.OPENAI_API_KEY
            self.client = OpenAI()
        elif self.api_type == "groq":
            self.api_key = settings.GROQ_API_KEY
            self.client = Groq(
                api_key=settings.GROQ_API_KEY
            )
        else:
            raise ValueError("Invalid API type. Choose either 'openai' or 'groq'.")

    def call_openai_client(self, messages):
        chat_completion = self.client.chat.completions.create(
            model=self.openai_model_name,
            messages=messages,
            response_format={"type": "json_object"},
        )
        return chat_completion.choices[0].message['content']

    def call_groq_client(self, messages):
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.groq_model_name,
        )
        response = chat_completion.choices[0].message.content
        if self.is_valid_json(response):
            return response
        else:
            return self.handle_non_json_response(response)

    def handle_non_json_response(self, text: str):
        # Generate a prompt to extract JSON from the non-JSON response
        extraction_prompt = (
            "Extract only the JSON part from the following text and return it as a valid JSON object:\n\n"
            f"{text}"
        )
        extraction_messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": extraction_prompt}
        ]
        extracted_json = self.call_groq_client(extraction_messages)
        # Validate the extracted response
        if self.is_valid_json(extracted_json):
            return json.loads(extracted_json)
        else:
            return {"error": "Failed to extract valid JSON from the Groq API response"}

    def is_valid_json(self, text: str):
        try:
            json.loads(text)
            return True
        except ValueError:
            return False

    def call_api(self, messages):
        if self.api_type == "openai":
            return self.call_openai_client(messages)
        elif self.api_type == "groq":
            return self.call_groq_client(messages)
