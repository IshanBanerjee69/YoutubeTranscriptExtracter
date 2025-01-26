import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

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

st.title("YouTube Transcript Extractor")

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
        else:
            st.warning("Unable to retrieve the transcript.")

st.markdown("---")

