import openai

class OpenAI:
    def _init_(self, api_key):
        openai.api_key = api_key

    def generate_response(self, prompt):
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            temperature=0.8,
            max_tokens=1024
        )
        return response["choices"][0]["text"]