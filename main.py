
import sys
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(sys.executable)
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

