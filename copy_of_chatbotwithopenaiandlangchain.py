# -*- coding: utf-8 -*-
"""Copy of ChatBotWithOpenAIAndLangChain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PAVffNbfvdeayh6vfxNlsugnx1yHskdS
"""

!pip install langchain
!pip install openai
!pip install gradio
!pip install huggingface_hub

import os
import re
import requests
import json
import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

"""**How to get Open AI API Key?**
- Go to https://platform.openai.com/account/api-keys
- Create a new Secret Key
- Copy the Secret Key for your use.
"""

OPENAI_API_KEY="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"
PLAY_HT_API_KEY="5973d6af1cac4f379b2ba4d833d6e7dd"
PLAY_HT_USER_ID="DwBmlbxZhsPjGtwsBevDXn2d5Fo1"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

play_ht_api_get_audio_url="https://play.ht/api/v2/tts"
PLAY_HT_VOICE_ID="s3://voice-cloning-zero-shot/9b2bfcf2-b2b3-4134-a5b2-a8bfb8f60e33/bhuvaneswari/manifest.json"

template = """Meet Riya, your youthful and witty personal assistant! At 21 years old, she's full of energy and always eager to help. Riya's goal is to assist you with any questions or problems you might have. Her enthusiasm shines through in every response, making interactions with her enjoyable and engaging..
{chat_history}
User: {user_message}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "user_message"], template=template
)

memory = ConversationBufferMemory(memory_key="chat_history")

"""
- Similar to Open AI Mondel we can also use HuggingFace Transformer Models.
- Reference links: https://python.langchain.com/docs/integrations/providers/huggingface , https://python.langchain.com/docs/integrations/llms/huggingface_hub.html

"""

# from langchain.llms import HuggingFacePipeline
# hf = HuggingFacePipeline.from_model_id(
#     model_id="gpt2",
#     task="text-generation",)

llm_chain = LLMChain(
    llm=ChatOpenAI(temperature='0.5', model_name="gpt-3.5-turbo"),
    prompt=prompt,
    verbose=True,
    memory=memory,
)

def get_text_response(user_message,history):
    response = llm_chain.predict(user_message = user_message)
    return response

demo = gr.ChatInterface(get_text_response, examples=["How are you doing?","What are your interests?","Which places do you like to visit?"])

if __name__ == "__main__":
    demo.launch() #To create a public link, set `share=True` in `launch()`. To enable errors and logs, set `debug=True` in `launch()`.

"""##**Publishing your code to Hugging Face**"""

from huggingface_hub import notebook_login

notebook_login()

from huggingface_hub import HfApi
api = HfApi()

HUGGING_FACE_REPO_ID = "Bhuvana27/GradiolangchainChatbot"

"""**Adding Secret Variables in Hugging Face Account:**

- Open your Space
- Click on Settings Button
- Checkout to **Variables and secrets** section
- Create New Secrets

*Note*: Make sure to add your **OPENAI_API_KEY** in Secret key
"""

# Commented out IPython magic to ensure Python compatibility.
# %mkdir /content/ChatBotWithOpenAI
!wget -P  /content/ChatBotWithOpenAI/ https://s3.ap-south-1.amazonaws.com/cdn1.ccbp.in/GenAI-Workshop/ChatBotWithOpenAIAndLangChain/app.py
!wget -P /content/ChatBotWithOpenAI/ https://s3.ap-south-1.amazonaws.com/cdn1.ccbp.in/GenAI-Workshop/ChatBotWithOpenAIAndLangChain/requirements.txt

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/ChatBotWithOpenAI

api.upload_file(
    path_or_fileobj="./requirements.txt",
    path_in_repo="requirements.txt",
    repo_id=HUGGING_FACE_REPO_ID,
    repo_type="space")

api.upload_file(
    path_or_fileobj="./app.py",
    path_in_repo="app.py",
    repo_id=HUGGING_FACE_REPO_ID,
    repo_type="space")

