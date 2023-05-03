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
from DBService.db_service import UserDataDatabaseService
from chat_state import ChatState

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
        self._chat_gpt_clients = dict()

    def _get_chat_state(self, user_id: str) -> ChatState:
        chat_state_value = self._user_data_db.get_chat_state(user_id)
        return ChatState(chat_state_value)
    
    def _set_chat_state(self, user_id: str, chat_state: ChatState):
        self._user_data_db.set_chat_state(user_id, chat_state.value[0])

    def _get_openai_api_key(self, user_id: str) -> str | None:
        api_key = self._user_data_db.get_api_key(user_id)
        return api_key.strip() if api_key else None
    
    def _parse_assistant_role(button_action_body: str) -> str:
        return button_action_body.split("__")[1].replace("_role", '').replace("_", " ")

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

    def _send_text_message(self, user_id: str, message: str):
        viber.send_messages(user_id, [TextMessage(text=message)])

    def _send_keyboard(self, user_id: str, keyboard: dict, message: str = ''):
        extended_keyboard = keyboards.append_buttons(keyboard, [keyboards.HELP_BUTTON])
        text_message = TextMessage(text=message)
        keyboard_message = KeyboardMessage(keyboard=extended_keyboard)
        messages = [text_message, keyboard_message] if len(message) > 0 else [keyboard_message]
        viber.send_messages(user_id, messages)

    def _send_initial_message(self, request: ViberConversationStartedRequest | ViberSubscribedRequest):
        user_id = request.user.id
        logger.info(f"_send_initial_message called for User {user_id}")

        reply_message = constants.WELCOME_USER_MESSAGE
        keyboard = keyboards.MAIN_KEYBOARD
        if not self._get_openai_api_key(user_id):
            reply_message += f" {constants.API_KEY_REQUEST_MESSAGE}"
            keyboard = keyboards.SET_API_KEY_KEYBOARD

        viber.send_messages(user_id, [TextMessage(text=reply_message)])
        self._send_keyboard(user_id, keyboard)

    def _handle_conversation_started_request(self, request: ViberConversationStartedRequest):
        logger.info(f"_handle_subscribed_request called for User {request.user.id}")
        self._send_initial_message(request)

    def _handle_subscribed_request(self, request: ViberSubscribedRequest):
        logger.info(f"_handle_subscribed_request called for User {request.user.id}")
        self._send_initial_message(request)

    def _handle_unsubscribed_request(self, request: ViberUnsubscribedRequest):
        logger.info(f"User {request.user_id} unsubscribed.")

    def _handle_failed_request(self, request: ViberFailedRequest):
        logger.error(f"Client failed receiving message. failure: {request}")

    def _handle_message_request(self, request: ViberMessageRequest):
        message = request.message.text
        user_id = request.sender.id
        logger.info(f'Received message "{message}" from User {user_id}.')

        if message in keyboards.BUTTON_ACTIONS:
            self._handle_keyboard_button_click(request)
        else:
            self._handle_text_message_request(request)
            

    def _handle_text_message_request(self, request: ViberMessageRequest):
        user_id = request.sender.id
        logger.info(f'_handle_text_message_request for User {user_id}.')

        message = request.message.text
        api_key = self._get_openai_api_key(user_id)
        chat_state = self._get_chat_state(user_id)
        if not chat_state: chat_state = ChatState.MAIN
        logger.info(f"User's {user_id} chat state is {chat_state}.")

        if chat_state == ChatState.MAIN:
            if api_key:
                self._send_text_message(user_id, constants.ASSISTANT_IS_ANSWERING_MESSAGE)
                answer = TextDavinciClient.ask_question(api_key, message)
                viber.send_messages(user_id, [TextMessage(text=answer)])
                bot._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)
            else:
                viber.send_messages(user_id, [TextMessage(text=constants.API_KEY_REQUEST_MESSAGE)])
                self._send_keyboard(user_id, keyboards.SET_API_KEY_KEYBOARD)

        elif chat_state == ChatState.PROVIDING_API_KEY:
            api_key = message
            self._user_data_db.store_api_key(user_id, api_key)
            viber.send_messages(user_id, [TextMessage(text=constants.API_KEY_SET_SUCCESSFULLY_MESSAGE)])
            self._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)
            self._set_chat_state(user_id, ChatState.MAIN)

        elif chat_state == ChatState.HAVING_CONVERSATION_WITH_ASSISTANT:
            chat_gpt_client = self._chat_gpt_clients[user_id]
            self._send_text_message(user_id, constants.ASSISTANT_IS_ANSWERING_MESSAGE)
            response = chat_gpt_client.ask_chat(message)
            viber.send_messages(user_id, [TextMessage(text=response)])
            self._send_keyboard(user_id, keyboards.END_CHAT_KEYBOARD)

        elif chat_state == ChatState.PROVIDING_IMAGES_DESCRIPTION:
            pass

        else:
            viber.send_messages(user_id, [TextMessage(text=constants.HELP_MESSAGE)])
            self._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)

    def _handle_keyboard_button_click(self, request: ViberMessageRequest):
        message = request.message.text
        user_id = request.sender.id
        logger.info(f'_handle_keyboard_button_click for User {request.sender.id}.')

        api_key = self._get_openai_api_key(user_id)

        if message == keyboards.get_button_action(keyboards.HELP_BUTTON):
            viber.send_messages(user_id, [TextMessage(text=constants.HELP_MESSAGE)])
            if api_key:
                self._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)
            else:
                self._send_keyboard(user_id, keyboards.SET_API_KEY_KEYBOARD)

        elif message == keyboards.get_button_action(keyboards.CANCEL_BUTTON):
            self._set_chat_state(user_id, ChatState.MAIN)
            if api_key:
                self._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)
            else:
                self._send_keyboard(user_id, keyboards.SET_API_KEY_KEYBOARD)

        elif message == keyboards.get_button_action(keyboards.SET_API_KEY_BUTTON):
            viber.send_messages(user_id, [TextMessage(text=constants.PLEASE_SEND_API_KEY_MESSAGE)])
            self._send_keyboard(user_id, keyboards.CANCEL_KEYBOARD)
            self._set_chat_state(user_id, ChatState.PROVIDING_API_KEY)

        elif api_key:
            chat_state = self._get_chat_state(user_id)

            if message == keyboards.get_button_action(keyboards.START_CHAT_BUTTON):
                viber.send_messages(user_id, [TextMessage(text=constants.ASSISTANT_ROLE_REQUEST_MESSAGE)])
                self._send_keyboard(user_id, keyboards.ASSISTANT_ROLES_KEYBOARD)
                self._set_chat_state(user_id, ChatState.SELECTING_ASSISTANT_ROLE)

            elif message in keyboards.ROLE_BUTTON_ACTIONS :
                if chat_state == ChatState.SELECTING_ASSISTANT_ROLE:
                    assistant_role = self._parse_assistant_role(message)
                    chat_gpt_client = ChatGPTClient(api_key, assistant_role)
                    self._chat_gpt_clients[user_id] = chat_gpt_client
                    viber.send_messages(user_id, [TextMessage(text=constants.CHAT_STARTED_MESSAGE)])
                    self._send_keyboard(user_id, keyboards.END_CHAT_KEYBOARD)
                    self._set_chat_state(user_id, ChatState.HAVING_CONVERSATION_WITH_ASSISTANT)
                else:
                    self._handle_text_message_request(request)

            elif message == keyboards.get_button_action(keyboards.END_CHAT_KEYBOARD):
                if chat_state == ChatState.HAVING_CONVERSATION_WITH_ASSISTANT:
                    del self._chat_gpt_clients[user_id]
                    viber.send_messages(user_id, [TextMessage(text=constants.CHAT_ENDED_MESSAGE)])
                    self._send_keyboard(user_id, keyboards.MAIN_KEYBOARD)
                    self._set_chat_state(user_id, ChatState.MAIN)
                else:
                    self._handle_text_message_request(request)

            else:
                self._send_text_message(user_id, "This feature is not supported yet.")
        else:
            viber.send_messages(user_id, [TextMessage(text=constants.SOMETHING_WENT_WRONG_MESSAGE + constants.API_KEY_REQUEST_MESSAGE)])
            self._send_keyboard(user_id, keyboards.SET_API_KEY_KEYBOARD)
            self._set_chat_state(user_id, ChatState.MAIN)


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
