import logging
import requests
from github import Github
from log.app_log import log_function_entry_exit


@log_function_entry_exit
def is_github_api_key_valid(api_key):
    github_api_url = "https://api.github.com/user"
    headers = {"Authorization": f"token {api_key}"}

    try:
        response = requests.get(github_api_url, headers=headers)
        return response.status_code == 200

    except requests.RequestException:
        return False


@log_function_entry_exit
def does_github_pull_request_exist(api_key, repo_name, pr_number):
    github_api_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    headers = {"Authorization": f"token {api_key}"}

    try:
        response = requests.get(github_api_url, headers=headers)
        return response.status_code == 200
    except requests.RequestException:
        return False


@log_function_entry_exit
def does_github_repository_exist(api_key, repo_name):
    github_api_url = f"https://api.github.com/repos/{repo_name}"
    headers = {"Authorization": f"token {api_key}"}
    try:
        response = requests.get(github_api_url, headers=headers)
        return response.status_code == 200
    except requests.RequestException:
        return False


@log_function_entry_exit
def get_diff(api_key, repo_name, pull_request_number):
    """
    Get the diff and commit message for a GitHub pull request.

    :param api_key: The GitHub API key to use.

    :param repo_name: The name of the repository.

    :param pull_request_number: The number of the pull request within the repo history.

    :return: A list of diffs and the commit message.
    """
    data = Github(api_key)
    pull = data.get_user().get_repo(repo_name).get_pull(int(pull_request_number))
    diff = pull.get_files()
    # get the latest commit message
    commit_message = pull.get_commits().reversed[0].commit.message
    diffs = []
    for dif in diff:
        diffs.append(dif.patch)
    return diffs, commit_message


# TODO: integrate this function into the main code
@log_function_entry_exit
def set_comment(repo_name, pull_request_number, comment):
    print("set_comment")
    # pull = self.data.get_user().get_repo(repo_name).get_pull(pull_request_number)
    # # edit the comment with the necessary access
    # pull.edit(body=comment)


@log_function_entry_exit
def test_github_api_connectivity():
    github_api_url = "https://api.github.com"

    try:
        response = requests.get(github_api_url)
        if response.status_code != 404:
            return True
        else:
            logging.warning("OpenAI API connection failed.")
            return False
    except requests.RequestException:
        logging.error("get request failed")
        return False


@log_function_entry_exit
def validate_github_inputs(api_key, repo_name, pr_number):
    try:
        is_valid_key = is_github_api_key_valid(api_key)
        # repo_exists = does_github_repository_exist(api_key, repo_name)
        # pr_exists = does_github_pull_request_exist(api_key, repo_name, pr_number)
        status = is_valid_key  # and repo_exists and pr_exists
    except Exception as e:
        logging.error(f"Error validating GitHub inputs: {e}")
        return False
    return status
