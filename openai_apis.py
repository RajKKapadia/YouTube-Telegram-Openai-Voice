import os
import tempfile
import uuid

from openai import OpenAI
import soundfile as sf
import config

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

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
        transcript = client.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format="text"
        )
        return {
            'status': 1,
            'transcript': transcript
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
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print('Error at chat_completion...')
        print(e)
        return 'We are facing an issue at this moment.'


chat_completion('hi')


def text_to_speech(text: str) -> tuple[str, str]:
    file_name = f'{uuid.uuid1()}.{config.AUDIO_FILE_FORMAT}'
    audio_file_path = os.path.join(
        config.OUTPUT_DIR,
        file_name
    )
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
        response_format=config.AUDIO_FILE_FORMAT
    )
    response.write_to_file(audio_file_path)
    return audio_file_path, file_name
