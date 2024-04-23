import os
import requests
import streamlit as st
from pytube import YouTube
from zipfile import ZipFile
from utils import read_file
# from time import sleep


def youtube_transcription():
    st.markdown('# **YouTube Transcriber ▶️**')
    st.caption("**Easily convert YouTube videos into text with detailed transcripts for better comprehension and analysis.**")
    st.sidebar.caption("""
    ### :orange[Welcome to YouTube Transcriber!]
    Easily convert YouTube videos into text with detailed transcripts for better comprehension and analysis.""")
    
    URL = st.sidebar.text_input('Enter URL of YouTube video:')
    submit_button = st.sidebar.button('Go')
    
    st.sidebar.caption("""
    
    ### Get Started
    1. **Enter YouTube Video URL**: Simply paste the URL of the YouTube video you want to transcribe.
    2. **Generate Transcript**: Click "Go" to convert the video into a detailed text transcript.
    3. **Analyze and Comprehend**: Use the transcript for better understanding and analysis of the video's content.

    ### Privacy Notice
    - Your video URL is used solely for the purpose of generating the transcript and is not shared with anyone.
    - Generated transcripts are stored temporarily and can be downloaded for your records.

    :rainbow[Start transcribing your YouTube videos now!]
    """)

    if submit_button and URL:
        api_key = st.secrets['api_key']
        headers = {"authorization": api_key, "content-type": "application/json"}
        bar = st.progress(0)

        # Function to download YouTube audio
        def get_yt_audio(url):
            video = YouTube(url)
            yt = video.streams.get_audio_only()
            yt.download()
            bar.progress(10)
            return yt.default_filename
        
        # Function to transcribe audio
        def transcribe_yt(filename):
            bar.progress(20)
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=headers, data=read_file(filename))
            audio_url = response.json()['upload_url']
            bar.progress(30)

            json = {"audio_url": audio_url}
            transcript_response = requests.post('https://api.assemblyai.com/v2/transcript', json=json, headers=headers)
            transcript_id = transcript_response.json()["id"]
            bar.progress(50)

            endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
            status = 'processing'
            with st.spinner('Transcription is processing...'):
                while status != 'completed':
                    response = requests.get(endpoint, headers=headers)
                    status = response.json()['status']
            
            bar.progress(100)
            return response.json()["text"], endpoint
        
        # Main transcription process
        try:
            filename = get_yt_audio(URL)
            transcript_text, transcript_endpoint = transcribe_yt(filename)

            st.subheader('Transcription Output')
            st.success(transcript_text)

            # Save the transcript in text and srt formats
            with open('yt.txt', 'w') as yt_txt:
                yt_txt.write(transcript_text)

            srt_response = requests.get(transcript_endpoint + "/srt", headers=headers)
            with open("yt.srt", "w") as srt_file:
                srt_file.write(srt_response.text)

            # Create a zip file of the transcripts
            with ZipFile('transcription.zip', 'w') as zip_file:
                zip_file.write('yt.txt')
                zip_file.write('yt.srt')

            # Download button for the zip file
            with open("transcription.zip", "rb") as zip_download:
                st.download_button("Download ZIP", zip_download, "transcription.zip", "application/zip")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    youtube_transcription()
