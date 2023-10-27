import streamlit as st
from langchain.agents import initialize_agent, Tool
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import AzureOpenAI
import pandas as pd
import os
from dotenv import load_dotenv
 
load_dotenv()
 
os.environ["OPENAI_API_BASE"] = os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://aoiaipsi.openai.azure.com/'
 
os.environ["OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"] = 'f769445c82844edda56668cb92806c21'
 
os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"] = "2023-03-15-preview"
 
os.environ["OPENAI_API_TYPE"] = "azure"
AZURE_OPENAI_NAME = 'gpt-35-turbo-0301'
 
def main():
    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV(agent)")
 
    user_csv = st.file_uploader("Upload your CSV file", type='csv', accept_multiple_files=True)
    
    data_list = []
    
    for f in user_csv:
        st.write(f)
        data = pd.read_csv(f)
        
        # Add a "prompt" column with your desired prompt
        data["prompt"] = """
        Let's decode the way to respond to the queries. The responses depend on the type of information requested in the query.
 
        1. If the query requires a table, format your answer like this:
           {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}
 
        2. For a bar chart, respond like this:
           {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
 
        3. If a line chart is more appropriate, your reply should look like this:
           {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}
 
        Note: We only accommodate two types of charts: "bar" and "line".
 
        4. For a plain question that doesn't need a chart or table, your response should be:
           {"answer": "Your answer goes here"}
 
        For example:
           {"answer": "The Product with the highest Orders is '15143Exfo'"}
 
 
        Return all output as a string. Remember to encase all strings in the "columns" list and data list in double quotes.
        For example: {"columns": ["Products", "Orders"], "data": [["51993Masc", 191], ["49631Foun", 152]]}
 
        Now, let's tackle the query step by step. Here's the query for you to work on:
        """
        
        data_list.append(data)
 
    df = pd.concat(data_list)
 
    if df is not None:
        user_question = st.text_input("ASK YOUR QUESTION:")
 
        llm = AzureOpenAI(deployment_name=AZURE_OPENAI_NAME, temperature=0)
 
        agent = create_pandas_dataframe_agent(llm, df, verbose=True)
 
        if user_question is not None and user_question != "":
            response = agent.run(user_question)
 
            st.spinner("Generating response.....")
            st.write(response)
 
if __name__ == "__main__":
    main()
