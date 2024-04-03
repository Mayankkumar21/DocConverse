import shutil
import subprocess
from flask import Flask, jsonify, render_template, request
import os
from werkzeug.utils import secure_filename
import requests,json,os

app = Flask(__name__)
file_name = ''
conversation_history = []

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global file_name
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_name = secure_filename(file.filename)
    # Define the destination folder
    destination_folder = 'source_documents'
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    # Save the file to the destination folder
    file_path = os.path.join(destination_folder, file_name)
    file.save(file_path)
    return 'File uploaded successfully', 200

@app.route('/chat',methods=['GET','POST'])
def chat_page():
    return render_template('index.html')

@app.route('/generate-response', methods=['POST'])
def generate_response():
    print("filename is", file_name)
    data = request.get_json()
    prompt = data['prompt']

    # Execute ingest.py
    subprocess.run(['python3', 'ingest.py'])

    # Execute privateGPT.py using Popen
    process = subprocess.Popen(['python3', 'privateGPT.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)

    # Send prompt to privateGPT.py and capture responses
    actual_response = ''
    try:
        # Send prompt to privateGPT.py
        process.stdin.write(prompt + '\n')
        process.stdin.flush()

        # Read response from privateGPT.py
        while True:
            response = process.stdout.readline()
            if not response:
                break
            actual_response += response.strip() + '\n'
    except (BrokenPipeError, IOError):
        pass  # Ignore BrokenPipeError and IOError

    # Check if privateGPT.py exited without errors
    if process.returncode == 0:
        return jsonify({'response': actual_response.strip()})
    else:
        error_message = process.stderr.read().strip()
        return jsonify({'error': error_message}), 500


if __name__ == '__main__':
    app.run(debug=True)
