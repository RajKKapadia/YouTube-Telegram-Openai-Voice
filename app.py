from fastapi import APIRouter, Request

from openai_apis import transcript_audio, chat_completion
from telegram_api import send_message, set_webhook, get_file_path, save_file_and_get_local_path

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
                local_file_path = save_file_and_get_local_path(file_path['file_path'])
                if local_file_path['status'] == 1:
                    transcript = transcript_audio(local_file_path['local_file_path'], local_file_path['file_id'])
                    if transcript['status'] == 1:
                        query = chat_completion(transcript['transcript'])
        else:
            query = body['message']['text']
        response = chat_completion(query)
        send_message(sender_id, response)
        return 'OK', 200
    except Exception as e:
        print('Error at telegram...')
        print(e)
        return 'OK', 200


@router.route('/set-telegram-webhook', methods=['POST'])
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
