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
from DBService.db_service import UserDataDatabaseService

from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest, ViberFailedRequest, ViberMessageRequest, ViberSubscribedRequest, ViberUnsubscribedRequest


class ViberBot:
    def __init__(self):
        db_encryption_key = os.getenv(constants.API_KEYS_DB_ENCRYPTION_KEY_ENV)
        if not db_encryption_key:
            logger.error("API_KEYS_DB_ENCRYPTION_KEY_ENV was not found in environment variables")
        self._user_data_db = UserDataDatabaseService(db_encryption_key, "user_data.db")
        self._init_handlers()

    def _init_handlers(self):
        pass

    def _get_openai_api_key(self, user_id: str) -> str | None:
        api_key = self._user_data_db.get_api_key(user_id)
        return api_key.strip() if api_key else None

    def handle_request(self, request_data: bytes):
        viber_request = viber.parse_request(request_data)

        if isinstance(viber_request, ViberConversationStartedRequest):
            self._handle_conversation_started_request(viber_request)
        elif isinstance(viber_request, ViberSubscribedRequest):
            self._handle_subscribed_request(viber_request)
        elif isinstance(viber_request, ViberUnsubscribedRequest):
            self._handle_unsubscribed_request(viber_request)
        elif isinstance(viber_request, ViberMessageRequest):
            self._handle_message_request(viber_request)
        elif isinstance(viber_request, ViberFailedRequest):
            self._handle_failed_request(viber_request)

    def _send_keyboard(self, user_id: str, keyboard: dict):
        extended_keyboard = keyboards.append_buttons(keyboard, [keyboards.HELP_BUTTON])
        keyboard_message = KeyboardMessage(keyboard=extended_keyboard)
        viber.send_messages(user_id, [keyboard_message])

    def _handle_conversation_started_request(self, request: ViberConversationStartedRequest):
        user_id = request.user.id
        logger.info(f"_handle_subscribed_request called for User {user_id}")

        viber.send_messages(user_id, [TextMessage(text=constants.WELCOME_USER_MESSAGE)])

    def _handle_subscribed_request(self, request: ViberSubscribedRequest):
        user_id = request.user.id
        logger.info(f"_handle_subscribed_request called for User {user_id}")

        reply_message = constants.WELCOME_USER_MESSAGE
        keyboard = keyboards.MAIN_KEYBOARD
        if not self._get_openai_api_key(user_id):
            reply_message += f" {constants.API_KEY_REQUEST_MESSAGE}"
            keyboard = keyboards.SET_API_KEY_KEYBOARD

        viber.send_messages(user_id, [TextMessage(text=reply_message)])
        self._send_keyboard(user_id, keyboard)

    def _handle_unsubscribed_request(self, request: ViberUnsubscribedRequest):
        logger.info(f"User {request.user_id} unsubscribed.")

    def _handle_failed_request(self, request: ViberFailedRequest):
        logger.error(f"Client failed receiving message. failure: {request}")

    def _handle_message_request(self, request: ViberMessageRequest):
        message = request.message.text
        logger.info(f'Received message "{message}" from User {request.sender.id}.')
        print(f'Received message "{message}" from User {request.sender.id}.')

        if message == 'One':
            response_text = 'Hello 1'
        elif message == 'Two':
            response_text = 'Hello 2'
        else:
            response_text = message
        viber.send_messages(to=request.sender.id, messages=[TextMessage(text=response_text)])
        self._send_keyboard(request.sender.id, keyboards.MAIN_KEYBOARD)


app = Flask(__name__)
viber = Api(BotConfiguration(
    name='Your Smart Assistant',
    avatar='',
    auth_token=os.getenv(constants.VIBER_BOT_TOKEN_ENV)
))
bot = ViberBot()

@app.route('/', methods=['POST'])
def incoming():
    logger.info("Received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, verify the signature
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    bot.handle_request(request.get_data())

    return Response(status=200)

if __name__ == "__main__":
    app.run(port='8087')
