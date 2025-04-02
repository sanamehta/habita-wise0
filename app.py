from flask import Flask, render_template, request, jsonify, send_file
import openai
import time
import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import io
import json
from tools import handle_tool_call
from werkzeug.utils import secure_filename
import base64

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.urandom(24)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Get API key and Assistant ID from environment variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
vapi_auth_token = os.getenv("VAPI_AUTH_TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Store sessions in memory (in production, use a proper database)
sessions = {}

def create_new_session():
    thread = client.beta.threads.create()
    return {
        'thread_id': thread.id,
        'messages': [],
        'last_uploaded_file': None
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        session_id = str(len(sessions))
        sessions[session_id] = create_new_session()
    
    session = sessions[session_id]
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Add user message to chat
        session['messages'].append({"role": "user", "content": user_input})
        
        # Add the user message to the thread
        client.beta.threads.messages.create(
            thread_id=session['thread_id'],
            role="user",
            content=user_input
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=session['thread_id'],
            assistant_id=assistant_id
        )
        
        # Poll for the run to complete
        max_attempts = 30
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            run_status = client.beta.threads.runs.retrieve(
                thread_id=session['thread_id'],
                run_id=run.id
            )
            
            if run_status.status == "requires_action":
                try:
                    tool_outputs = []
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        # Execute the function
                        function_response = handle_tool_call(tool_call)
                        
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": str(function_response)
                        })
                    
                    # Submit the outputs back to the assistant
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=session['thread_id'],
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    
                    attempt = 0
                    
                except Exception as e:
                    return jsonify({'error': f"Tool execution failed: {str(e)}"}), 500
            
            elif run_status.status == "completed":
                break
            elif run_status.status in ["failed", "expired", "cancelled"]:
                return jsonify({'error': f"Run {run_status.status}"}), 500
            
            time.sleep(2)
        
        if attempt >= max_attempts:
            return jsonify({'error': "The assistant took too long to respond"}), 500
        
        # Get messages
        messages = client.beta.threads.messages.list(
            thread_id=session['thread_id']
        )
        
        # Extract the latest assistant message
        for message in messages.data:
            if message.role == "assistant" and message.id not in [m.get("id") for m in session['messages'] if m.get("id")]:
                assistant_response = message.content[0].text.value
                message_data = {
                    "role": "assistant", 
                    "content": assistant_response,
                    "id": message.id
                }
                session['messages'].append(message_data)
                return jsonify({
                    'response': assistant_response,
                    'session_id': session_id
                })
        
        return jsonify({'error': "No response from assistant"}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    session_id = request.form.get('session_id')
    
    if not session_id or session_id not in sessions:
        session_id = str(len(sessions))
        sessions[session_id] = create_new_session()
    
    session = sessions[session_id]
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp_file:
                tmp_file.write(file.read())
                tmp_path = tmp_file.name
            
            # Upload file to OpenAI
            with open(tmp_path, "rb") as file_data:
                uploaded_file = client.files.create(
                    file=file_data,
                    purpose="assistants"
                )
            
            # Clean up the temporary file
            os.unlink(tmp_path)
            
            # Attach file to the thread
            client.beta.threads.messages.create(
                thread_id=session['thread_id'],
                role="user",
                content=f"I've uploaded a file named {file.filename}. Please analyze it.",
                file_ids=[uploaded_file.id]
            )
            
            # Track which file was last uploaded
            session['last_uploaded_file'] = file.filename
            
            return jsonify({
                'message': f"File {file.filename} uploaded successfully!",
                'session_id': session_id
            })
            
        except Exception as e:
            return jsonify({'error': f"Error uploading file: {str(e)}"}), 500
    
    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'csv', 'xlsx', 'docx', 'json', 'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True,port=5003)
