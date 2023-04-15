
import sys
# Press the green button in the gutter to run the script.
from GitHub import GitHubHandler
from OpenAI import OpenAI

init_prompt = """
You are an expert programmer, and you are trying to summarize a "git diff" file for a Pull request documentation .
Reminders about the git diff format:
For each file, there are a few metadata lines, for example:
\`\`\`
diff --git a/lib/index.js b/lib/index.js
index aadf691..bfef603 100644
--- a/lib/index.js  
+++ b/lib/index.js
\`\`\`
This means that \`lib/index.js\` was modified in this commit. Note that this is only an example.
Then there is a specifier of the lines that were modified.
A line starting with \`+\` means it was added.
A line that starting with \`-\` means that line was deleted.
A line that starts with neither \`+\` nor \`-\` is code given for context and better understanding. 
This is not part of the diff.
you will get the commit message at the start for reference of the subject of the diffs files.
# respect the commit message in corresponding to the diffs in order generate the best summary.
# the commit message will be at the start like this : "commit message: <commit message>" 
"""

first_injection_prompt = """
The following is a git diff of a single file.
Please summarize it in a comment, describing the changes made in the diff in high level.
Do it in the following way:
Write \`SUMMARY:\` and then write a summary of the changes made in the diff respecting the commit , as a bullet point list.
Every bullet point should start with a \`* \`. :
"""

injection_prompt_rep = """
here is another git diff of a single file.
Please summarize it in a comment, describing the changes made in the diff in high level.
Do not add "SUMMARY:" again it will be connected to the previous summary.
Do it in the following way:
write a summary of the changes made in the diff, as a bullet point list.
Every bullet point should start with a \`* \`. :
"""

def generate_PR_summay(diffs, commit_message):
    prompt = init_prompt
    final_summery = ""
    commit_injection = f"\ncommit message: {commit_message}"

    for diff in diffs:
        if diff != diffs[0]:
            prompt += injection_prompt_rep + diff
            response = openai.generate_response(prompt)
            prompt = prompt.replace(injection_prompt_rep, "")

        else:
            prompt += first_injection_prompt + commit_injection + diff
            response = openai.generate_response(prompt)
            prompt = prompt.replace(first_injection_prompt, "")

        if response:
            final_summery += response

    return final_summery


if __name__ == '__main__':
    print(sys.executable)

    # 1) open session with git hub and openAI
    # 1.1) get api key for all the session from file
    ##git hub first line and openAI second line
    github = GitHubHandler(input("Enter your github key: "))
    openai = OpenAI(input("Enter your openAI key: "))

    # 2) get the pull request name and number from the user
    repo_name = input("Enter the repo name: ")
    pull_request_number = int(input("Enter the pull request number: "))

    # 3) get the diff from the pull request and the commit message
    diffs, commit_messages = github.get_diff(repo_name, pull_request_number)

    # 4) send the diff and the commit message to the openAI server
    summery = generate_PR_summay(diffs, commit_messages)
    print(summery)
    # 5) create the summery from the diff and the commit message
    # 6) set the summery as the body of the pull request


    # USER
    # 1) open session with github
    # 1.1) get api key for all the session from file
    # 1.2) get repo name and pull request number from user
    #Server
    # 2) get the pull request from github
    # 3) get the diff from the pull request and the commit message
    # 4) send the diff and the commit message to the openAI server
    # 5) create the summery from the diff and the commit message
    # 6) set the summery as the body of the pull request

    # TODO: OpenAIrespect file names in the response

    # PR object --> git branch , e.g B1...B3
    # diff files
    # Commits
    # commit message
    # File names

    # diff format:
    # commit messagem ,file name , diff file (patch) , file name , diff file(patch)...



