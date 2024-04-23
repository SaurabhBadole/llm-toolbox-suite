import streamlit as st

from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun

st.sidebar.caption("""
### :orange[Chat with search🔍]""")
st.sidebar.caption("""Enhance your conversations with integrated search capabilities, providing instant answers and information from the web.""")


with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="langchain_search_api_key_openai", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


st.sidebar.caption(""" 
### Get Started
1. **Enter your OpenAI API Key**: To start, please enter your OpenAI API key above.
2. **Chat and Search**: Engage in conversations and use the integrated search to get real-time information and answers.
3. **Enjoy Enhanced Interactions**: Experience more informative and dynamic conversations.


### Privacy Notice
- Your API key is stored securely during your session and is not shared with anyone.
- Conversations and search queries are handled with care to ensure your privacy.

:rainbow[Enhance your conversations with Chat with search!]
""")


st.title("Chat with search🔍")
st.caption("**Enhance your conversations with integrated search capabilities, providing instant answers and information from the web.**")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! I'm here to assist you by searching the web. What can I find for you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is the current exchange rate for USD to EUR?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        [search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
