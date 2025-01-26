import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_video_id(url):
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def ask_gpt(transcript, question):
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about YouTube video transcripts."},
                {"role": "user", "content": f"Transcript: {transcript}\n\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error querying ChatGPT: {e}")
        return None

st.title("YouTube Transcript Extractor and Q&A")

url = st.text_input("Enter the YouTube video URL:")

if url:
    video_id = get_video_id(url)
    
    if not video_id:
        st.error("Invalid YouTube URL. Please try again.")
    else:
        transcript = get_transcript(video_id)
        
        if transcript:
            st.subheader("Transcript:")
            st.text_area("", value=transcript, height=300)
            
            st.subheader("Ask a question about the transcript:")
            
            with st.form(key='question_form'):
                question = st.text_input("Your question:")
                submit_button = st.form_submit_button(label='Ask')
            
            if question and (submit_button or st.session_state.get('form_submitted', False)):
                st.session_state['form_submitted'] = True
                answer = ask_gpt(transcript, question)
                if answer:
                    st.subheader("Answer:")
                    st.write(answer)
            elif submit_button and not question:
                st.warning("Please enter a question.")
        else:
            st.warning("Unable to retrieve the transcript.")

st.markdown("---")
