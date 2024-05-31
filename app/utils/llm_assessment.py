from app.utils.llm_client import LLMClient

class LLMAssessment:
    def __init__(self):
        self.client = LLMClient()

    def generate_llm_assessment(self, system_message: str, prompt: str) -> dict:
        if self.client.api_type == "anthropic":
            messages = [{"role": "user", "content": prompt}]
            response = self.client.call_api(messages, system=system_message)
        else:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ]
            response = self.client.call_api(messages)
        return response
