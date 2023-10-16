

import streamlit as st

import huggingface

import matplotlib.pyplot as plt

 

# Set your OpenAI API key

api_key = "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"

 

# Function to generate data visualization

def generate_visualization(data):

    # Example: Create a bar chart from the data

    categories = data['categories']

    values = data['values']

 

    plt.bar(categories, values)

    plt.xlabel('Categories')

    plt.ylabel('Values')

    plt.title('Data Visualization')

 

    st.pyplot()

 

# Function to process user input

def process_user_input(user_input):

    # Call the OpenAI API to understand the user's request

    response = huggingface.Completion.create(

        engine="Uzair1/text-chat-davinci-002-20221122",

        prompt=user_input,

        max_tokens=50,

        api_key=api_key

    )

    user_request = response.choices[0].text.strip()

 

    # You'll need to parse the user's request to extract structured data

    # In this example, we assume data is provided as a dictionary

    data = {

        'categories': ['A', 'B', 'C'],

        'values': [10, 20, 15]

    }

 

    return data

 

# Streamlit app

st.title("Data Visualization Chatbot")

 

user_input = st.text_input("Enter your data and request:")

 

if st.button("Generate Visualization"):

    if user_input:

        # Process user input

        data = process_user_input(user_input)

 

        # Generate and display the data visualization

        generate_visualization(data)

    else:

        st.warning("Please enter a valid user request.")

 

if __name__ == "__main__":

    huggingface.api_key = api_key  # Set the OpenAI API key

 

    # Run the Streamlit app

    st.set_option('deprecation.showPyplotGlobalUse', False)

#plt.bar - Insurance Resources and Information.

#plt.bar is your first and best source for all of the information you’re looking for. From general topics to more of what you would expect to find here, plt.bar has it all. We hope you find what you...
