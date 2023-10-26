
import os
import streamlit as  st
import pandas as pd
from langchain.llms import AzureOpenAI
from pandasai import PandasAI
from dotenv import load_dotenv
from langchain.agents import create_csv_agent


load_dotenv()
os.environ["OPENAI_API_BASE"] = os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://aoiaipsi.openai.azure.com/'

os.environ["OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"] = 'f769445c82844edda56668cb92806c21'

os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"] = "2023-07-01-preview" #"2023-03-15-preview"

os.environ["OPENAI_API_TYPE"] = "azure"

AZURE_OPENAI_NAME = 'gpt-35-turbo-0301'

#openai_api_key = os.getenv('OPENAI_API_KEY')

def chat_with_csv(df,prompt):
    llm = AzureOpenAI(deployment_name=AZURE_OPENAI_NAME, temperature=0)

    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df,prompt=prompt)
    print(result)
    return result
    

st.set_page_config(layout="wide")

st.title("Chat with csv app3")
input_csv = st.sidebar.file_uploader("Upload your csv file",type='csv')

if input_csv is not None:
    col1,col2 = st.columns([1,1])
    with col1:
        st.info("DataFrame of first 10 data")
        data = pd.read_csv(input_csv)
        st.dataframe(data.head(10))
        
    
    with col2:
        st.info("Chat with")
        input_text = st.text_area("Enter your query")
        if input_text is not None:
            if st.button("chat with csv"):
                st.spinner("Generating answer...")
                st.info("your query:" + input_text)
                result = chat_with_csv(data,input_text)
                st.success(result)
                           
