import streamlit as  st
from langchain.agents import create_csv_agent
from langchain.llms import AzureOpenAI
from pandasai import pd

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_BASE"] = os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://aoiaipsi.openai.azure.com/'

os.environ["OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"] = 'f769445c82844edda56668cb92806c21'

os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"] = "2023-07-01-preview" #"2023-03-15-preview"

os.environ["OPENAI_API_TYPE"] = "azure"

AZURE_OPENAI_NAME = 'gpt-35-turbo-0301'


def main():
    
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV(agent)")
    
    user_csv = st.file_uploader("upload your csv file", type = 'csv')
    
    if user_csv is not None:
        data = pd.read_csv(user_csv)
        st.dataframe(data.head(10))
        
        
        
        
        user_question= st.text_input("ASK YOUR QUESTION:")
        
        
        llm = AzureOpenAI(deployment_name=AZURE_OPENAI_NAME, temperature=0)

        agent = create_csv_agent(llm, user_csv,verbose=True)
        
        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            
            st.spinner("Generating response.....")
            st.write(response)


if __name__ == "__main__":
    main()
