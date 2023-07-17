import os
import streamlit as st

from PR_Summarizer import (
    doc_loader, summary_prompt_creator, doc_to_final_summary, get_diff
)
from app_prompts import file_map, file_combine
from streamlit_app_utils import check_gpt_4, check_key_validity, create_temp_file, create_chat_model, \
    token_limit, token_minimum


def main():
    """
    The main function for the Streamlit app.

    :return: None.
    """
    st.title("Probot - Pullrequest summarizer")

    # TODO: feature?
    # input_method = st.radio("Select input method", ('Upload a document', 'Enter a YouTube URL'))

    open_ai_api_key = st.text_input("Enter Open-AI API key here, or contact the author if you don't have one.")
    github_api_key = st.text_input("Enter Github API key here, or contact the author if you don't have one.")
    repo_name = st.text_input("Enter Github repository name")
    pr_number = st.text_input("Enter Pullrequest number")

    use_gpt_4 = st.checkbox("Use GPT-4 for the final prompt (STRONGLY recommended, requires GPT-4 API access - "
                            "progress bar will appear to get stuck as GPT-4 is slow)", value=True)
    find_clusters = st.checkbox('Find optimal clusters (experimental, could save on token usage)', value=False)
    st.sidebar.markdown('# Made by: ')
    st.sidebar.markdown('Auther 1: [Bivas Dor](https://github.com/dorbivas)')
    st.sidebar.markdown('Auther 2: [Inon Dan](https://github.com/danninon)')

    st.sidebar.markdown('# Git link: [Probot](https://github.com/dorbivas/PRobot)')

    st.sidebar.markdown("""<small>It's always good practice to verify that a website is safe before giving it your 
    API key. This site is open source, so you can check the code yourself, or run the streamlit app 
    locally.</small>""", unsafe_allow_html=True)

    if st.button('Summarize (click once and wait)'):
        process_summarize_button(open_ai_api_key, github_api_key, repo_name, int(pr_number), use_gpt_4, find_clusters)


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
    if not validate_input(open_ai_api_key, use_gpt_4):
        return

    with st.spinner("Summarizing... please wait..."):
        git_diff, commit_message = get_diff(github_api_key, repo_name, pr_number)

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

        st.markdown(summary, unsafe_allow_html=True)
        os.unlink(temp_file_path)


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


def validate_input(api_key, use_gpt_4):
    # TODO: validate other params (github api key, github repo, github number)

    if not check_key_validity(api_key):
        st.warning('Key not valid or API is down.')
        return False

    if use_gpt_4 and not check_gpt_4(api_key):
        st.warning('Key not valid for GPT-4.')
        return False

    return True


if __name__ == '__main__':
    main()
