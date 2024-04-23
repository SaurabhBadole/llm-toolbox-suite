import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import base64
import tempfile
import os
from htmltemplates import *
from datetime import datetime



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = NVIDIAEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatNVIDIA(model="meta/llama3-70b-instruct")
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def save_chat_session(chat_history):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        for message in chat_history:
            temp_file.write(message.content.encode("utf-8") + b"\n")
        return temp_file.name

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def download_pdf(chat_history):
    pdf_filename = "chat_session.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    is_user_message = True
    for message in chat_history:
        if is_user_message:
            paragraph = Paragraph(message.content, styles["Normal"])
        else:
            paragraph = Paragraph(message.content, styles["Normal"])
            paragraph.textColor = colors.blue
        story.append(paragraph)
        story.append(Spacer(1, 12))
        is_user_message = not is_user_message

    doc.build(story)
    with open(pdf_filename, "rb") as pdf_file:
        pdf_contents = pdf_file.read()
    return pdf_contents

##---------------------------------------------------------------------------
## V1 without using the file rename format.

# def main():
#     load_dotenv()
#     st.set_page_config(page_title="Your Personalized Document Chatbot", page_icon=":books:")

#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = None

#     st.header("Your Personalized Document Chatbot :books:")
#     st.markdown(css, unsafe_allow_html=True)  # Applying custom CSS

#     user_question = st.text_input("Ask a question about your documents:")
#     if user_question:
#         handle_userinput(user_question)

#     with st.sidebar:
#         st.subheader("Your documents")
#         pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
#         if st.button("Process"):
#             with st.spinner("Processing"):
#                 raw_text = get_pdf_text(pdf_docs)
#                 text_chunks = get_text_chunks(raw_text)
#                 vectorstore = get_vectorstore(text_chunks)
#                 st.session_state.conversation = get_conversation_chain(vectorstore)
#                 st.success("Vector Store DB Is Ready")

#     if st.session_state.chat_history is not None:
#         pdf_contents = download_pdf(st.session_state.chat_history)
#         st.download_button(
#             "Download above Conversation",
#             pdf_contents,
#             "chat_session.pdf",
#             "application/pdf",
#             key="download"
#         )


##---------------------------------------------------------------------------

def generate_file_name():
    now = datetime.now()
    return now.strftime("chat_session_%Y%m%d_%H%M%S.pdf")

def save_pdf_to_folder(pdf_content, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = generate_file_name()
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "wb") as f:
        f.write(pdf_content)
    return file_path

def main():
    load_dotenv()
    st.set_page_config(page_title="Your Personalized Document Chatbot", page_icon=":books:")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Your Personalized Document Chatbot :books:")
    st.caption("**Harness the power of Retrieval-Augmented Generation to answer questions from your documents with AI precision and efficiency.**")
    st.markdown(css, unsafe_allow_html=True)  # Applying custom CSS

    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.sidebar.caption(""" ### :orange[Welcome to DocAI Q&A!] """)
        st.sidebar.caption("""Harness the power of Retrieval-Augmented Generation to answer questions from your documents with AI precision and efficiency.""")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.success("Vector Store DB Is Ready")


    
    st.sidebar.caption("""
    ### How to Use
    1. **Upload Your Documents**: Easily upload your documents to the app.
    2. **Ask Questions**: Query the content of your documents using natural language.
    3. **Get Accurate Answers**: Receive precise and relevant answers generated by AI.
    4. **Download Conversations**: Save your query and answer sessions by downloading them in PDF format.

    :rainbow[Enjoy a seamless and intelligent way to interact with your documents!]
    """)


    if st.session_state.chat_history is not None:
        pdf_contents = download_pdf(st.session_state.chat_history)
        save_folder = os.path.join(os.getcwd(), "DocAI_history")
        saved_file_path = save_pdf_to_folder(pdf_contents, save_folder)
        
        st.download_button(
            "Download above Conversation",
            pdf_contents,
            saved_file_path,
            "application/pdf",
            key="download"
        )
if __name__ == '__main__':
    main()
