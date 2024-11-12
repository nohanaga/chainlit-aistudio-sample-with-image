import chainlit as cl
import requests
import json
import os
from dotenv import load_dotenv
import base64
# Load environment variables
load_dotenv()

AZURE_ENDPOINT_URL = os.environ['AZURE_ENDPOINT_URL']
AZURE_ENDPOINT_KEY = os.environ['AZURE_ENDPOINT_KEY']
AZURE_MODEL_DEPLOYMENT = "" #os.environ['AZURE_MODEL_DEPLOYMENT']

# Usage example
url = AZURE_ENDPOINT_URL
api_key = AZURE_ENDPOINT_KEY
deployment_name =AZURE_MODEL_DEPLOYMENT

if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


def allow_self_signed_https(allowed):
    if allowed:
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def call_azure_ml_endpoint(url, api_key, data, deployment_name=None):
    allow_self_signed_https(True)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    # if deployment_name:
    #     headers['azureml-model-deployment'] = deployment_name

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        # Decode the JSON response to get a Python dictionary
        decoded_response = json.loads(response.content.decode('utf-8'))
        return decoded_response

    except requests.exceptions.HTTPError as error:
        error_message = {
            'status_code': error.response.status_code,
            'headers': error.response.headers,
            'body': error.response.content
        }
        return error_message

async def handle_image(image):
    # アップロードされた画像のパスを取得
    image_path = image.path

    # 画像ファイルを読み込んで、base64 エンコード
    with open(image_path, "rb") as img_file:
        base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')

    return base64_encoded


# チャットが開始されたときに実行される関数
@cl.on_chat_start  
async def on_chat_start():
    await cl.Message(content="写真とメッセージを入力してください！").send()

@cl.on_message
async def on_message(message: cl.Message):
    base64_data = None

    # ユーザーから画像がアップロードされている場合
    images = [file for file in message.elements if "image" in file.mime]
    if images:
        # Base64 エンコードされたデータを取得
        base64_data = await handle_image(images[0])

    if base64_data:
        data ={
            "question": [message.content, "data:image/png;base64," + base64_data],
            "chat_history": []
        }
    else:
        data = {"question": [message.content], "chat_history": []}

    response = call_azure_ml_endpoint(url, api_key, data, deployment_name)

    if isinstance(response, dict) and 'answer' in response:
        await cl.Message(content=response['answer']).send()
    else:
        await cl.Message(content=response).send()
