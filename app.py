import streamlit as st
from langchain_core.prompts import PromptTemplate
from euriai import EuriaiLangChainLLM
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from io import StringIO

#LLM and key loading function
def load_LLM(api_key):
    
    llm = EuriaiLangChainLLM(api_key=api_key, model="gpt-4.1-nano",temperature=0.7, max_tokens=300)
    return llm


#Page title and header
st.set_page_config(page_title="AI Long Text Summarizer")
st.header("AI Long Text Summarizer")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("ChatGPT cannot summarize long texts. Now you can do it with this app.")

with col2:
    st.write("Created By Durgesh Singh")


#Input API Key
st.markdown("## Enter Your Euri API Key")

def get_api_key():
    input_text = st.text_input(label="API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="api_key_input", type="password")
    return input_text

api_key = get_api_key()




# Input
st.markdown("## Upload the text file you want to summarize")

uploaded_file = st.file_uploader("Choose a file", type="txt")


       
# Output
st.markdown("### Here is your Summary:")

if uploaded_file is not None:
    
    bytes_data = uploaded_file.getvalue()

    
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    string_data = stringio.read()
    

    file_input = string_data

    if len(file_input.split(" ")) > 20000:
        st.write("Please enter a shorter file. The maximum length is 20000 words.")
        st.stop()

    if file_input:
        if not api_key:
            st.warning('Please insert API Key. \
            Instructions [here](https://api.euron.one/api/v1/)', 
            icon="⚠️")
            st.stop()
    

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], 
        chunk_size=5000, 
        chunk_overlap=350
        )

    splitted_documents = text_splitter.create_documents([file_input])

    llm = load_LLM(api_key=api_key)

    summarize_chain = load_summarize_chain(
        llm=llm, 
        chain_type="map_reduce"
        )

    summary_output = summarize_chain.run(splitted_documents)

    st.write(summary_output)