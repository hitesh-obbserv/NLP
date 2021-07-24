# -*- coding: utf-8 -*-
# @Date    : 25-06-2021
# @Author  : Hitesh Gorana
# @Link    : None
# @Version : 0.0
import base64
import json
import re

import pandas as pd
import requests
import streamlit as st

st.set_page_config(layout='wide')
COPY = False

API = ("api_kyQBgsSSWviekDkqOVLHjvREJZaZoZdigT",)


def query(payload, API_URL, headers):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


def download(text):
    text = text.encode()
    b64 = base64.b64encode(text).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="summarize.txt" target="_blank">Download</a>'
    return href


def summarization(API_URL, headers):
    text = st.text_area(
        "Enter text",
        height=200,
    )
    if st.button("summarize", help='summarize'):
        if text:
            data = query(
                {
                    "inputs": text,
                }, API_URL, headers
            )
            if COPY:
                st.code(data[0]['summary_text'])
            else:
                _ = st.text_area('Output', value=data[0]['summary_text'], height=200)
                st.markdown(download(data[0]['summary_text']), unsafe_allow_html=True)
        else:
            st.markdown("# :anger:")
            st.text('No text to summarize')


def TextGeneration(API_URL, headers):
    text = st.text_area(
        "Enter ",
        height=200,
        max_chars=512,
    )
    if st.button("generate", help='generate text'):
        if text:
            data = query(
                {
                    "inputs": text,
                }, API_URL, headers
            )
            if COPY:
                st.code(data[0]['generated_text'])
            else:
                _ = st.text_area('Output', value=data[0]['generated_text'], height=200)
            st.markdown(download(data[0]['generated_text']), unsafe_allow_html=True)
        else:
            st.markdown("# :anger:")
            st.text('No text for Generation')


def QuestionAnswering(API_URL, headers):
    QA = st.text_area(
        "Question",
        height=200,
    )
    Context = st.text_area(
        "Context",
        height=200,
    )
    if st.button("Ask", help='Ask question'):
        if QA and Context:
            data = query(
                {
                    "inputs": {
                        "question": QA,
                        "context": Context,
                    }
                }, API_URL, headers
            )
            if COPY:
                st.code(data['score'])
                st.code(data['answer'])
            else:
                _ = st.text_area('score', value=data['score'])
                _ = st.text_area('answer', value=data['answer'])
            st.markdown(download(data['answer'] + f' \nSCORE : {str(data["score"])}'), unsafe_allow_html=True)
        else:
            st.markdown("# :anger:")
            st.text('No text for answer')


def FILL_MASK(API_URL, headers):
    text = st.text_area(
        "Enter ",
        height=200,
    )
    if st.button("fill mask", help='fill mask'):
        data = None
        if text:
            data = query(
                {
                    "inputs": text,
                }, API_URL, headers
            )
            if COPY:
                st.code(data[0]['sequence'])
            else:
                _ = st.text_area('Output', value=data[0]['sequence'], height=200)
            st.markdown(download(data[0]['sequence']), unsafe_allow_html=True)
        else:
            st.markdown("# :anger:")
            st.text('No text for Generation')
        df = pd.DataFrame(data)
        st.table(df)


def FILL_MASK_INFO():
    st.text('replace unknown with this letter given bellow')
    st.code('[MASK]')


def Backlink():
    url = st.text_area(
        "Enter Link",
    )
    backlink = st.text_area(
        "Enter backlink",
    )
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if st.button("check"):
        # if (re.match(regex, url) is not None) and (re.match(regex, backlink) is not None):

        if url and backlink:
            def check_backlink():
                f = requests.get(url)
                print('.com'.join(backlink.split('.com')))
                data = f.text
                if backlink.endswith('/'):
                    return data.find(backlink[:-1]) and data.find(backlink) and data.find('.com'.join(backlink.split('.com')[1:])[1:-1])
                else:
                    return data.find(backlink) and backlink.find('.com'.join(backlink.split('.com')[1:])[1:])
            res = check_backlink()
            if res == -1:
                st.code("Backlink not found.")
            else:
                st.code("Backlink found.")
    else:
        st.markdown("# :anger:")
        st.text('No Link to backlink check')
# else:
#     st.text('enter valid link')


def main():
    # print('NEW USER')
    # key = st.sidebar.selectbox("API", API)
    key = API[-1]
    headers = {"Authorization": f"Bearer {key}"}

    USER_ENDPOINT = "https://api-inference.huggingface.co/usage/2021/6"
    response = requests.request("GET", USER_ENDPOINT, headers=headers).json()
    if response['available'] - response['used'] <= response['available']:
        # st.sidebar.code(f'NAME : {str(response["name"])}')
        # st.sidebar.code(f'TOTAL USED : {str(response["used"])}')
        # st.sidebar.code(f'TOTAL AVAILABLE : {str(response["available"] - response["used"])}')
        name = st.sidebar.selectbox("TASK", ('Summarization', 'TextGeneration', 'Question Answering',
                                             'FILL MASK', 'Backlink'))
        st.title(f"{name}")
        if name == 'Summarization':
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            summarization(API_URL, headers)
        elif name == "TextGeneration":
            API_URL = "https://api-inference.huggingface.co/models/gpt2"
            TextGeneration(API_URL, headers)
        elif name == "Question Answering":
            API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
            QuestionAnswering(API_URL, headers)
        elif name == 'FILL MASK':
            API_URL = "https://api-inference.huggingface.co/models/bert-base-uncased"
            FILL_MASK(API_URL, headers)
            FILL_MASK_INFO()
        elif name == 'Backlink':
            Backlink()
        st.markdown('# `USAGE`')
    else:
        st.markdown('# SERVICE IS DOWN')


def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":

    # _max_width_()
    st.markdown("""
                <style>
                footer {visibility: hidden;}
                #MainMenu {visibility: hidden;}
                </style>
                """, unsafe_allow_html=True)
    # MainMenu {visibility: hidden;}
    # st.set_page_config(  # Alternate names: setup_page, page, layout
    #     layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    #     initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    #     page_title=None,  # String or None. Strings get appended with "• Streamlit".
    #     page_icon=None,  # String, anything supported by st.image, or None.
    # )
    # st.set_option('wideMode', True)

    main()
