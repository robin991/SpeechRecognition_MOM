import whisper
import openai
import os
import sys 
import subprocess  
from fastapi import FastAPI, File, UploadFile
import aiofiles  
'''
Whisper : https://www.assemblyai.com/blog/how-to-run-openais-whisper-speech-recognition-model/
Subprocess: https://www.datacamp.com/tutorial/python-subprocess
openai.completion : https://platform.openai.com/docs/guides/gpt/chat-completions-vs-completions

'''

openai.api_key = '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'

model = whisper.load_model("base")

def video_to_audio(video_file):
    audio_file = "input_audio.mp3"
    subprocess.call(['ffmpeg',"-y","-i", video_file, audio_file],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.STDOUT)
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

audio_file = video_to_audio('ELON MUSK on How to manage companies better 2020.mp4')
transcript = audio_to_transcript(audio_file)
final_result = MOM_generation(transcript)

print(final_result)
