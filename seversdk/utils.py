import os
import ffmpeg
import random
import string
import requests
import json

def generateString(length: int) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=length))

def checkNewFile(handlerFiles: list):
    #Собираем список всех файлов в папке inbox_audio
    inboxAudio = os.listdir('inbox_audio')
    
    #Перебираем все файлы, которые ещё не обработаны
    for fileName in inboxAudio:
        if fileName not in handlerFiles:
            return fileName
        
    #Если не нашли файлы, вёрнём None
    return None

def convertMp3ToWav(input_path: str, output_path: str) -> None:
    """
    Конвертирует MP3 в WAV через ffmpeg-python.
    
    Требования:
      • pip install ffmpeg-python
      • ffmpeg в PATH
    """
    (
        ffmpeg.input(input_path).output(output_path, format='wav', acodec='pcm_s16le', ar='44100', ac=2).run(overwrite_output=True)
    )
    
#Функция для отправки запроса на сервер
def sendHandledData(data, host):
    with open(f"results/{data['session_id']}/audio.mp3", 'rb') as file:
        files = {
            'file': (f"results/{data['session_id']}/audio.mp3", file, 'application/octet-stream')
        }
        data = {
            'json_data': json.dumps(data)
        }

        response = requests.post(host, files=files, data=data)
        
        #Возвращаем ответ сервера
        return response.ok