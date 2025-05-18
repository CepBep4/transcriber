from seversdk import Metrics
from seversdk import logger
from seversdk import convertMp3ToWav
from seversdk import transcribe
import time

#Рекурсивная функция для обработки файлов
def worker(path, pipe):
    #Засекаем время обработки
    timeStart = time.time()
    
    #Конвертация в WAV
    try:
        convertMp3ToWav(
            input_path=f'inbox_audio/{path}',
            output_path=f'results/{path.replace(".mp3", "")}.wav'
        )
    except Exception as e:
        logger.critical(f"Ошибка при конвертации файла {path}: {e}")
        logger.info(f"Файл {path} не обработан")
    
    #Транскрибация
    try:
        text = transcribe(pipe, f'results/{path.replace(".mp3", "")}.wav')
    except:
        logger.critical(f"Ошибка при транскрибации файла {path}: {e}")
        logger.info(f"Файл {path} не обработан")
    
    #Время окончания обработки
    timeEnd = time.time()
        
    #После работы выполняем проверку очереди
    logger.info(f"Поток завершил обработку, время обработки: {round(timeEnd-timeStart, 3)} секунд")
    
    #Проверяем очередь
    queue = Metrics.getQueue()
    if queue != []:
        logger.info(f"Файл {queue[0]} взят в обработку")
        Metrics.setQueue(queue[1:])
        worker(queue[0], pipe)
    else:
        threadsCount = Metrics.getThreadsCount()
        threadsCount -= 1
        Metrics.setThreadsCount(threadsCount)
        
        #Завершаем работу потока
        return None