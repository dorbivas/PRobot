from github import Github

class GitHubHandler:
    def _init_(self, username, password):
        self.g = Github(username, password)

    def get_pull_request(self, repo_name, pull_request_number):
        repo = self.g.get_repo(repo_name)
        return repo.get_pull_request(pull_request_number)

    def add_comment(self, repo_name, pull_request_number, comment):
        pull_request = self.get_pull_request(repo_name, pull_request_number)
        pull_request.create_issue_comment(comment)