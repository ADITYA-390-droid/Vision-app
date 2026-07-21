import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS

st.title("🤖 माझा बहुभाषिक AI Vision App")

# Streamlit Secrets मधून लपवलेली API Key घेणे
api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')


# फोटो आणि भाषा निवडणे
uploaded_file = st.file_uploader("📸 फोटो निवडा", type=["jpg", "jpeg", "png"])
lang = st.selectbox("🗣️ तुमची भाषा निवडा:", ["मराठी", "हिंदी", "English"])

if uploaded_file and st.button("Submit"):
    with st.spinner('माहिती शोधत आहे...'):
        img = Image.open(uploaded_file)
        
        # भाषेचा कोड ठरवणे
        if lang == "English":
            lang_code = 'en'
        elif lang == "हिंदी":
            lang_code = 'hi'
        else:
            lang_code = 'mr'
        
        # जेमिनीकडून माहिती काढणे
        prompt = f"Identify the main object in this image and give a short 2-sentence summary in {lang}."
        response = model.generate_content([prompt, img])
        
        st.success("माहिती मिळाली!")
        st.write(response.text)
        
        # ऑडिओ बनवणे
        tts = gTTS(text=response.text, lang=lang_code)
        tts.save("audio.mp3")
        st.audio("audio.mp3")
