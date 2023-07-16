import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from GitHub import GitHubHandler
from OpenAI import OpenAI




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pull Request Summary Generator")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Labels
        self.label_token = QLabel("GitHub Token:", self)
        self.label_token.move(20, 20)
        self.label_token.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_token.setStyleSheet("color: #333333;")

        self.label_openai_token = QLabel("OpenAI Token:", self)
        self.label_openai_token.move(20, 60)
        self.label_openai_token.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_openai_token.setStyleSheet("color: #333333;")

        self.label_repo_name = QLabel("Repository Name:", self)
        self.label_repo_name.move(20, 100)
        self.label_repo_name.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_repo_name.setStyleSheet("color: #333333;")

        self.label_pr_number = QLabel("PR Number:", self)
        self.label_pr_number.move(20, 140)
        self.label_pr_number.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_pr_number.setStyleSheet("color: #333333;")

        self.label_summary = QLabel("Pull Request Summary:", self)
        self.label_summary.move(20, 180)
        self.label_summary.setFont(QFont("Arial", 10, QFont.Bold))
        self.label_summary.setStyleSheet("color: #333333;")

        # Text Fields
        self.text_github_token = QLineEdit(self)
        self.text_github_token.setGeometry(150, 20, 200, 25)
        self.text_github_token.setText("")

        self.text_openai_token = QLineEdit(self)
        self.text_openai_token.setGeometry(150, 60, 200, 25)
        self.text_openai_token.setText("") #for testing

        self.text_repo_name = QLineEdit(self)
        self.text_repo_name.setGeometry(150, 100, 200, 25)
        self.text_repo_name.setText("showCasePr0b0t") #for testing

        self.text_pr_number = QLineEdit(self)
        self.text_pr_number.setGeometry(150, 140, 200, 25)
        self.text_pr_number.setText("3") #for testing

        # Buttons
        self.button_generate_summary = QPushButton("Generate Pull Request Summary", self)
        self.button_generate_summary.setGeometry(100, 340, 200, 30)
        self.button_generate_summary.clicked.connect(self.generate_summary)
        self.button_generate_summary.setStyleSheet("background-color: #007AFF; color: #FFFFFF; font-weight: bold;")

        self.button_reset_summary = QPushButton("Reset Summary", self)
        self.button_reset_summary.setGeometry(20, 340, 80, 30)
        self.button_reset_summary.clicked.connect(self.reset_summary)
        self.button_reset_summary.setStyleSheet("background-color: #007AFF; color: #FFFFFF; font-weight: bold;")

        self.button_set_body = QPushButton("Set Body", self)
        self.button_set_body.setGeometry(310, 340, 80, 30)
        self.button_set_body.clicked.connect(self.set_body)
        self.button_set_body.setStyleSheet("background-color: #007AFF; color: #FFFFFF; font-weight: bold;")

        # Summary Text Edit
        self.textedit_summary = QTextEdit(self)
        self.textedit_summary.setGeometry(20, 200, 370, 130)
        self.textedit_summary.setReadOnly(True)
        self.textedit_summary.setStyleSheet("background-color: #F2F2F2; border: 1px solid #CCCCCC;")

        self.openai = None



    def generate_summary(self):
        github_token = self.text_github_token.text()
        openai_token = self.text_openai_token.text()
        repo_name = self.text_repo_name.text()

        try:
            pr_number = int(self.text_pr_number.text())
            github = GitHubHandler(github_token)
            openai = OpenAI(openai_token)
            diff_files, commit_message = github.get_diff(repo_name, pr_number)
            summary = openai.generate_PR_summary(diff_files, commit_message)
            with open("summary.txt", "w") as f:
                f.write(summary)

            self.textedit_summary.setPlainText(summary)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
            return

    def reset_summary(self):
        self.textedit_summary.clear()

    def set_body(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Use the Fusion style for a consistent look
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
