import os
import openai
from dotenv import load_dotenv
import streamlit as st
import translators as ts
import translators.server as tss

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

input_lang = "English"
output_lang = "English"

# ==========[ FUNCTIONS ]========== #
def generate_response(user_input: str) -> str:
  input_prompt = "Convert this text " + user_input + " into a professional email in plain markdown in " + output_lang + " without subject title: "

  response =  openai.Completion.create(
  model="text-davinci-003",    
  prompt= input_prompt,
  max_tokens=1000,
  )  

  return response.choices[0].text

def generate_translation(text: str) -> str:
  response =  openai.Completion.create(
  model="text-davinci-003",    
  prompt="Translate the following into Chinese: " +  text,
  max_tokens=1000,
  )  
  return response.choices[0].text

def summarize(text: str) -> str:
  response =  openai.Completion.create(
  model="text-davinci-003",    
  prompt="Summarize the following into understandable bullet points in markdown in Chinese: " +  text,
  max_tokens=1000,
  )  
  return response.choices[0].text

# ==========[ STREAMLIT UI ]========== # 

st.set_page_config(layout="wide")
st.title("Email Secretary 📧")
with st.sidebar:
  st.markdown("## Navigation")
  page = st.radio("", ["Email Writer", "Text Translate and Summary"])

# =====[ EMAIL WRITER ]===== #
if page == "Email Writer":
  rewrite_output = ""

  st.markdown("## Email Writer")
  _, col1, col2, _= st.columns(4)
  col3, col4 = st.columns(2)

  with col1:
    input_lang = st.selectbox("Input Language", ["English", "Simplified Chinese"])
  with col2:
    output_lang = st.selectbox("Output Language:", ["English", "Simplified Chinese"])

  with col3:
    st.markdown("## Input")
    user_input = st.text_area("", height=300, key="rewrite text area")

    if st.button('Start writing ', key="rewrite button"):
      rewrite_output = generate_response(user_input)
    
  with col4:
    st.markdown("## Output")
    if rewrite_output: 
      st.markdown(rewrite_output)
      if output_lang == "English":
        st.markdown("---")
        st.code(generate_translation(rewrite_output), language="markdown")

  st.markdown("---")

# =====[ EMAIL SUMMARY ]===== #
if page == "Text Translate and Summary":
  output_summary = ""

  st.markdown("## Email Translate and Summary")
  col5, col6 = st.columns(2)

  with col5:
    st.markdown("## Text")
    user_input = st.text_area("", height=300, key="summary text area")

    if st.button('Start Summarizing ', key="summary button"):
      output_summary = generate_translation(user_input)
    
  with col6:
    st.markdown("## Summarize")
    if output_summary: 
      st.markdown(output_summary)

      st.markdown("---")
      st.markdown("#### 主要信息")
      st.markdown(summarize(output_summary))






