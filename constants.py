# environment variables
VIBER_BOT_TOKEN_ENV = "VIBER_BOT_TOKEN"
API_KEYS_DB_ENCRYPTION_KEY_ENV = "API_KEYS_DB_ENCRYPTION_KEY"

# User and chat data field keys
API_KEY_FIELD = "api_key"
CHAT_STATE_FIELD = "chat_state"
IMAGES_DESCRIPTION_KEY = "img_description"
IMAGES_COUNT_KEY = "img_count"
CHAT_CLIENT = "chat_client"

# Predefinded messages
BOT_MENU_HELP_MESSAGE = "For more details see Help section."
WELCOME_USER_MESSAGE = "Welcome to the Smart Assistant Viber bot! Ask me something or go to menu in order to use extended list of features. " + BOT_MENU_HELP_MESSAGE
# API Key
PLEASE_SEND_API_KEY_MESSAGE = "Please send me your OpenAI API key. Use Help menu button in order to get info about how to get it."
API_KEY_REQUEST_MESSAGE = "Please provide me with your OpenAI API key via bot menu in order to use bot functionality."
API_KEY_SET_SUCCESSFULLY_MESSAGE = "API key set successfully! Now you can use bot functionality."
# Conversation with Chat GPT
ASSISTANT_ROLE_REQUEST_MESSAGE = "Please select role of your assistant from the given list or send me your option."
ASSISTANT_IS_ANSWERING_MESSAGE = "Assistant is answering on your message. Please wait..."
CHAT_STARTED_MESSAGE = "Chat with your assistant has been started. Feel free to ask something 😊"
CHAT_ENDED_MESSAGE = "Chat with your assistant has been ended. It was a pleasure to communicate with you 😊"
# Image Generation
IMAGE_DESCRIPTION_REQUEST_MESSAGE = "Please provide description of image which you want to generate."
IMAGE_COUNT_REQUEST_MESSAGE = "How much images do you want to generate?"
IMAGE_SIZE_REQUEST_MESSAGE = "Please select images size."
IMAGE_GENERATION_IN_PROGRESS_MESSAGE = "Image is generating at the moment. Please wait..."
IMAGE_SIZE_FORMAT_IS_INCORRECT_MESSAGE = "Entered image size format is incorrect."
HERE_ARE_YOUR_IMAGES_MESSAGE = "Here are your images 😊"
# Media file transcription
TRANSCRIPT_MEDIA_HELP = "If you want transcript some media file or voice message than use `Transcript Media` menu button and provide bot with voice message, audio or video file."
MEDIA_FILE_REQUEST_MESSAGE = "Please provide media file which you want to transcript. It can be voice message, audio or video file.\nSupported formats: ['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg']"
TRANSCRIPTION_IN_PROGRESS_MESSAGE = "Transcription in progress. Please wait..."
# Errors
SOMETHING_WENT_WRONG_MESSAGE = "Something went wrong."
TRY_AGAIN_MESSAGE = "An error occurred. Please try again."
# Help
HELP_MESSAGE = '''
1. In order to use bot functionality you need to provide bot with your OpenAI API Key. Read the following article if you need to know how and where to get it: [How to get OpenAI API Key?](https://www.awesomescreenshot.com/blog/knowledge/chat-gpt-api#How-do-I-get-an-API-key-for-Chat-GPT%3F")
If you already have an API key that provide bot with it using `Set API Key` menu button.
2. After setting OpenAI API Key you will unlock access to the next features:
    - Communication with AI assistant
    - Image generation by description
    - Audio transcription
3. You can communicate with your assistant in 2 ways. First way is very simple - just write some message to the bot and he will answer. But if you want bot to remember message history and have longer full-fledged conversation than use `Start Chat With Assistant` button and follow instructions.
Worth noting that you are able to communicate with your assistant with the help of voice messages. Just send it to you assistant and he will reply (Note that communication via voice messages works a little longer then via text messages).
4. Use `Generate Image` menu button in order to generate image or some images by description. Feel free to describe as much details of desired image as you want.
5. If you want transcript some media file or voice message than use `Transcript Media` menu button and provide bot with voice message, audio or video file.
'''
