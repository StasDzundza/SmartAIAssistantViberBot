import copy

keyboard_template = {
    "Type": "keyboard",
    "DefaultHeight": True,    # Possible values: true, false; Default: false
    "InputFieldState": "regular",    # Possible values: "hidden", "regular", "minimized"; Default: "regular"
    "BgColor": "#FFFFFF",    # Default: "#FFFFFF"
    "Buttons": [
        {
            "Columns": 6,    # Integer value between 1 and 6; Default: 6
            "Rows": 1,    # Integer value between 1 and 2; Default: 1
            "BgColor": "#2db9b9",    # Default: "#FFFFFF"
            "BgMediaType": "picture",    # Possible values: "picture", "gif"; Default: "picture"
            "BgMedia": "http:#path.to/your/image",    # URL of the image or GIF
            "BgMediaScaleType": "fit",    # Possible values: "fit", "crop", "fill"; Default: "fit"
            "BgLoop": "true",    # Possible values: "true", "false"; Default: "false"
            "Image": "http:#path.to/your/button/image",    # URL of the image for the button
            "Text": "Button Text",    # Button text
            "TextVAlign": "middle",    # Possible values: "middle", "top", "bottom"; Default: "middle"
            "TextHAlign": "center",    # Possible values: "center", "left", "right"; Default: "center"
            "TextPaddings": [12, 12, 12, 12],    # List of 4 integer values for top, right, bottom, left padding; Default: [0, 0, 0, 0]
            "TextOpacity": 100,    # Integer value between 0 and 100; Default: 100
            "TextSize": "regular",    # Possible values: "small", "regular", "large"; Default: "regular"
            "TextStyle": "bold",    # Possible values: "bold", "italic", "underline", "strike"; Default: "bold"
            "TextBgGradientColor": "#CCCCCC",    # Default: ""
            "ActionType": "reply",    # Possible values: "reply", "open-url", "location-picker", "share-phone", "none"; Default: "reply"
            "ActionBody": "Action Text",    # Action-specific data
            "ImageScaleType": "fit",    # Possible values: "fit", "crop", "fill"; Default: "fit"
            "Silent": "true",    # Possible values: "true", "false"; Default: "false"
            "FavIconUrl": "http:#path.to/your/favicon",    # URL of the favicon
            "MapThumbnailUrl": "http:#path.to/your/map/thumbnail",    # URL of the map thumbnail
            "MapScaleType": "fit",    # Possible values: "fit", "crop", "fill"; Default: "fit"
            "MapZoomLevel": 50    # Integer value between 0 and 100; Default: 50
        }
    ]
}

BUTTONS_KEY = "Buttons"
ROLE_BUTTON_ACTIONS = ["__chatbot_role__", "__cook_role__", "__doctor_role__", "__professional_sportsmen_role__", "__scientist_role__", "__funny_guy_role__"]
IMAGE_COUNT_BUTTON_ACTIONS = ["__1__", "__2__", "__3__", "__4__"]
IMAGE_COUNT_BUTTON_ACTIONS = ["__small__", "__medium__", "__large__"]
BUTTON_ACTIONS = ["__help__", "__cancel__", "__set_api_key__", "__start_chat__", "__end_chat__", "__generate_image__"] + \
    ROLE_BUTTON_ACTIONS + IMAGE_COUNT_BUTTON_ACTIONS + IMAGE_COUNT_BUTTON_ACTIONS

def append_buttons(keyboard: dict, buttons: list[dict]) -> dict:
    extended_keyboard = copy.deepcopy(keyboard)
    extended_keyboard[BUTTONS_KEY].extend(buttons)
    return extended_keyboard

EMPTY_KEYBOARD = {
    "Type": "keyboard",
    BUTTONS_KEY: []
}

HELP_BUTTON = { "ActionType": "reply", "ActionBody": "__help__", "Text": "Help ℹ️" }
SET_API_KEY_BUTTON = { "ActionType": "reply", "ActionBody": "__set_api_key__", "Text": "Set API Key 🔑" }
CANCEL_BUTTON = { "ActionType": "reply", "ActionBody": "__cancel__", "Text": "Cancel ❌" }

HELP_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
HELP_KEYBOARD[BUTTONS_KEY].append(HELP_BUTTON)

SET_API_KEY_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
SET_API_KEY_KEYBOARD[BUTTONS_KEY].append(SET_API_KEY_KEYBOARD)

CANCEL_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
CANCEL_KEYBOARD[BUTTONS_KEY].append(CANCEL_BUTTON)

MAIN_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
MAIN_KEYBOARD[BUTTONS_KEY].extend([
    { "ActionType": "reply", "ActionBody": "__start_chat__", "Text": "Start Chat With Assistant 💬" },
    { "ActionType": "reply", "ActionBody": "__generate_image__", "Text": "Generate Image 🖼️" },
    SET_API_KEY_BUTTON
])

END_CHAT_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
END_CHAT_KEYBOARD[BUTTONS_KEY].append({"ActionType": "reply", "ActionBody": "__end_chat__", "Text": "End Chat ❌" })

ASSISTANT_ROLES_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
ASSISTANT_ROLES_KEYBOARD[BUTTONS_KEY].extend([
    { "ActionType": "reply", "ActionBody": "__chatbot_role__", "Text": "Chatbot 🤖" },
    { "ActionType": "reply", "ActionBody": "__cook_role__", "Text": "Cook 👨‍🍳" },
    { "ActionType": "reply", "ActionBody": "__doctor_role__", "Text": "Doctor 👨‍⚕️" },
    { "ActionType": "reply", "ActionBody": "__professional_sportsmen_role__", "Text": "Professional sportsmen 🏆" },
    { "ActionType": "reply", "ActionBody": "__scientist_role__", "Text": "Scientist 👨‍🔬" },
    { "ActionType": "reply", "ActionBody": "__funny_guy_role__", "Text": "Funny guy 😂" },
])

IMAGE_COUNT_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
IMAGE_COUNT_KEYBOARD[BUTTONS_KEY].extend([
    { "ActionType": "reply", "ActionBody": "__1__", "Text": "1️⃣" },
    { "ActionType": "reply", "ActionBody": "__2__", "Text": "2️⃣" },
    { "ActionType": "reply", "ActionBody": "__3__", "Text": "3️⃣" },
    { "ActionType": "reply", "ActionBody": "__4__", "Text": "4️⃣" }
])

IMAGE_SIZE_KEYBOARD = copy.deepcopy(EMPTY_KEYBOARD)
IMAGE_SIZE_KEYBOARD[BUTTONS_KEY].extend([
    { "ActionType": "reply", "ActionBody": "__small__", "Text": "Small" },
    { "ActionType": "reply", "ActionBody": "__medium__", "Text": "Medium" },
    { "ActionType": "reply", "ActionBody": "__large__", "Text": "Large" }
])

keyboard = {
    "Type": "keyboard",
    "InputFieldState": "regular",
    "Buttons": [
        {
            "Columns": 3,
            "Rows": 1,
            "BgColor": "#2db9b9",
            "Text": "One",
            "TextHAlign": "center",
            "TextVAlign": "middle",
            "ActionType": "reply",
            "ActionBody": "One",
            "Silent": "true"
        },
        {
            "Columns": 3,
            "Rows": 1,
            "BgColor": "#2db9b5",
            "Text": "Two",
            "TextHAlign": "center",
            "TextVAlign": "middle",
            "ActionType": "reply",
            "ActionBody": "Two",
            "Silent": "true"
        }
    ]
}
