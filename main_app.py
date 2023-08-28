import streamlit as st 
import whisper
import openai

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from dotenv import load_dotenv
import os



model = whisper.load_model("base")
def congfigure ():
    # function to configure API key
    load_dotenv()

def video_to_audio(video_file):
    audio_file = "input_audio.mp3"
    # subprocess.call(['ffmpeg',"-y","-i", video_file, audio_file],
    #                 stdout = subprocess.DEVNULL,
    #                 stderr = subprocess.STDOUT)
    ffmpeg_extract_audio(video_file, audio_file)
    #video = moviepy.editor.VideoFileClip(video_file)
    #audio = video.audio
    return audio_file

def audio_to_transcript(audio_file):
    result = model.transcribe(audio_file)
    transcript = result["text"]
    return transcript  

def MOM_generation(prompt):

    # using freeform completiona API
    reponse  = openai.Completion.create( model="text-davinci-003",
                            prompt= "Act like an employee of a company whose is attending a meeting and generate the Minute of Meeting in form of bullet points for the below transcript?\n"+prompt,
                            temperature = 0.8,
                            max_tokens = 256)
    
    return  reponse['choices'][0]['text']

# configure api key
congfigure()
openai.api_key = st.secrets['api_key']

# main title of the application
st.title('MOM Solution')

# upload video
video_file = st.file_uploader("Video",type = ['mp4'])
#tfile = tempfile.NamedTemporaryFile(delete=False)
#tfile.write(video_file.read())

st.write("[Sample video download link]()")

if video_file:
    st.video(video_file)
      
    audio_file = video_to_audio(video_file.name)
    transcript = audio_to_transcript(audio_file)
    final_result = MOM_generation(transcript)
    st.write("This is the output transcript")
    st.write(final_result)
else:
    st.warning("Upload Video File")
