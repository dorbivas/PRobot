import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
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



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pull Request Summary Generator")
        self.setGeometry(100, 100, 400, 400)

        # Labels
        self.label_token = QLabel("GitHub Token:", self)
        self.label_token.move(20, 20)

        self.label_openai_token = QLabel("OpenAI Token:", self)
        self.label_openai_token.move(20, 60)

        self.label_repo_name = QLabel("Repository Name:", self)
        self.label_repo_name.move(20, 100)

        self.label_pr_number = QLabel("PR Number:", self)
        self.label_pr_number.move(20, 140)

        self.label_summary = QLabel("Pull Request Summary:", self)
        self.label_summary.move(20, 180)

        # Text Fields
        self.text_token = QLineEdit(self)
        self.text_token.setGeometry(150, 20, 200, 25)

        self.text_openai_token = QLineEdit(self)
        self.text_openai_token.setGeometry(150, 60, 200, 25)

        self.text_repo_name = QLineEdit(self)
        self.text_repo_name.setGeometry(150, 100, 200, 25)

        self.text_pr_number = QLineEdit(self)
        self.text_pr_number.setGeometry(150, 140, 200, 25)

        # Buttons
        self.button_generate_summary = QPushButton("Generate Pull Request Summary", self)
        self.button_generate_summary.setGeometry(100, 340, 200, 30)
        self.button_generate_summary.clicked.connect(self.generate_summary)

        self.button_reset_summary = QPushButton("Reset Summary", self)
        self.button_reset_summary.setGeometry(20, 340, 80, 30)
        self.button_reset_summary.clicked.connect(self.reset_summary)

        self.button_set_body = QPushButton("Set Body", self)
        self.button_set_body.setGeometry(310, 340, 80, 30)
        self.button_set_body.clicked.connect(self.set_body)

        # Summary Text Edit
        self.textedit_summary = QTextEdit(self)
        self.textedit_summary.setGeometry(20, 200, 370, 130)
        self.textedit_summary.setReadOnly(True)
        self.openai = None

    def generate_PR_summary(self, diffs, commit_message):
        prompt = init_prompt
        final_summery = ""
        commit_injection = f"\ncommit message: {commit_message}"

        for diff in diffs:
            if diff != diffs[0]:
                prompt += injection_prompt_rep + diff
                response = self.openai.generate_response(prompt)
                prompt = prompt.replace(injection_prompt_rep, "")

            else:
                prompt += first_injection_prompt + commit_injection + diff
                response = self.openai.generate_response(prompt)
                prompt = prompt.replace(first_injection_prompt, "")

            if response:
                final_summery += response

        return final_summery


    def generate_summary(self):

        github_token = self.text_token.text()
        openai_token = self.text_openai_token.text()
        repo_name = self.text_repo_name.text()
        pr_number = int(self.text_pr_number.text())
        print('1')
        try:
            github = GitHubHandler(github_token)
            print(github.data)
            self.openai = OpenAI(openai_token)
            diffs, commit_message = github.get_diff(repo_name, pr_number)
            summary = self.generate_PR_summary(diffs, commit_message)
            print(summary)
            #  github.set_comment(repo_name,pull_request_number, summary)
            self.textedit_summary.setPlainText(summary)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
            return

        # Clear the input fields
        self.text_token.clear()
        self.text_openai_token.clear()
        self.text_repo_name.clear()
        self.text_pr_number.clear()

    def reset_summary(self):
        self.textedit_summary.clear()

    def set_body(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
