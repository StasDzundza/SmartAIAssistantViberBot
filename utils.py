import requests
import mimetypes

mimetypes.init()

def is_media_file(fileName):
    mimestart = mimetypes.guess_type(fileName)[0]

    if mimestart != None:
        mimestart = mimestart.split('/')[0]

        if mimestart in ['audio', 'video']:
            return True

    return False

def download_file(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")