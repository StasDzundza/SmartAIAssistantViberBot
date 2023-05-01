keyboard = {
    "Type": "keyboard",
    "Buttons": [
        {   
            "ActionType": "reply",
            "ActionBody": "One",
            "Text": "One"
        },
        {
            "ActionType": "reply",
            "ActionBody": "Two",
            "Text": "Two"
        }
    ]
}

keyboard2 = {
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

keyboard_template = """
{
    "Type": "keyboard",
    "DefaultHeight": true,    // Possible values: true, false; Default: false
    "InputFieldState": "regular",    // Possible values: "hidden", "regular", "minimized"; Default: "regular"
    "BgColor": "#FFFFFF",    // Default: "#FFFFFF"
    "Buttons": [
        {
            "Columns": 6,    // Integer value between 1 and 6; Default: 6
            "Rows": 1,    // Integer value between 1 and 2; Default: 1
            "BgColor": "#2db9b9",    // Default: "#FFFFFF"
            "BgMediaType": "picture",    // Possible values: "picture", "gif"; Default: "picture"
            "BgMedia": "http://path.to/your/image",    // URL of the image or GIF
            "BgMediaScaleType": "fit",    // Possible values: "fit", "crop", "fill"; Default: "fit"
            "BgLoop": "true",    // Possible values: "true", "false"; Default: "false"
            "Image": "http://path.to/your/button/image",    // URL of the image for the button
            "Text": "Button Text",    // Button text
            "TextVAlign": "middle",    // Possible values: "middle", "top", "bottom"; Default: "middle"
            "TextHAlign": "center",    // Possible values: "center", "left", "right"; Default: "center"
            "TextPaddings": [12, 12, 12, 12],    // List of 4 integer values for top, right, bottom, left padding; Default: [0, 0, 0, 0]
            "TextOpacity": 100,    // Integer value between 0 and 100; Default: 100
            "TextSize": "regular",    // Possible values: "small", "regular", "large"; Default: "regular"
            "TextStyle": "bold",    // Possible values: "bold", "italic", "underline", "strike"; Default: "bold"
            "TextBgGradientColor": "#CCCCCC",    // Default: ""
            "ActionType": "reply",    // Possible values: "reply", "open-url", "location-picker", "share-phone", "none"; Default: "reply"
            "ActionBody": "Action Text",    // Action-specific data
            "ImageScaleType": "fit",    // Possible values: "fit", "crop", "fill"; Default: "fit"
            "Silent": "true",    // Possible values: "true", "false"; Default: "false"
            "FavIconUrl": "http://path.to/your/favicon",    // URL of the favicon
            "MapThumbnailUrl": "http://path.to/your/map/thumbnail",    // URL of the map thumbnail
            "MapScaleType": "fit",    // Possible values: "fit", "crop", "fill"; Default: "fit"
            "MapZoomLevel": 50    // Integer value between 0 and 100; Default: 50
        }
    ]
}
"""
