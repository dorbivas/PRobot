import functools
import os

import requests
import streamlit as st

import logging
import logging.config

from app_github import test_github_api_connectivity, validate_github_inputs, get_diff, set_comment

from app_openai import (
    doc_loader, summary_prompt_creator, doc_to_final_summary, test_openai_api_connectivity
)
from app_streamlit import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, \
    token_limit, token_minimum, check_gpt_3_5

from app_prompts import file_map, file_combine
from log.app_log import log_function_entry_exit, init_logger


@log_function_entry_exit
def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """

    # Set up the logger as shown above
    init_logger()

    try:
        # Example log messages

        logging.info("Called 'main'.")
        st.title("Probot - Pullrequest summarizer")
        # Create a Streamlit app
        st.title("API Connectivity Status")

        render_check_connectivity()
        connectivity_status = is_check_connectivity()

        # TODO: feature?
        # input_method = st.radio("Select input method", ('Upload a document', 'Enter a YouTube URL'))

        open_ai_api_key = st.text_input("Enter Open-AI API key here, or contact the author if you don't have one.",
                                        disabled=not connectivity_status)
        github_api_key = st.text_input("Enter Github API key here, or contact the author if you don't have one.",
                                       disabled=not connectivity_status)
        repo_name = st.text_input("Enter Github repository name", disabled=not connectivity_status)
        pr_number = st.text_input("Enter Pullrequest number", disabled=not connectivity_status)

        use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - "
                                "progress bar will appear to get stuck as GPT-4 is slow)", value=True,
                                disabled=not connectivity_status)
        find_clusters = st.checkbox('Find optimal clusters (experimental, could save on token usage)', value=False,
                                    disabled=not connectivity_status)
        st.sidebar.markdown('# Made by: ')
        st.sidebar.markdown('Auther 1: [Bivas Dor](https://github.com/dorbivas)')
        st.sidebar.markdown('Auther 2: [Inon Dan](https://github.com/danninon)')

        st.sidebar.markdown('# Git link: [Probot](https://github.com/dorbivas/PRobot)')

        st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your 
        API key. This site is open source, so you can check the code yourself, or run the streamlit app 
        locally.</small>""", unsafe_allow_html=True)

        st.button(
            'Summarize (click once and wait)', disabled=not connectivity_status, on_click=process_summarize_button,
            args=(open_ai_api_key, github_api_key, repo_name, pr_number, use_gpt_4, find_clusters)
        )

        if st.button('Set PR comment!', disabled=not connectivity_status and is_summary_present()):
            set_comment(github_api_key, repo_name, pr_number, st.session_state.summary)
    except Exception as e:
        logging.exception(e)
        st.write("An error occurred. Please contact the author.")


@log_function_entry_exit
def render_check_connectivity():
    github_status = test_github_api_connectivity()
    if github_status:
        st.write("GitHub API: ✅ Connected")
    else:
        st.write("GitHub API: ❌ Not Connected")

    # Check OpenAI API connectivity and display status
    openai_status = test_openai_api_connectivity()
    if openai_status:
        st.write("OpenAI API: ✅ Connected")
    else:
        st.write("OpenAI API: ❌ Not Connected")


def is_check_connectivity():
    github_status = test_github_api_connectivity()
    openai_status = test_openai_api_connectivity()
    return github_status and openai_status


@log_function_entry_exit
def process_summarize_button(open_ai_api_key, github_api_key, repo_name, pr_number, use_gpt_4, find_clusters):
    """
    Processes the summarize button, and displays the summary if input and doc size are valid
    :param open_ai_api_key: Open-AI API key
    :param github_api_key: GitHub API key
    :param repo_name: GitHub repository's Name
    :param pr_number: Repository's requested Pullrequest number
    :param use_gpt_4: Whether to use GPT-4 or not

    :param find_clusters: Whether to find optimal clusters or not, experimental

    :return: None
    """
    if not validate_input(open_ai_api_key, github_api_key, repo_name, pr_number, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):

        git_diff, commit_message = get_diff(github_api_key, repo_name, pr_number)
        logging.info("Got diff from GitHub API.")

        temp_file_path = create_temp_file(git_diff)

        doc = doc_loader(temp_file_path)
        map_prompt = file_map
        combine_prompt = file_combine

        llm = create_chat_model(open_ai_api_key, use_gpt_4)
        initial_prompt_list = summary_prompt_creator(map_prompt, 'text', llm)
        final_prompt_list = summary_prompt_creator(combine_prompt, 'text', llm)

        if not validate_doc_size(doc):
            os.unlink(temp_file_path)
            return

        if find_clusters:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, open_ai_api_key, use_gpt_4,
                                           find_clusters)

        else:
            summary = doc_to_final_summary(doc, 10, initial_prompt_list, final_prompt_list, open_ai_api_key, use_gpt_4)

        st.markdown(summary, unsafe_allow_html=True, key='summary')
        os.unlink(temp_file_path)


def is_summary_present():
    return 'summary' in st.session_state


@log_function_entry_exit
def validate_doc_size(doc):
    """
    Validates the size of the document

    :param doc: doc to validate

    :return: True if the doc is valid, False otherwise
    """
    if not token_limit(doc, 800000):
        st.warning('File or transcript too big!')
        return False

    if not token_minimum(doc, 10):
        st.warning('File or transcript too small!')
        return False
    return True


@log_function_entry_exit
def validate_input(open_ai_api_key, github_api_key, repo_name, pr_number, use_gpt_4):
    # TODO: validate other params (github api key, github repo, github number)
    if not validate_github_inputs(github_api_key, repo_name, pr_number):
        st.warning('GitHub inputs not valid.')
        return False

    if not check_key_validity(open_ai_api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(open_ai_api_key):
        st.warning('Key not valid for GPT-4.')
        return False
    if not check_gpt_3_5(open_ai_api_key):
        st.warning('Key not valid for GPT-3.5.')
        return False

    return True


if __name__ == '__main__':
    main()
