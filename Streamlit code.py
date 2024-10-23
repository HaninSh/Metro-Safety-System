#stream lit code for local front_end
import streamlit as st
import requests

# FastAPI backend URL
backend_url = "http://20.83.24.19/process-video/"

def process_video(video_link):
    try:
        # Send the video link to the backend for processing
        response = requests.post(backend_url, data={"drive_link": video_link})  # Changed to data= for form data
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error: Backend returned status code {response.status_code}")
            st.error(response.json())  # Show error details
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit UI
st.title("Video Processing App")

# Input for the video link
video_link = st.text_input("Enter the video link:")

if st.button("Process Video"):
    if video_link:
        with st.spinner('Processing the video...'):
            processed_video_bytes = process_video(video_link)
            if processed_video_bytes:
                st.success("Video processed successfully!")
                st.video(processed_video_bytes)
            else:
                st.error("Failed to process the video.")
    else:
        st.warning("Please provide a video link.")
