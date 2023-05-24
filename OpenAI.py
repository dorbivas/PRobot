import openai
import os


class BadOpenAITokenError(Exception):
    pass


class OpenAI:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_response(self, prompt):
        try:
            # configure the behavior  of chatGPT
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                temperature=1,
                max_tokens=2048,

            )
            return response["choices"][0]["text"]
        except openai.error.OpenAIError as error:
            print(f"Error generating response: {error}")


def test():
    pass

def check_response(response):
    pass


