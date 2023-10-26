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


def get_text():
   input_text = st.sidebar.text_input("Enter your question")
   return input_text

# Function to generate response to user question
def get_response(query):
   with st.spinner(text="In progress"):
       response = agent.run(query)
   return response

st.header("CSV Reader ")
# File uploader function
user_csv = st.file_uploader("Upload your CSV file", type="csv")
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
           
def get_text():
   input_text = st.text_input("Enter your question")
   return input_text
