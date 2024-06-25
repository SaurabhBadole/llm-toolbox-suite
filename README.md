# LLM Toolbox Suite

Welcome to the **LLM Toolbox Suite**, a powerful and versatile set of tools designed to harness the capabilities of large language models for various productive tasks. This suite is built using Streamlit and integrates APIs from OpenAI, AssemblyAI, and NVIDIA.

## Overview

**LLM Toolbox Suite** is designed to provide users with an interactive and user-friendly interface to **chat with AI, chat with multiple Documents, chat with WebSearch, effortlessly transcribe, analyze, and chat with multi-speaker audio/video conversations amd even generate Meeting of Minutes with main themes!** 

The suite includes:

- **ChatBuddy** : An interactive chatbot powered by OpenAI's GPT and Streamlit.![Chatbuddy](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/f5c2e146-005f-4df5-95bc-1d5e54a2f5d8)



- **RAG DocAI Q&A**: Harness the power of Retrieval-Augmented Generation to answer questions from your documents with AI precision and efficiency.![RAG_DocAI_Q A](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/1cdb4435-1c0a-47a2-b257-62a80bc0f3e9)


- **Chat with Search**: Enhance your conversations with integrated search capabilities, providing instant answers and information from the web.![Chat_with_search](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/4111a594-d53e-4b65-bd8b-2c9d4fc4c9f4)



- **AudioVideo Transcriber**: Effortlessly transcribe, analyze, and chat with multi-speaker audio/video conversations.![AudioVideo_Transcriber](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/0a1067e1-d72b-45b4-95d6-f5edcabedb4c)



- **YouTube Transcriber**: Easily convert YouTube videos into text with detailed transcripts for better comprehension and analysis.![YouTube_Transcriber](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/9fe1ebec-5894-4ae3-8f32-835f30d2f70f)



- **MoM Generator**: Transform your meeting recordings into detailed, categorized summaries and downloadable transcripts effortlessly.![MoM_Generator](https://github.com/SaurabhBadole/llm-toolbox-suite/assets/132877393/ac76befa-4552-43f4-ac8e-e70c63d12b3d)



## Features


- **Interactive and Responsive Design**: Enjoy a user-friendly and visually appealing interface.
- **API Integration**: Seamlessly integrates with OpenAI, AssemblyAI, and NVIDIA APIs.
- **Chat Interface**: Engage in conversations with an AI assistant for seamless interaction.
- **Retrieval-Augmented Generation (RAG)**: Leverage advanced AI to provide precise answers to questions from documents using retrieval-augmented generation techniques.
- **Integrated Search Capabilities**: Enhance conversations with instant access to web-based information and answers.
- **Audio/Video Transcription**: Effortlessly transcribe and analyze multi-speaker audio and video conversations.
- **YouTube Video Transcription**: Convert YouTube videos into detailed text transcripts for improved comprehension and analysis.
- **Meeting Summary Generation**: Automatically generate detailed, categorized summaries and downloadable transcripts from meeting audio recordings.
- **PDF Export**: Download your conversation as a PDF file.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- Streamlit
- OpenAI API Key
- AssemblyAI API Key
- NVIDIA API Key

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/SaurabhBadole/llm-toolbox-suite.git
    cd llm-toolbox-suite
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the root directory and adding your API keys:
    ```sh
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    HF_API_TOKEN=your_huggingface_api_token
    NVIDIA_API_KEY=your_nvidia_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

### Running the Application

Run the main file to start the application:
```sh
streamlit run Chatbuddy.py
```

## Project Structure

Here's an overview of the project's structure:

```
llm-toolbox-suite/
│
├──pages/
|  └──1_RAG_DocAI_Q&A.py              # application file for having conversation with an AI bot while can also download the conversation as PDF
|  └──2_Chat_with_search.py           # application file for having conversations with WebSearch
|  └──3_AudioVideo_Transcriber.py     # application file for transcribing, analyzing, and chatting with multi-speaker audio/video conversations
|  └──4_YouTube_Transcriber.py        # application file for convert YouTube videos into text with detailed transcripts
|  └──5_MoM_Generator.py              # application file for Meeting of Minutes generator with Main Themes and time stamps
├── .env                              # Environment variables
├── Chatbuddy.py                      # Main application file starting with main page ChatBuddy
├── htmltemplates.py                  # HTML templates for RAG DocAI Q&A Streamlit Interface
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
├── utils.py                          # Utility functions
├── chat_history/                     # Directory for saving chat history for ChatBuddy
├── DocAI_history/                    # Directory for saving DocAI RAG conversations
```

### Detailed Description of Files

- **pages/RAG_DocAI_Q&A.py**:
  - This file provides functionality for users to interact with an AI bot, allowing them to ask questions and receive detailed responses. Additionally, it includes an option to download the entire conversation as a PDF for record-keeping or review purposes.

- **pages/Chat_with_search.py**:
  - This file enables users to engage in conversations with an AI that has integrated web search capabilities. The AI can fetch and provide real-time information from the web, enhancing the quality and relevance of the responses.

- **pages/AudioVideo_Transcriber.py**:
  - This file is designed to handle audio and video files, transcribing the spoken content into text. It can analyze multi-speaker conversations, providing insights and the ability to chat about the content. It's ideal for reviewing and interacting with recorded meetings or interviews.

- **pages/YouTube_Transcriber.py**:
  - This file allows users to convert YouTube videos into text. It generates detailed transcripts, making it easier to analyze and extract information from video content. This can be useful for content creators, researchers, and anyone needing text versions of video material.

- **pages/MoM_Generator.py**:
  - This file is aimed at generating Minutes of Meetings (MoM). It extracts the main themes and provides timestamps, making it a valuable tool for summarizing meetings and ensuring that important points are documented and easily accessible. 
- **.env**: Stores API keys and other environment variables.
- **Chatbuddy.py**: The main Streamlit application file. Contains the core logic for the chat interface and PDF download functionality.
- **htmltemplates.py**: Defines the HTML and CSS templates used for styling the chat interface.
- **requirements.txt**: Lists all the required Python packages.
- **utils.py**: Contains utility functions for time conversion, file reading, and chat session management.
- **chat_history/**: Directory for saving chat history files.
- **DocAI_history/**: Directory for saving DocAI RAG conversations

## Usage

1. **Enter API Keys**: Start the application and enter your API keys for tools wherever the api key is asked in the sidebar.
2. **Chat with multiple tools**: Begin chatting with the AI assistant by typing your message and then download conversations in pdf format.
3. **Download Conversation**: After your session, download the chat history in PDF format.
4. **Download Transcripts**: After transcribing the YT videos, you can downlownload it in txt and SRT format.
5. **Clear Chat**: Use the 'Clear Chat' button to start a new session.


## Acknowledgments

- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [AssemblyAI](https://www.assemblyai.com/)
- [NVIDIA](https://www.nvidia.com/)

## Contact

For any inquiries, please contact [Saurabh Khushal Badole](mailto:saurabhbadole25.98@gmail.com).

---

