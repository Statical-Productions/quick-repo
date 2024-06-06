# Imports
import gradio as gr
import requests
import uuid
import json
import os

# Variables
API_TOKEN = os.environ.get("API_TOKEN")

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_TOKEN}" }

# Functions
def https_predict(url, session_hash, fn_index, data, headers):
    session = session_hash if session_hash is not None else str(uuid.uuid4())
    try:
        response = requests.post(url, data=json.dumps({"data": data, "fn_index": fn_index, "session_hash": session}), headers=headers if headers is not None else {})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(e)
        raise

def generate(input):
    json_data = json.loads(input)
    data = https_predict(json_data[0], json_data[1], json_data[2], json_data[3], json_data[4])
    return data

# Initialize
with gr.Blocks() as main:
    with gr.Row():
        input = gr.Textbox(label="Input", lines=1)
        run = gr.Button("▶")
        output = gr.Textbox(label="Output", lines=1)

    run.click(generate, inputs=[input], outputs=[output])

main.launch(show_api=True)
