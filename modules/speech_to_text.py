from openai import OpenAI
import numpy as np

def speech_to_text(audio_path):
    try:
        client = OpenAI()
        
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
        return transcription.text
    
    except Exception as e:
        raise Exception(f"Error in speech to text conversion: {str(e)}")