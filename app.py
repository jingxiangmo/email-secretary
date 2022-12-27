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

def get_translate(lang):
  input_translate=st.text_area('Text to translate:', '''''', height=210, key="translate text area")
  if input_translate:
    return generate_translation(input_translate, lang)

def get_rewrite(input_translate):
  if not input_translate:
    input_translate = ""
  return st.text_area("Email to rewrite: ", input_translate, height=300, key="rewrite text area")


# ==========[ STREAMLIT ]========== # 
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
  st.header("Translator")
  input_translate = get_translate(st.selectbox("Translation format:", ["Simplified Chinese -> English", "English -> Simplified Chinese"]))

  if st.button('Start translating', key="translate button") and input_translate:
    st.markdown(input_translate)

with col2:
    st.header("Email Writer")
    input_rewrite = get_rewrite(input_translate)
    if st.button('Start writing ', key="rewrite button") and input_rewrite:
      output = generate_response(input_rewrite)
      st.markdown(output)
      st.markdown("""---""")   
      st.markdown( tss.google(output, "en", "zh"))