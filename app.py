import os
import openai
from dotenv import load_dotenv
import streamlit as st
import translators as ts
import translators.server as tss

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(user_input):
  response =  openai.Completion.create(
  model="text-davinci-003",    
  prompt="Convert the following into a professional email in plain markdown: " + user_input,
  max_tokens=1000,
  )  
  return response.choices[0].text

def generate_translation(user_input, lang):
  response =  openai.Completion.create(
  model="text-davinci-003",    
  prompt="Translate the following into " + lang +  user_input,
  max_tokens=1000,
  )  
  return response.choices[0].text

input_translate = ""


def get_translate(lang):
  input_translate=st.text_area('Text to translate:', '''''', key="translate text area")
  if input_translate:
    return generate_translation(input_translate, lang)

st.header("Translator")
choice = st.selectbox("Translation format:", ["Simplified Chinese -> English", "English -> Simplified Chinese"])

input_translate = get_translate(choice)

if st.button('Start translating', key="translate button"):
  if input_translate:
      st.markdown(input_translate)

def get_rewrite():
  input_rewrite = st.text_area("Email to rewrite: ", 
  input_translate,  key="rewrite text area")
  return input_rewrite


with st.sidebar:
  st.header("Email Writer")
  input_rewrite = get_rewrite()

  if st.button('Start writing ', key="rewrite button"):
    if input_rewrite:
        output = generate_response(input_rewrite)
        st.markdown(output)
        st.markdown("""---""")   
        st.markdown( tss.google(output, "en", "zh"))