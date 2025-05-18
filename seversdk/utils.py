import os
import ffmpeg
import random
import string

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