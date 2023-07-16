from github import Github


class GitHubHandler:

    def __init__(self, api_key):
        self.data = Github(api_key)
        self.user = self.data.get_user()
        self.repo = self.user.get_repo("PRobot")
        # test conectivity

    def get_pull_request(self, repo_name, pull_request_number):
        repo = self.data.get_repo(repo_name)
        return repo.get_pull(pull_request_number)

    def set_comment(self, repo_name, pull_request_number, comment):
        pull = self.data.get_user().get_repo(repo_name).get_pull(pull_request_number)
        # edit the comment with the neccerly access
        pull.edit(body=comment)

    def get_commit(self, repo_name, commit_sha):
        return self.repo.get_commit(commit_sha)

    def get_diff(self, repo_name, pull_request_number):
        pull = self.data.get_user().get_repo(repo_name).get_pull(pull_request_number)
        diff = pull.get_files()
        # get the latest commit message
        commit_message = pull.get_commits().reversed[0].commit.message
        diffs = []
        for dif in diff:
            diffs.append(dif.patch)
        return diffs, commit_message

