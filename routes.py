from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
import ast

def process_intermediate_steps(steps):
    messages = []

    for step in steps:
        # Convert the string representation of the tuple back into a tuple
        step_tuple = ast.literal_eval(step)

        action = step_tuple[0]['tool']
        action_input = step_tuple[0]['tool_input']
        observation = step_tuple[1]

        messages.append({
            'type': 'action',
            'content': f"Action: {action}, Input: {action_input}"
        })
        messages.append({
            'type': 'observation',
            'content': observation
        })

    return messages

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    # Extract question from the form data
    question = request.form['question']

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
        chat_messages = process_intermediate_steps(backend_response['intermediate_steps'])
        
        chat_messages.append({
            'type': 'final-response',
            'content': backend_response['nl_response']
        })
        
        return render_template('chat.html', chat_messages=chat_messages)
    else:
        return "Error communicating with the server."
if __name__ == '__main__':
    app.run(debug=True)
