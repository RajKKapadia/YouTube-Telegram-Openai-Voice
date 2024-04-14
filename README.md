# Telegram + Openai Chatbot to answer audio messages...

#### YouTube
I have recorded a quick video tutorial on this repository, you can watch it [here](https://youtu.be/v2Wjje8BT-Q).

#### Steps
* create a .env file in the root directory
* create GCP account, and get the service account credentials, then create a Cloud Storage Buckate, and **make it public**.
* in the .env file replace the CREDENTIALS with your service account file value
* replace the GCP_CLOUD_STORAGE_BUCKET_NAME with your bucket name

#### Run the code
* for server
`uvicorn run:app --host 0.0.0.0 --port 5000`
* for local
`uvicorn run:app --reload`

#### Set the Telegram webhook
* either deploy the application on the server or use NGROK
* replace YOUR_BASE_URL with your public URL not the localhost
* send a POST request to `YOUR_BASE_URL/set-telegram-webhook`
```json
{
"secret_token": "any random string",
"url": "YOUR_BASE_URL/telegram"
}
```