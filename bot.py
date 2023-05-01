import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("viber_bot.log"),
    ]
)
logger = logging.getLogger(__name__)

import os
import constants
import keyboards

from OpenAIClients.ChatGPT.chat_gpt_client import ChatGPTClient, TextDavinciClient
from OpenAIClients.DALLE.dalle_client import DALLEClient, ImageRequestData, ImageSize
from OpenAIClients.WhisperClient.whisper_client import WhisperClient
from OpenAIClients.DBService.db_service import ApiKeysDatabaseService

from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest, ViberFailedRequest, ViberMessageRequest, ViberSubscribedRequest, ViberUnsubscribedRequest


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Your Smart Assistant',
    avatar='',
    auth_token=os.getenv(constants.VIBER_BOT_TOKEN_ENV)
))

class ViberBot:
    def __init__(self):
        db_encryption_key = os.getenv(constants.API_KEYS_DB_ENCRYPTION_KEY_ENV)
        if not db_encryption_key:
            logger.error("API_KEYS_DB_ENCRYPTION_KEY_ENV was not found in environment variables")
        self._db_service = ApiKeysDatabaseService(db_encryption_key, "api_keys.db")


@app.route('/', methods=['POST'])
def incoming():
    logger.info("Received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Hello there!")
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="thanks for subscribing!")
        ])

        keyboard_message = KeyboardMessage(
            tracking_data='your_custom_tracking_data',
            keyboard=keyboards.keyboard2
        )
        viber.send_messages(viber_request.user.id, [keyboard_message])
    elif isinstance(viber_request, ViberUnsubscribedRequest):
        logger.info(f"User {viber_request.user_id} unsubscribed.")
    elif isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message.text
        logger.info(f'Received message "{message}" from User {viber_request.sender.id}.')
        print(f'Received message "{message}" from User {viber_request.sender.id}.')

        if message == 'One':
            response_text = 'Hello 1'
        elif message == 'Two':
            response_text = 'Hello 2'
        else:
            response_text = message
        viber.send_messages(to=viber_request.sender.id, messages=[TextMessage(text=response_text)])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.error(f"Client failed receiving message. failure: {viber_request}")

    return Response(status=200)

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    #app.run(host='0.0.0.0', port=8080, debug=True, ssl_context=context)
    app.run(port='8087')