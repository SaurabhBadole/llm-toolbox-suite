import os
import streamlit as st
import base64
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack import Pipeline
from haystack.document_stores.in_memory import InMemoryDocumentStore
from assemblyai_haystack.transcriber import AssemblyAITranscriber
from haystack.document_stores.types import DuplicatePolicy
from haystack.utils import ComponentDevice
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from time import sleep
import requests


def audiovideomodule():
    
    with st.sidebar:
        st.caption("### :orange[Welcome to Audio/Video Transcriber!]")
        st.caption("Effortlessly transcribe, analyze, and chat with multi-speaker audio/video conversations.")

        ASSEMBLYAI_API_KEY = st.text_input("Enter your ASSEMBLYAI_API_KEY: ", type="password")
        st.markdown("[Get your your AssemblyAI API key ](https://www.assemblyai.com/app/account)")

        HF_API_TOKEN = st.text_input("Enter your HF_API_TOKEN: ", type="password")
        st.markdown("[Get your Hugging Face API key](https://huggingface.co/settings/tokens)")


    st.sidebar.caption("""
    

    ### Get Started
    1. **Enter your API Keys**: To begin, please enter your AssemblyAI API key and Hugging Face API token above.
    2. **Upload Your Audio/Video Files**: Easily upload your files for transcription.
    3. **Transcribe and Analyze**: Automatically transcribe and analyze your multi-speaker conversations.
    4. **Chat with Transcriptions**: Engage in interactive chats based on the transcribed content.

    ### Privacy Notice
    - Your API keys are stored securely during your session and are not shared with anyone.
    - Uploaded files and transcriptions are handled with care to ensure your privacy.

    :rainbow[Enhance your transcription experience with our powerful tools!]
    """)


    def get_api_keys():
        os.environ["ASSEMBLYAI_API_KEY"] = ASSEMBLYAI_API_KEY
        os.environ["HF_API_TOKEN"] = HF_API_TOKEN
        return ASSEMBLYAI_API_KEY, HF_API_TOKEN

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    # Set up Streamlit interface
    st.title("Audio/Video Transcriber")
    st.caption("**Effortlessly transcribe, analyze, and chat with multi-speaker audio/video conversations**")

    # Get API keys
    ASSEMBLYAI_API_KEY, HF_API_TOKEN = get_api_keys()

    # File uploader
    uploaded_file = st.file_uploader("Upload Audio/Video File", type=["mp3", "mp4", "wav", "m4a"])

    transcript_text = ""

    # Check if a file is uploaded and API keys are provided
    if uploaded_file is not None and ASSEMBLYAI_API_KEY and HF_API_TOKEN:
        with open("temp_file", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Initialize components
        speaker_document_store = InMemoryDocumentStore()
        transcriber = AssemblyAITranscriber(api_key=ASSEMBLYAI_API_KEY)
        speaker_splitter = DocumentSplitter(split_by="sentence", split_length=10, split_overlap=1)
        speaker_embedder = SentenceTransformersDocumentEmbedder(device=ComponentDevice.from_str("cpu"))
        speaker_writer = DocumentWriter(speaker_document_store, policy=DuplicatePolicy.SKIP)

        # Create the indexing pipeline
        indexing_pipeline = Pipeline()
        indexing_pipeline.add_component(instance=transcriber, name="transcriber")
        indexing_pipeline.add_component(instance=speaker_splitter, name="speaker_splitter")
        indexing_pipeline.add_component(instance=speaker_embedder, name="speaker_embedder")
        indexing_pipeline.add_component(instance=speaker_writer, name="speaker_writer")
        
        indexing_pipeline.connect("transcriber.speaker_labels", "speaker_splitter")
        indexing_pipeline.connect("speaker_splitter", "speaker_embedder")
        indexing_pipeline.connect("speaker_embedder", "speaker_writer")

        # Transcribe the file
        st.write("Transcribing the file...")
        bar = st.progress(0)

        result = indexing_pipeline.run(
            {
                "transcriber": {
                    "file_path": "temp_file",
                    "summarization": None,
                    "speaker_labels": True
                },
            }
        )
        bar.progress(50)
        st.success("Transcription complete!")

        # # Extract the transcript text
        # transcript_docs = speaker_document_store.get_all_documents_generator()
        # transcript_text = "\n".join([doc.content for doc in transcript_docs])

        bar.progress(100)

        # Provide options for downloading or interacting with the transcript
        st.header('Output')
        tab1, tab2 = st.tabs(["Download Transcript", "Chat with Transcript"])

        with tab1:
            st.write("Download the transcribed text:")
            b64 = base64.b64encode(transcript_text.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="transcript.txt">Download Transcript</a>'
            st.markdown(href, unsafe_allow_html=True)

        with tab2:
            st.write("Ask questions about the transcript:")

            open_chat_prompt = """
            GPT4 Correct User: You will be provided with a transcription of a recording with each sentence or group of sentences attributed to a Speaker by the word "Speaker" followed by a letter representing the person uttering that sentence. Answer the given question based on the given context.
            If you think that given transcription is not enough to answer the question, say so.

            Transcription:
            {% for doc in documents %}
            {% if doc.meta["speaker"] %} Speaker {{doc.meta["speaker"]}}: {% endif %}{{doc.content}}
            {% endfor %}
            Question: {{ question }}

            GPT4 Correct Assistant:
            """
            
            retriever = InMemoryEmbeddingRetriever(speaker_document_store)
            text_embedder = SentenceTransformersTextEmbedder(device=ComponentDevice.from_str("cpu"))
            answer_generator = HuggingFaceAPIGenerator(
                api_type="serverless_inference_api",
                api_params={"model": "openchat/openchat-3.5-0106"},
                generation_kwargs={"max_new_tokens":500}
            )
            prompt_builder = PromptBuilder(template=open_chat_prompt)

            speaker_rag_pipe = Pipeline()
            speaker_rag_pipe.add_component("text_embedder", text_embedder)
            speaker_rag_pipe.add_component("retriever", retriever)
            speaker_rag_pipe.add_component("prompt_builder", prompt_builder)
            speaker_rag_pipe.add_component("llm", answer_generator)
            
            speaker_rag_pipe.connect("text_embedder.embedding", "retriever.query_embedding")
            speaker_rag_pipe.connect("retriever.documents", "prompt_builder.documents")
            speaker_rag_pipe.connect("prompt_builder.prompt", "llm.prompt")

            question = st.text_input("Enter your question:", "")

            if st.button("Get Answer") and question:
                result = speaker_rag_pipe.run({
                    "prompt_builder": {"question": question},
                    "text_embedder": {"text": question},
                    "retriever": {"top_k": 10}
                })
                st.write(result["llm"]["replies"][0])

if __name__ == "__main__":
    audiovideomodule()
