import os
from PIL import Image

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory



apikey = st.secrets["OPENAI_API_KEY"]
# App UI framework
favicon=Image.open("assets/favicon.ico")
st.set_page_config(
    page_title="QuickTweetAI-AI Tweet Generator",
    page_icon=favicon,
    layout="wide",
)
st.title('QuickTweetAI- Your AI Tweet Generator')
st.subheader('🌟 Welcome to QuickTweetAI: Your Personal AI Tweet Generator! 🌟\nCrafting the perfect tweet just got easier! Introducing TweetCraftAI, your go-to destination for effortless and engaging tweets.\nSimply input your keywords, and watch as our advanced AI transforms them into attention-grabbing, share-worthy tweets tailored to your style.')

keywords = st.text_input('Enter keywords (comma-separated): ')
prompt_template = f'generate a tweet on these keywords: {keywords}' if keywords else ''

# Prompt templates
title_template = PromptTemplate(
    input_variables=['keywords'],
    template=prompt_template
)

tweet_template = PromptTemplate(
    input_variables=['keywords'],
    template='generate a tweet on these keywords: {keywords}'
)

# Memory
title_memory = ConversationBufferMemory(input_key='keywords', memory_key='chat_history')
tweet_memory = ConversationBufferMemory(input_key='keywords', memory_key='chat_history')
# Llms
llm = OpenAI(model_name="text-davinci-003", temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
tweet_chain = LLMChain(llm=llm, prompt=tweet_template, verbose=True, output_key='script', memory=tweet_memory)

# Chaining the components and displaying outputs
# Chaining the components and displaying outputs
if keywords:
    # Generate tweet
    with st.spinner("Generating tweet..."):
        tweet = tweet_chain.run({'keywords': keywords})

    # Display generated tweet
    st.subheader('Generated Tweet:')
    st.info(tweet)

    
    with st.expander('Tweet History'):
     history = tweet_memory.buffer
     st.info(history)
    if not history:
        st.info("No tweet history yet.")
        
    
footer_html = """
    <div style=" padding: 10px; position:fixed; bottom: 0; width: 100%; text-align: center justify-content:center;">
        <p>Built with ❤️ by Aquib Hussain---- <a href="https://twitter.com/AquibG1?t=UQlKWtQKEqYneDmph_FHcQ&s=09">𝕏</a></p>
      
    </div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
