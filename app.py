from fastapi import APIRouter, Request

from openai_apis import text_to_speech, transcript_audio, chat_completion
from telegram_api import send_audio, send_message, set_webhook, get_file_path, save_file_and_get_local_path
from utils import upload_file_to_gcs
import config

router = APIRouter(
    prefix='',
    responses={404: {'description': 'Not found'}}
)


@router.get('/')
def home():
    return 'OK', 200


@router.post('/telegram')
async def telegram(request: Request):
    try:
        body = await request.json()
        print(body)
        sender_id = body['message']['from']['id']
        if 'voice' in body['message'].keys():
            file_id = body['message']['voice']['file_id']
            file_path = get_file_path(file_id)
            if file_path['status'] == 1:
                local_file_path = save_file_and_get_local_path(
                    file_path['file_path'])
                if local_file_path['status'] == 1:
                    transcript = transcript_audio(
                        local_file_path['local_file_path'], local_file_path['file_id'])
                    if transcript['status'] == 1:
                        query = chat_completion(transcript['transcript'])
        else:
            query = body['message']['text']
        response = chat_completion(query)
        """Convert this response to audio using the following function
        audio_file_path = text_to_speech(response)
        Then upload this audio_file to a cloud storage and get the public URL
        audio_url = upload_file(audio_file_path)
        you need to write the function upload_file
        send_audio(audio_url)
        """
        if config.REPLY_TYPE == 'audio':
            audio_file_path, audio_file_name = text_to_speech(response)
            public_url = upload_file_to_gcs(audio_file_path, audio_file_name)
            send_audio(sender_id, public_url, 'Response')
        else:
            send_message(sender_id, response)
        return 'OK', 200
    except Exception as e:
        print('Error at telegram...')
        print(e)
        return 'OK', 200


@router.post('/set-telegram-webhook')
async def set_telegram_webhook(request: Request):
    try:
        body = await request.json()
        flag = set_webhook(body['url'], body['secret_token'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    except Exception as e:
        print('Error at set_telegram_webhook...')
        print(e)
        return 'BAD REQUEST', 400
