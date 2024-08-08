# Preparing Lamini LLM compatible with Langchain

# Libraries
import lamini
from typing import Any, Dict, Iterator, List, Mapping, Optional
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk
from collections import deque
from langchain_core.messages import AIMessage,HumanMessage
from langchain.chains import ConversationChain

# Setting Environment
import os 
from dotenv import load_dotenv
load_dotenv()

lamini.api_key=os.getenv('LAMINI_API_KEY')
model_id = "c38c5762bd0e660709a3a1288dbedee647a437e58a5c48dab32d0f61f59f5601"


class CustomLaminiLLM(LLM):
    model_id: str

    def _call(self, prompt: str,context:str, stop: Optional[List[str]] = None, run_manager: Optional[CallbackManagerForLLMRun] = None, **kwargs: Any,) -> str:
        full_prompt = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        full_prompt += "You are a psychiatrist bot known as Thought Therapist for helping people with depression and stress. Keep your answers within 200 words. Put the following chat history in context:"
        full_prompt+=context
        full_prompt += "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        full_prompt += prompt
        full_prompt += "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        llm = lamini.Lamini(self.model_id)
        return (llm.generate(full_prompt))
    
    def _llm_type(self) -> str:
        return "custom"



llm = CustomLaminiLLM(model_id=model_id)




# Creating Streamlit App
import streamlit as st
import time 

# Messages re-run
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat history
if "message_queue" not in st.session_state:
    st.session_state.message_queue = deque()
    st.session_state.message_queue.append(AIMessage(content="Hi! How are you ?"))


with st.chat_message("assistant"):
        st.markdown('Hi! How are you ?')
        

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input

if prompt := st.chat_input("Message Thought Therapist"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Context Generation
    context = ""
    if st.session_state.message_queue:
        for chat in st.session_state.message_queue:
            if isinstance(chat, AIMessage):
                context += 'AI: '
            else:
                context += 'Human: '
            context += chat.content
            context += '\n'
    # Display assistant response in chat message container
    response = llm(prompt=prompt, context=context)
    def response_generator():
        for word in response.split():
            yield word + " "
            time.sleep(0.05)
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    st.session_state.messages.append({"role": "assistant", "content": response})
    if(len(st.session_state.message_queue)>=21):
        st.session_state.message_queue.popleft()
        st.session_state.message_queue.popleft()
    st.session_state.message_queue.append(HumanMessage(content=prompt))
    st.session_state.message_queue.append(AIMessage(content=response))


