# Imports
import gradio as gr
import requests
import uuid
import json
import os

# Variables
API_TOKEN = os.environ.get("API_TOKEN")

hf_headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_TOKEN}" }

# Functions
def https_predict(url, session_hash, fn_index, data, headers):
    session = session_hash if session_hash is not None else str(uuid.uuid4())
    try:
        response = requests.post(url, data=json.dumps({"data": data, "fn_index": fn_index, "session_hash": session}), headers=headers if headers is not None else hf_headers or {})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(e)
        raise

def generate(input):
    json_data = json.loads(input)
    data = https_predict(*json_data)
    return json.dumps(data)

# Initialize
with gr.Blocks() as main:
    with gr.Row():
        input = gr.Textbox(label="Input", lines=1)
        submit = gr.Button("▶")
        output = gr.Textbox(label="Output", lines=1)

    submit.click(fn=generate, inputs=[input], outputs=[output], queue=False)

main.launch(show_api=True)
