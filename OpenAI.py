import openai
import os
import tiktoken
from langchain.text_splitter import Tokenizer


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
                temperature=1.2,
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
                no_tokens = len(encoding.encode(self.bullets_from_single_file_initial_prompt_text+prompt))
                file_no += 1
                if no_tokens > self.m_max_tokens/2:
                    continue
                if diff_string is None:
                    continue


                print("start file no: " + str(file_no))

                prompt = prompt.replace(self.bullets_from_single_file_initial_prompt_text, "")
                prompt += self.bullets_from_single_file_initial_prompt_text + diff_string



                # if no_tokens >= self.m_max_tokens:
                #     prompt = prompt[:no_tokens]

                response = self.generate_response(prompt)
                if response is not None:
                    self.append_to_file(response)
                print("finished file no: " + str(file_no))
            print("finished generating summaries for each file")
            initial_text = self.final_summary_initial_prompt_text
            commit = commit_message
            file_summary_text = self.read_file_into_string() + "\n[Finished Summary input]"

            final_prompt = f'{initial_text}{commit}{file_summary_text}'
            if len(final_prompt) >= self.m_max_tokens:
                final_prompt = prompt[:len(final_prompt)]
            final_summary = self.generate_response(final_prompt)

        except Exception as e:
            print(e)
            return "Error generating summary"
        return final_summary

    def delete_file_if_already_exists(self):
        file_path = self.tmp_summary_file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")

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

    m_max_tokens = 2048
    tmp_summary_file = "tmp_summary.txt"

    bullets_from_single_file_initial_prompt_text = """1. You are an expert programmer, and you are trying to 
    summarize a "git diff" single file change for a pull request documentation purpose. 2. You are given a textual 
    representation of a single git diff file, and you are asked to summarize it into a single bullet-point. 3. A 
    bullet-point is a short readable summary. 4. If you think one bullet-point is insufficient, you can try to 
    summarize the diff into more than one bullet point, but one is preferable.

    [Example for Diff File]
    - Added a new feature that allows users to upload images.
    - Fixed a bug related to user authentication.
    - Refactored code to improve performance.
    [Finished Example for Diff File]
    [Now, the diff file is:]
    """

    final_summary_initial_prompt_text = """1. You are an expert programmer, and you are trying to make a summary of 
    many bullet-points more concise. 2. Summarize the bullet points into a shorter, more accurate version, 
    using these rules: A. Uniting similar bullets, B. Removing duplicates, C. Removing trivial or redundant bullet 
    points. the format of the summary should be built over several bullet points(if possible), each bullet point 
    should be separated new line. 5. In addition, you'll be receiving the commit message for the generated pull 
    request. You may use it to determine which bullet points would be desired by the pull request user.

    The input format you'll be receiving is as follows:
    1. The commit message.
    2. The bullet points in the format:
       - Bullet point 1
       - Bullet point 2
       - Bullet point 3
       ...
       
    an example input format you'll be receiving is as follows:
    [Example for Commit Message]
        updated model to use new data-type and solved bug in file1.py, added test for reminders class
    [Example for Bullet Points]
        The bullet points in the format:
       -Added a new feature in file1.py that allows users to upload images.
       -Fixed a bug in file2.py related to user authentication.
       -Refactored code in file3.py to improve performance.
   -added model X and tests for new feature
   etc...
   [Finished Example for Input Format]
    [Now the Commit Message followed by the Bullet Points are:]
    """
