from openai import OpenAI
import streamlit as st
import json
from datetime import datetime
import base64
from fpdf import FPDF

# Sidebar configuration
with st.sidebar:
    st.title(":orange[Welcome to ChatBuddy!]")
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

st.sidebar.caption("""
### Get Started
1. **Enter your OpenAI API Key**: To start chatting with ChatBuddy, you'll need to enter your OpenAI API key.
2. **Chat with ChatBuddy**: Once you've entered your API key, you can start a conversation with ChatBuddy. Ask questions, seek advice, or just chat!
3. **Download Your Conversation**: After your chat session, you have the option to download the entire conversation in PDF format.

### How to Enter Your API Key
- Paste your OpenAI API key in the input box below.
- Click on "Submit chat query" to validate and start your session.

### Privacy Notice
- Your API key is stored securely during your session and is not shared with anyone.
- Conversations are stored temporarily and can be downloaded in PDF format for your records.

### Tips
- Make sure your API key is active and has sufficient quota.
- For best results, be clear and concise with your questions.

:rainbow[Enjoy your conversation with ChatBuddy!]
""")



# Main chat interface
st.markdown(
    """
    <style>
        .chat-header {
            font-size: 2em;
            font-weight: bold;
            color: #333;
            animation: fadeIn 2s;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .chat-input {
            margin-top: 20px;
        }
        .download-button {
            background-color: #1D1D1D;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            border-radius: 8px;
            cursor: pointer;
        }
        .download-button:hover {
            background-color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Your ChatBuddy🙋🏻💭")
st.caption("####  :rainbow[**ChatBuddy powered by Streamlit x OpenAI**]")

# Initialize session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hey Buddy! How can I help you today?"}]

# Display messages in chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if prompt := st.chat_input(placeholder="Type your message..."):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Simulate loading state
    with st.spinner('Generating response...'):
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

# Function to download chat history as PDF
def download_chat_history_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            pdf.set_text_color(0, 0, 255)  # Blue for user messages
            pdf.multi_cell(0, 10, f'User: {msg["content"]}')
        else:
            pdf.set_text_color(255, 0, 0)  # Red for assistant messages
            pdf.multi_cell(0, 10, f'Assistant: {msg["content"]}')
    
    pdf_output = f"chat_history/chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(pdf_output)
    
    with open(pdf_output, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{pdf_output}">Download PDF</a>'
    return href

# Download button
st.markdown('<div class="chat-input">', unsafe_allow_html=True)
st.markdown(f'<button class="download-button">{download_chat_history_pdf()}</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Clear chat button
if st.button('Clear Chat'):
    st.session_state["messages"] = [{"role": "assistant", "content": ""}]
    st.experimental_rerun()
