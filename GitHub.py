from github import Github

key = "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"

class GitHubHandler:

    def __init__(self, api_key):
        self.token = Github(api_key)
        #test conectivity


    def get_pull_request(self, repo_name, pull_request_number):
        repo = self.token.get_repo(repo_name)
        return repo.get_pull(pull_request_number)

    def add_comment(self, repo_name, pull_request_number, comment):
        pull_request = self.get_pull_request(repo_name, pull_request_number)
        pull_request.create_issue_comment(comment)

    def get_commit(self, repo_name, commit_sha):
        repo = self.token.get_user().get_repo(repo_name)
        return repo.get_commit(commit_sha)


def test():
    github = GitHubHandler(key)
    mycommit = github.get_commit("PRobot", "71dad601a0f1d59c14927ce5ffdea6ed71ee3cbb")
    #print commit message
    print(mycommit.commit.message)



test()