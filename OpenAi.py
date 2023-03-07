


import openai
import os
key = "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"

class OpenAI:
    def __init__(self, api_key):

        openai.api_key = "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"
        #openai.organization = "ma-org"
        #openai.api_key = api_key
        #Authorization: Bearer YOUR_API_KEY


    def generate_response(self, prompt):
        try:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                temperature=0.8,
                max_tokens=1024
            )
            return response["choices"][0]["text"]
        except openai.error.OpenAIError as error:
            print(f"Error generating response: {error}")


def test():

    openai = OpenAI(key)
    prompt = "who is the president of the united states?"
    response = openai.generate_response(prompt)
    if response:
        print(response)

test()
