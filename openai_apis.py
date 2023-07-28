import os
import tempfile

import openai
import soundfile as sf
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")

OUTPUT_DIR = os.path.join(
    tempfile.gettempdir(),
    'openai_telegram',
    'audios'
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


def transcript_audio(ogg_file_path: str, file_id: str) -> dict:
    try:
        audio_data, sample_rate = sf.read(ogg_file_path)
        mp3_file_path = f'{OUTPUT_DIR}/{file_id}.mp3'
        sf.write(mp3_file_path, audio_data, sample_rate)
        audio_file = open(mp3_file_path, 'rb')
        os.unlink(ogg_file_path)
        os.unlink(mp3_file_path)
        transcript = openai.Audio.transcribe(
            'whisper-1', audio_file)
        return {
            'status': 1,
            'transcript': transcript['text']
        }
    except Exception as e:
        print('Error at transcript_audio...')
        print(e)
        return {
            'status': 0,
            'transcript': ''
        }


def chat_completion(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': text}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print('Error at chat_completion...')
        print(e)
        return 'We are facing an issue at this moment.'
