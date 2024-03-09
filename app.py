import streamlit as st
from dotenv import load_dotenv
load_dotenv() #Load all the environment variables
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
st.set_page_config(page_title="YouTube Transcript Summarizer", page_icon="📹")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt=""""You are Youtube Video summarizer. You will be taking transcript text and summarizing the entire video and providing the summary in points in 250 words. Please provide the summary of the text given here: """
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)
        transcript=""
        for i in transcript_text:
           transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

with open('properties/style.css') as f:
   st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.title("Youtube Transcript To Detailed Notes Converter")
youtube_link=st.text_input("Enter Youtube video link: ")
if youtube_link:
  video_id=youtube_link.split("=")[1]
  print(video_id)
  st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True, output_format="JPEG", channels="RGB")
if st.button("Get detailed notes", key="get_notes_button"):
    transcript_text=extract_transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown(" ## Detailed Notes:")
        st.write(summary)




