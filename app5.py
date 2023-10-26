import streamlit as st
import os
from streamlit_chat import message
from langchain.agents import create_csv_agent
from langchain.llms import AzureOpenAI

os.environ["OPENAI_API_BASE"] = os.environ["AZURE_OPENAI_ENDPOINT"] = 'https://aoiaipsi.openai.azure.com/'

os.environ["OPENAI_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"] = 'f769445c82844edda56668cb92806c21'

os.environ["OPENAI_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"] = "2023-07-01-preview" #"2023-03-15-preview"

os.environ["OPENAI_API_TYPE"] = "azure"

AZURE_OPENAI_NAME = 'gpt-35-turbo-0301'

st.header("CSV Reader ")
# File uploader function
user_csv = st.file_uploader("Upload your CSV file", type="csv")

def get_text():
   input_text = st.text_input("Enter your question")
   return input_text

# Function to generate response to user question
def get_response(query):
   with st.spinner(text="In progress"):
       prompt = (
        """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            There can only be two types of chart, "bar" and "line".

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}

            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}

            Return all output as a string.

            All strings in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query: 
            """
         + query
    )
    # run the prompt through the agent
       response = agent.run(prompt)
    #response = text_analytics_client.analyze_sentiment(documents=["This is a great product."])
    
    # convert the response to the string
       return response.__str__()

   
       #response = agent.run(query)
   #return response
if user_csv is not None:
    
   # Get the user input
   user_input = get_text()
   # Initialize the OpenAI model
   llm = AzureOpenAI(deployment_name=AZURE_OPENAI_NAME, temperature=0)
   # Initialize the agent
   agent = create_csv_agent(llm, user_csv, verbose=True)
   # Initialize the session state
   if 'generated' not in st.session_state:
       st.session_state['generated'] = ["Yes, you can!"]
   if 'past' not in st.session_state:
       st.session_state['past'] = ["Can I ask anything about my csv file?"]
   if user_input:
       st.session_state.past.append(user_input)
       # Get the chatbot response
       response = get_response(user_input)
       st.session_state.generated.append(response)
   # Displaying the chat
   if len(st.session_state['generated']) != 1:
       for i in range(1,len(st.session_state['generated'])):
           message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
           message(st.session_state['generated'][i], key=str(i))
           
