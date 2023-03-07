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
    mycommit = github.get_commit("PRobot", "8ba8034d242d298d46687814eae34c0f2a238c48")
    diff = mycommit.files[0].patch
    print(diff)
    #print commit message
    #print(mycommit.commit.message)



test()