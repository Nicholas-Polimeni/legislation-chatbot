import requests
import json
import ast
import re

import streamlit as st


def query_llm(query):
    url = "https://us-east4-legistlation-llm.cloudfunctions.net/llm-backend"
    data = {"query": query}
    response = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    ).json()
    return response["answer"], response["context"]


def main():
    st.set_page_config(layout="wide", page_title="Legislation Chatbot")
    left, right = st.columns(2, gap="large")
    answer = None

    with left:
        st.title("US Legislation Chatbot")
        st.subheader("Enter a query about US legislation")
        user_input = st.text_input("Input", label_visibility="hidden")
        if user_input:
            with st.spinner(
                "Please wait while we analyze thousands of documents (average response time: <10 sec)..."
            ):
                answer, context = query_llm(user_input)
        st.divider()
        st.write(
            """
            ### What is this?
            An intelligent, ChatGPT-like chatbot for asking about US legislation, built on
            cutting-edge LLMs and a database of thousands of Congressional documents. It is
            also accessible as an API.

            ### Why?
            Federal legislation impacts the entire nation, but there are hundreds
            of thousands of documents to sift through. Unfortunately, that makes it
            possible to hide important changes from the people. Use it to learn more about
            issues you care about or even as a research assistant.

            ### How?
            Utilizing the Congress API, sentence transformers, Google Cloud functions, and
            built off of Anthropic's Claude-2 (shout-out to Anthropic for
            providing an API key!), we've created a complex retrieval-augmented generative AI to answer your
            queries.

            ### How do I use this?
            Try to ask about bills related to a topic you care about, ask for details about
            a specific bill, or anything you think is important! **Power to the people :fist:**

            **More info** [here](https://devpost.com/software/legislation-llm), including potential future features (like notifications
            for topics you care about)!
            
            **Authors: [Nicholas Polimeni](https://www.linkedin.com/in/nickpolimeni/), 
            [Faris Durrani](https://www.linkedin.com/in/farisdurrani/)**
            """
        )

    with right:
        if answer:
            context = [ast.literal_eval(item) for item in context]
            st.header("Answer")
            st.write(answer)
            st.write("")
            st.subheader("Related Bills and Sub-sections")
            for bill in context:
                for key, val in bill.items():
                    key = key.replace(".txt", "").upper()

                    exp = r"[^\w\n .()]+"
                    val = re.sub(exp, "", val)

                    with st.expander(f"BILL {key}"):
                        st.text(val)


if __name__ == "__main__":
    main()
