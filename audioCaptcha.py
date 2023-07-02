import requests
import os
import speech_recognition as sr
from time import sleep
from pydub import AudioSegment
import pyperclip
import whisper


    

def speech_rec(the_audio_src_link):
    print('Speech to text conversion intialized')
    filename = "cap.mp3"
    dst = "cap.wav"
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(dst):
        os.remove(dst)

    
    
    
    audio = requests.get(f"{the_audio_src_link}")
    #print(f'the link being used is ------- || > {pyperclip.paste()} < || --------')
    #print(audio)
    with open(filename , 'wb') as f:
        f.write(audio.content)
        print(audio.content)
        print('Audio Saved Bro')
    
    #Converting the audio from .mp3 to .wav format 
    sound = AudioSegment.from_mp3(filename)
    sound.export(dst , format="wav")
    print('Conversion Complete')
    
    #initializing the recognizer
    print("Audio Recognition has begun : - >")
    
    
    '''
    r = sr.Recognizer()
    with sr.AudioFile("cap.wav") as src:
        audio_data = r.record(src)
        text = r.recognize_google(audio_data, key = None , language='en-US', show_all=True)
        print(text)
    '''
    #using open_ai whisper to transcribe the audio captcha
    model = whisper.load_model('base')
    result = model.transcribe(dst)
    text = result["text"]
    print(f'The Speech to text result is ====================== {text}')
    try:
    
        if os.path.exists(filename):
            os.remove(filename)
        if os.path.exists(dst):
            os.remove(dst)
        print('Existing audio capcha files have been removed + | - : >')
    except Exception as error:
        print(error)
    
    return text  
if __name__ == '__main__':
    speech_rec()
   
    
