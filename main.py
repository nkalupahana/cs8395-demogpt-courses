import streamlit as st
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.document_loaders import *
from langchain.chains.summarize import load_summarize_chain
import tempfile
from langchain.docstore.document import Document

st.title("Class Suggester")

major = st.text_input("Enter your major")
interests = st.text_input("Enter your interests (separated by commas)")

def courseAdvisor(major, interests):
    chat = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0.7
    )
    system_template = """You are an academic advisor helping students find interesting courses based on their major and interests."""
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = """Based on your major '{major}' and interests '{interests}', please generate a list of interesting courses for the student."""
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    result = chain.run(major=major, interests=interests)
    return result

if st.button("Submit"):
    if major and interests:
        course_list = courseAdvisor(major, interests)
        st.markdown(course_list)