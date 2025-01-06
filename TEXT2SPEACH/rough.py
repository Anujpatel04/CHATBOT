import streamlit as st
from mtranslate import translate
import pandas as pd
import os
from gtts import gTTS
import base64

# Function to decode audio file for download
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Custom CSS for background image
background_image_css = """
<style>
body {
    background-image: url('https://pikbest.com//backgrounds/blue-wavy-wave-lines-with-lights-on-a-dark-background-ai-generated_9208777.html');
    background-size: cover;
}
.sidebar .sidebar-content {
    background: rgba(255, 255, 255, 0.8);
}
</style>
"""
st.markdown(background_image_css, unsafe_allow_html=True)

# Title and description
st.title("🌍 Language Translator")
st.write("Translate text into various languages and download the audio of the translated text.")

# Sidebar for language selection
st.sidebar.header("Options")
st.sidebar.write("Select a language and manage your settings.")

# File uploader for language data
uploaded_file = st.sidebar.file_uploader("Upload Language CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    # Default CSV path
    df = pd.read_csv(r'D:\VS_CODE_PROJECTS-NARESH-IT\PROJECTS\TEXT2SPEACH\language.csv')

df.dropna(inplace=True)
lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()

# Create dictionary of language and 2-letter langcode
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

speech_langs = {
    "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
    "bs": "Bosnian", "ca": "Catalan", "cs": "Czech", "cy": "Welsh",
    "da": "Danish", "de": "German", "el": "Greek", "en": "English",
    "eo": "Esperanto", "es": "Spanish", "et": "Estonian", "fi": "Finnish",
    "fr": "French", "gu": "Gujarati", "od": "odia", "hi": "Hindi",
    "hr": "Croatian", "hu": "Hungarian", "hy": "Armenian", "id": "Indonesian",
    "is": "Icelandic", "it": "Italian", "ja": "Japanese", "jw": "Javanese",
    "km": "Khmer", "kn": "Kannada", "ko": "Korean", "la": "Latin",
    "lv": "Latvian", "mk": "Macedonian", "ml": "Malayalam", "mr": "Marathi",
    "my": "Myanmar (Burmese)", "ne": "Nepali", "nl": "Dutch", "no": "Norwegian",
    "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian",
    "si": "Sinhala", "sk": "Slovak", "sq": "Albanian", "sr": "Serbian",
    "su": "Sundanese", "sv": "Swedish", "sw": "Swahili", "ta": "Tamil",
    "te": "Telugu", "th": "Thai", "tl": "Filipino", "tr": "Turkish",
    "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese", "zh-CN": "Chinese"
}

# Text input
st.subheader("Input Text")
inputtext = st.text_area("Enter text to translate", height=100)

# Language selection
choice = st.sidebar.selectbox("Select Target Language", langlist)

# Translation and output
if st.button("Translate"):
    if len(inputtext) > 0:
        try:
            output = translate(inputtext, lang_array[choice])
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("Translated Text")
                st.text_area("", output, height=200)

            # Check if speech is supported
            if lang_array[choice] in speech_langs:
                aud_file = gTTS(text=output, lang=lang_array[choice], slow=False)
                aud_file.save("lang.mp3")

                with col2:
                    st.subheader("Audio")
                    audio_file_read = open('lang.mp3', 'rb')
                    audio_bytes = audio_file_read.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.markdown(get_binary_file_downloader_html("lang.mp3", 'Audio File'), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter text before submitting.")