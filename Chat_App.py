import streamlit as st
import requests
import ast
import re

def process_intermediate_steps(steps):
    messages = []

    for step in steps:
        match = re.match(r"\(AgentAction\(tool='(.*?)', tool_input='(.*?)',.*?\), '(.*?)'\)", step)

        if match:
            action, action_input, observation = match.groups()

            messages.append(f"Action: {action}, Input: {action_input}")
            messages.append(observation)
        else:
            # This will help you catch any strings that don't match the expected format
            messages.append(f"Unparsed step: {step}")

    return messages


def display_sql_results(result):
    columns = result['columns']
    rows = result['rows']

    st.write("SQL Results:")
    for column in columns:
        st.write(column)

    for row in rows:
        st.write(row)
def clean_message(message):
    # Remove newlines and tabs
    clean_msg = message.replace('\n', ' ').replace('\t', ' ')
    # Replace multiple consecutive spaces with a single space
    clean_msg = ' '.join(clean_msg.split())
    return clean_msg


def main():
    st.title("Chat with Database")
    
    # Define styles for chat bubbles
    st.markdown("""
    <style>
        .chat-message {
            margin: 10px;
            padding: 10px;
            border-radius: 10px;
        }

        .user-message {
            background-color: #e1ffc7;
            align-self: flex-start;
        }

        .agent-message {
            background-color: #f0f0f0;
            align-self: flex-end;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Input field for the question
    question = st.text_input("Your question:")
    
    # Button to send the question
    if st.button("Ask"):
        # Define db_alias (this is just an example, set it as required)
        db_alias = "any_alias"

        # API endpoint
        url = "http://localhost/api/v1/question"  # Note: Ensure the URL is correct

        # Data to be sent to the API
        data = {
            "question": question,
            "db_alias": db_alias
        }

        response = requests.post(url, json=data)

        if response.status_code == 200:
            backend_response = response.json()
            chat_messages_list = process_intermediate_steps(backend_response['intermediate_steps'])
            
            # Display the SQL query
            chat_messages_list.append(f"SQL Query: {backend_response['sql_query']}")
            
            # Display the natural language response
            chat_messages_list.append(backend_response['nl_response'])
            
            # Display user question
            st.markdown(f"<div class='chat-message user-message'>You: {question}</div>", unsafe_allow_html=True)

            # Display each message in chat_messages_list using the defined styles
            for message in chat_messages_list:
                cleaned_message = clean_message(message)
                st.markdown(f"<div class='chat-message agent-message'>Agent: {cleaned_message}</div>", unsafe_allow_html=True)
            
            # Display SQL results
            display_sql_results(backend_response['sql_query_result'])
            
            # Display other details
            st.write(f"Execution Time: {backend_response['exec_time']} seconds")
            st.write(f"Token Count: {backend_response['total_tokens']}")
            st.write(f"Total Cost: {backend_response['total_cost']}")
        else:
            st.markdown("<div class='chat-message agent-message'>Error communicating with the server.</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

