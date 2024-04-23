import streamlit as st
import pandas as pd
import requests
import time
import json

# Constants
AUTH_TOKEN = "3e10e0448d754962ac0491334562f21f"
HEADERS = {
    "authorization": AUTH_TOKEN,
    "content-type": "application/json"
}
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
UPLOAD_ENDPOINT = 'https://api.assemblyai.com/v2/upload'

def mom():
    def upload_audio_to_assemblyai(audio_file):
        """Upload audio file to AssemblyAI and get the upload URL."""
        try:
            response = requests.post(UPLOAD_ENDPOINT, headers=HEADERS, data=audio_file)
            response.raise_for_status()
            audio_url = response.json()['upload_url']
            return audio_url
        except requests.exceptions.RequestException as e:
            st.error(f"Error uploading audio: {e}")
            return None

    def request_transcription(audio_url):
        """Request transcription from AssemblyAI."""
        json_payload = {
            "audio_url": audio_url,
            "iab_categories": True,
            "auto_chapters": True,
            "speaker_labels": True  # Enable speaker labels for detailed summary
        }
        try:
            response = requests.post(TRANSCRIPT_ENDPOINT, json=json_payload, headers=HEADERS)
            response.raise_for_status()
            transcript_id = response.json()['id']
            return transcript_id
        except requests.exceptions.RequestException as e:
            st.error(f"Error requesting transcription: {e}")
            return None

    def poll_transcription_status(transcript_id):
        """Poll the transcription status until it's completed."""
        polling_endpoint = f"{TRANSCRIPT_ENDPOINT}/{transcript_id}"
        while True:
            try:
                response = requests.get(polling_endpoint, headers=HEADERS)
                response.raise_for_status()
                status = response.json()['status']
                if status == 'completed':
                    return response.json()
                elif status == 'failed':
                    st.error("Transcription failed.")
                    return None
                time.sleep(5)
            except requests.exceptions.RequestException as e:
                st.error(f"Error polling transcription status: {e}")
                return None

    def convert_millis_to_time_format(millis):
        """Convert milliseconds to HH:MM:SS or MM:SS format."""
        seconds = int((millis / 1000) % 60)
        minutes = int((millis / (1000 * 60)) % 60)
        hours = int((millis / (1000 * 60 * 60)) % 24)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}' if hours > 0 else f'{minutes:02d}:{seconds:02d}'

    def display_transcription_results(results):
        """Display the transcription results including themes, chapter summaries, and detailed transcript."""
        st.subheader('Main Themes')
        with st.expander('Themes'):
            categories = results.get('iab_categories_result', {}).get('summary', [])
            for category in categories:
                st.markdown(f"* {category}")

        st.subheader('Summary Notes')
        chapters = results.get('chapters', [])
        chapters_df = pd.DataFrame(chapters)
        chapters_df['start_str'] = chapters_df['start'].apply(convert_millis_to_time_format)
        chapters_df['end_str'] = chapters_df['end'].apply(convert_millis_to_time_format)

        for _, row in chapters_df.iterrows():
            with st.expander(row['gist']):
                st.write(row['summary'])
                st.button(row['start_str'], on_click=lambda start=row['start']: update_start(start))

        st.subheader('Detailed Transcript')
        with st.expander('Transcript'):
            transcript = results.get('text', '')
            st.text_area('Transcript', value=transcript, height=300)
            st.download_button(
                label="Download Transcript",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )

    def update_start(start):
        """Update the start point for audio playback."""
        st.session_state['start_point'] = int(start / 1000)

    # Streamlit App Layout
    st.markdown('# **Automated Minutes of Meetings (MoM) Generator 📝**')
    st.caption("**Transform your meeting recordings into detailed, categorized summaries and downloadable transcripts effortlessly.**")

    # Initialize session state
    if 'start_point' not in st.session_state:
        st.session_state['start_point'] = 0

    # Sidebar for file upload
    
    st.sidebar.caption("""### :orange[Welcome to MoM Generator!]""")
    st.sidebar.caption("Transform your meeting recordings into detailed, categorized summaries and downloadable transcripts effortlessly.")
                       
    st.sidebar.subheader('Input for Summarization below')
    uploaded_file = st.sidebar.file_uploader('Upload a file for summarization')

    st.sidebar.caption("""
    ### How to Use
    1. **Upload Your Audio File**: Simply upload your meeting audio recording.
    2. **Generate Summaries**: The app will process the audio to create detailed minutes and summaries.
    3. **Download Transcripts**: Get a downloadable transcript of your meeting for easy reference.

    ### Features
    - **Detailed Summaries**: Get comprehensive and categorized summaries of your meetings.
    - **Effortless Transcription**: Transform audio recordings into written transcripts quickly.
    - **Easy Downloads**: Download the meeting minutes and transcripts for future use.

    :rainbow[Streamline your meeting documentation with ease!]
    """)


    if uploaded_file is not None:
        st.audio(uploaded_file, start_time=st.session_state['start_point'])

        with st.spinner('Uploading audio...'):
            audio_url = upload_audio_to_assemblyai(uploaded_file)

        if audio_url:
            with st.spinner('Requesting transcription...'):
                transcript_id = request_transcription(audio_url)

            if transcript_id:
                with st.spinner('Transcribing...'):
                    transcription_results = poll_transcription_status(transcript_id)

                if transcription_results:
                    display_transcription_results(transcription_results)
if __name__ == '__main__':
    mom()