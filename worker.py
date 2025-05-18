from seversdk import Metrics, logger, transcribe, generateString
import time
import datetime
import random
import os
import json

#Рекурсивная функция для обработки файлов
def worker(path, pipe, metrics):
    #Засекаем время обработки
    timeStart = time.time()
    
    #Транскрибация
    try:
        text = transcribe(pipe, f'inbox_audio/{path}')
    except Exception as e:
        logger.critical(f"Ошибка при транскрибации файла {path}: {e}")
        logger.info(f"Файл {path} не обработан")
    
    #Записываем в папку results
    try:
        #Формируем данные для сохранения
        transcribeText = text
        sessionId = f"DC-{random.randint(10000, 99999)}_CALL-{generateString(8)}" #DC-10458_CALL-a1b2c3d4
        timeStamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        fileHandled = open(f'inbox_audio/{path}', "rb")
        
        #Сохраняем данные
        os.mkdir(f"results/{sessionId}")
        
        with open(f"results/{sessionId}/metadata.json", "w") as file:
            json.dump({
                "text": transcribeText,
                "session_id": sessionId,
                "time_stamp": timeStamp,
                "file_handled": path
            }, file)
            
        with open(f"results/{sessionId}/audio.mp3", "wb") as file:
            file.write(fileHandled.read())
            
        fileHandled.close()
        os.remove(f'inbox_audio/{path}')
        
        #Логируем успешное сохранение
        logger.info(f"Файл {path} обработан и сохранен: {sessionId}")
        
    except Exception as e:
        logger.critical(f"Ошибка при сохранении обработанного результата {path}: {e}")
        logger.info(f"Файл {path} обработан, но не сохранен")
        
    
    #Отправляем запрос на сервер
    ...

    
    #Время окончания обработки
    timeEnd = time.time()
        
    #После работы выполняем проверку очереди
    logger.info(f"Поток завершил обработку, время обработки: {round(timeEnd-timeStart, 3)} секунд")
    
    #Проверяем очередь
    if metrics.queue != []:
        logger.info(f"Файл {metrics.queue[0]} взят в обработку")
        notHandledFile = metrics.queue[0]
        metrics.queue.remove(notHandledFile)
        worker(notHandledFile, pipe, metrics)
    else:
        metrics.threadConut -= 1
        
        #Завершаем работу потока
        return None