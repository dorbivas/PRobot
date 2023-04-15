from github import Github

class GitHubHandler:

    def __init__(self, api_key):
        self.data = Github(api_key)
        self.repo = self.data.get_user().get_repo("PRobot")
        #test conectivity


    def get_pull_request(self, repo_name, pull_request_number):
        repo = self.data.get_repo(repo_name)
        return repo.get_pull(pull_request_number)

    def set_comment(self, repo_name, pull_request_number, comment):
        pull = self.data.get_user().get_repo(repo_name).get_pull(pull_request_number)
        #edit the comment with the neccerly access
        pull.edit(body=comment)

    def get_commit(self, repo_name, commit_sha):
        return self.repo.get_commit(commit_sha)

    def get_diff(self, repo_name, pull_request_number):
        pull = self.data.get_user().get_repo(repo_name).get_pull(pull_request_number)
        diff = pull.get_files()
        #get the latest commit message
        commit_message = pull.get_commits().reversed[0].commit.message
        diffs = []
        for dif in diff:
            diffs.append(dif.patch)
        return diffs, commit_message


def test():
    #get key from user input
    key = input("Enter your GitHub API key: ")
    github = GitHubHandler(key)

    #get the diff files and the commit message
    diffs, commit_message = github.get_diff("kaplat-ex1-dor-bivas", 8)


    print(commit_message)
    print(diffs)
    #set comment
    #github.set_comment("kaplat-ex1-dor-bivas", 5, "test comment")

    #mycommit = github.get_commit("PRobot", "8ba8034d242d298d46687814eae34c0f2a238c48")
    #diff = mycommit.files[0].patch
    #print(diff)
    #print commit message
    #print(mycommit.commit.message)



#test()