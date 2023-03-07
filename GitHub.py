from github import Github

key = "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"

class GitHubHandler:

    def __init__(self, api_key):
        self.data = Github(api_key)
        self.repo = self.data.get_user().get_repo("PRobot")
        #test conectivity


    def get_pull_request(self, repo_name, pull_request_number):
        repo = self.data.get_repo(repo_name)
        return repo.get_pull(pull_request_number)

    def add_comment(self, repo_name, pull_request_number, comment):
        pull = self.repo.get_pull(pull_request_number)
        pull.create_issue_comment(comment)

    def get_commit(self, repo_name, commit_sha):
        return self.repo.get_commit(commit_sha)



def test():
    github = GitHubHandler(key)
    mycommit = github.get_commit("PRobot", "c99eba24f6692eb358ca61673d1e752ff4c86636")
    diff = mycommit.files[0].patch
    print(diff)
    #print commit message
    #print(mycommit.commit.message)



test()