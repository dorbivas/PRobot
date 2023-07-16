import openai
import os
import tiktoken
from langchain.text_splitter import Tokenizer


class BadOpenAITokenError(Exception):
    pass


class OpenAI:
    m_max_tokens = 2048
    tmp_summary_file = "tmp_summary.txt"
    k_input_illusion_threshold = 1024  # The higher the threshold the more likely it is to be an illusion, but if it
    # does answer it will be more accurate.
    k_output_illusion_threshold = 128  # This is a more valid threshold, since it was defined by us to the model's
    # output.
    k_model_temperature = 1.2  # The higher the temperature the more creative the model will be, but it will also be
    # more likely to make mistakes.
    k_machine_learning_model = "text-davinci-002"

    def __init__(self, api_key):
        openai.api_key = api_key

    # check output
    def generate_response(self, prompt):
        try:
            # configure the behavior  of chatGPT
            response = openai.Completion.create(
                model=self.k_machine_learning_model,
                prompt=prompt,
                temperature=self.k_model_temperature,
                max_tokens=self.m_max_tokens,

            )
            return response["choices"][0]["text"]
        except Exception as e:
            print(e)

    def generate_PR_summary(self, diff_files, commit_message):
        # break to token sized chunks
        # summarize each chunk
        # summarize the summaries

        try:
            self.delete_file_if_already_exists()
            prompt = self.bullets_from_single_file_initial_prompt_text
            encoding = tiktoken.encoding_for_model("text-davinci-002")
            file_no = 0
            print("there are " + str(len(diff_files)) + " files")

            for diff_string in diff_files:
                no_tokens = len(encoding.encode(self.bullets_from_single_file_initial_prompt_text + prompt))
                file_no += 1
                print("start file no: " + str(file_no))

                # validate input
                if no_tokens > self.k_input_illusion_threshold:  # illusion threshold
                    print(f'skipping file no: {str(file_no)}' + " because it of input is too long")
                    continue

                if diff_string is None:
                    print(f'skipping file no: {str(file_no)}' + " because file diff file is none-existent")
                    continue

                prompt = prompt.replace(self.bullets_from_single_file_initial_prompt_text, "")
                prompt += self.bullets_from_single_file_initial_prompt_text + diff_string
                response = self.generate_response(prompt)

                if len(response) > self.k_output_illusion_threshold:
                    print(f'skipping file no: {str(file_no)} because answer output is too long')
                    continue
                # validate response

                self.append_to_file(response)
                print("finished file no: " + str(file_no))
            final_summary = self.generate_summery_prompt(commit_message, prompt)

        except Exception as e:
            print(e)
            return "Error generating summary"
        return final_summary

    def generate_summery_prompt(self, commit_message, prompt):

        print("finished generating summaries for each file")
        initial_text = self.final_summary_initial_prompt_text
        commit = commit_message
        file_summary_text = self.read_file_into_string()
        final_prompt = f'{initial_text}{commit}{file_summary_text}'
        if len(final_prompt) >= self.m_max_tokens:
            final_prompt = prompt[:len(final_prompt)]  # take care of case where final prompt is too long for openai
            # to handle
        final_summary = self.generate_response(final_prompt)  # add more validation to fine grain
        return final_summary

    def delete_file_if_already_exists(self):
        file_path = self.tmp_summary_file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

    def read_file_into_string(self):
        """Reads the contents of a file into a string."""
        with open(self.tmp_summary_file, 'r') as file:
            content = file.read()
        return content

    def append_to_file(self, text):
        """Appends text to a file."""
        with open(self.tmp_summary_file, 'a') as file:
            file.write(text)

    # def num_tokens_from_string(self, string: str, encoding_name: str) -> int:
    #     """Returns the number of tokens in a text string."""
    #     encoding = tiktoken.get_encoding(encoding_name)
    #     num_tokens = len(encoding.encode(string))
    #     return num_tokens


    bullets_from_single_file_initial_prompt_text = \
        """1. You are an expert programmer, and you are trying to 
    summarize a "git diff" single file change for the documentation of a git pull request.
    every seemingly important / large difference made, summarize it into a single concise bullet-point
    you're expected to summerize exactly one point from the difference. 

    [Example for a summery of a single change in a diff File]
    - Added a new feature that allows users to upload images.
    [Finished Example for Diff File]
    do not include the prompt in the summary, just the bullet points.
    """

    final_summary_initial_prompt_text = \
        """1. You are an expert programmer, and you are trying to make a summary out of a file with possible noice.
     The file was created by you, by adding one bullet-point from each git dif made in the pull request.
    The input You've received for each file is as follows: 
    
    The input format you'll be receiving is as follows:
    1. The commit message.
    2. The bullet points may or may not be scattered in the input, since you've created it.  
    BEWARE: The input may contain some noise, and you should ignore it.
    
    Summerize the file, following these rules:
    1. The summary should be heavily based on the bullet points you've received, and should be as concise as possible.
    2. The bullet points should be heavily chosen based on the commit message.
    3. The final summary should be no longer than 5 bullet points. number each bullet you've added from 1-5.
    
    [Example for summery output]
    1. Added a new feature that allows users to upload images.
    2. Fixed a bug that caused the app to crash when the user tried to upload an image.
    3. Security updated.
    
    
    
       
    """
