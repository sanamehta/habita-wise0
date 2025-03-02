import streamlit as st
import openai
import time
import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv
import io
import json
from tools import handle_tool_call

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Tenant Assistant",
    page_icon="🏠",
    layout="centered"
)

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "run_id" not in st.session_state:
    st.session_state.run_id = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# Get API key and Assistant ID from environment variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
vapi_auth_token = os.getenv("VAPI_AUTH_TOKEN")

# Check for missing API keys
missing_keys = []
if not api_key:
    missing_keys.append("OPENAI_API_KEY")
if not assistant_id:
    missing_keys.append("ASSISTANT_ID")
if not perplexity_api_key:
    missing_keys.append("PERPLEXITY_API_KEY")
if not vapi_auth_token:
    missing_keys.append("VAPI_AUTH_TOKEN")

if missing_keys:
    st.error(f"Please set the following keys in your .env file: {', '.join(missing_keys)}")
else:
    # Initialize OpenAI client
    if "client" not in st.session_state:
        st.session_state.client = OpenAI(api_key=api_key)
        
        # Create a new thread if one doesn't exist
        if not st.session_state.thread_id:
            thread = st.session_state.client.beta.threads.create()
            st.session_state.thread_id = thread.id

# App title
st.title("Tenant Rights Assistant")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Files")
    uploaded_file = st.file_uploader("Upload rental agreement or evidence", 
                                    type=["pdf", "txt", "csv", "xlsx", "docx", "json", "png", "jpg", "jpeg"], 
                                    key="file_uploader")
    st.caption("Supported formats: PDF, TXT, Word, Excel, Images")

# Handle file upload from sidebar
if uploaded_file is not None and (
    "last_uploaded_file" not in st.session_state or 
    st.session_state.last_uploaded_file != uploaded_file.name
):
    file_description = f"Uploaded file: {uploaded_file.name}"
    
    # Upload file to OpenAI
    try:
        with st.sidebar.status("Uploading file..."):
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            # Upload file to OpenAI
            with open(tmp_path, "rb") as file_data:
                file = st.session_state.client.files.create(
                    file=file_data,
                    purpose="assistants"
                )
            
            # Clean up the temporary file
            os.unlink(tmp_path)
            
            # Attach file to the thread
            st.session_state.client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=f"I've uploaded a file named {uploaded_file.name}. Please analyze it.",
                file_ids=[file.id]
            )
            
            # Track which file was last uploaded to prevent re-uploading the same file
            st.session_state.last_uploaded_file = uploaded_file.name
            
            # Add file upload message to session state
            st.session_state.messages.append({"role": "user", "content": file_description})
            
            # Display file upload notification in chat
            with st.container():
                st.markdown(f"""
                <div class="chat-message user">
                    <div class="avatar">👤</div>
                    <div class="content">{file_description}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.sidebar.success(f"File {uploaded_file.name} uploaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error uploading file: {e}")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        role = message["role"]
        content = message["content"]
        st.markdown(f"""
        <div class="chat-message {role}">
            <div class="avatar">
                {"👤" if role == "user" else "🤖"}
            </div>
            <div class="content">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)

# User input for chat
user_input = st.chat_input("Type your message here...")

# Process user input
if user_input and api_key and assistant_id:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.container():
        st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar">👤</div>
            <div class="content">{user_input}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display assistant "thinking" message
    with st.container():
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(f"""
        <div class="chat-message assistant">
            <div class="avatar">🤖</div>
            <div class="content">Thinking...</div>
        </div>
        """, unsafe_allow_html=True)
    
    try:
        # Add the user message to the thread
        st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_input
        )
        
        # Run the assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id
        )
        st.session_state.run_id = run.id
        
        # Poll for the run to complete
        max_attempts = 30  # Add a maximum number of polling attempts
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            run_status = st.session_state.client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=st.session_state.run_id
            )
            
            # Check if run requires action (function calling)
            if run_status.status == "requires_action":
                try:
                    tool_outputs = []
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        # Display function call in chat as a system message
                        tool_call_msg = f"🔧 Using tool: {function_name}({', '.join([f'{k}={v}' for k,v in function_args.items()])})"
                        thinking_placeholder.markdown(f"""
                        <div class="chat-message system">
                            <div class="avatar">🤖</div>
                            <div class="content">{tool_call_msg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Execute the function
                        function_response = handle_tool_call(tool_call)
                        
                        # Display function result
                        result_msg = f"Tool result: {str(function_response)[:200]}..." if len(str(function_response)) > 200 else f"Tool result: {function_response}"
                        thinking_placeholder.markdown(f"""
                        <div class="chat-message system">
                            <div class="avatar">🔧</div>
                            <div class="content">{result_msg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add the result to tool outputs
                        tool_outputs.append({
                            "tool_call_id": tool_call.id,
                            "output": str(function_response)
                        })
                    
                    # Submit the outputs back to the assistant
                    st.session_state.client.beta.threads.runs.submit_tool_outputs(
                        thread_id=st.session_state.thread_id,
                        run_id=st.session_state.run_id,
                        tool_outputs=tool_outputs
                    )
                    
                    # Reset attempt counter after successful tool call
                    attempt = 0
                    
                except Exception as e:
                    thinking_placeholder.error(f"Tool execution failed: {str(e)}")
                    break
            
            elif run_status.status == "completed":
                break
            elif run_status.status == "failed":
                thinking_placeholder.error(f"Run failed: {run_status.last_error}")
                break
            elif run_status.status == "expired" or run_status.status == "cancelled":
                thinking_placeholder.error(f"Run {run_status.status}")
                break
            
            # Add a timeout between polling attempts
            time.sleep(2)
        
        # Check if we exceeded maximum attempts
        if attempt >= max_attempts:
            thinking_placeholder.error("The assistant took too long to respond. Please try again.")
        
        # Get messages
        messages = st.session_state.client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )
        
        # Extract the latest assistant message
        for message in messages.data:
            if message.role == "assistant" and message.id not in [m.get("id") for m in st.session_state.messages if m.get("id")]:
                assistant_response = message.content[0].text.value
                message_data = {
                    "role": "assistant", 
                    "content": assistant_response,
                    "id": message.id
                }
                st.session_state.messages.append(message_data)
                
                # Replace the "thinking" message with the actual response
                thinking_placeholder.markdown(f"""
                <div class="chat-message assistant">
                    <div class="avatar">🤖</div>
                    <div class="content">{assistant_response}</div>
                </div>
                """, unsafe_allow_html=True)
                break
                
    except Exception as e:
        thinking_placeholder.error(f"Error: {e}")
elif user_input:
    st.warning("Missing API key or Assistant ID in .env file")



# Footer
st.markdown("---")
