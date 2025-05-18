import threading
import multiprocessing
from worker import worker
from seversdk import logger, checkNewFile, Metrics, transribeInit
import traceback

WORK_MODE = 't' # t - threadiing, p - multiprocess

#Инициализируем метрики
metrics = Metrics()

#Менеджер по потокам, функция раздаёт задачи
def main():
    #Инициализируем нейросеть, затем проверяем её
    pipe, cudaAwailable = transribeInit()
    
    #Логируем запуск программы
    logger.info(
        f"\nПрограмма запущена: True\
        \nMакс. кол-во потоков:{metrics.threadCountMax}\
        \nВерсия: {metrics.version}\
        \nРежим работы: {'threading' if WORK_MODE == 't' else 'multiprocessing' if WORK_MODE == 'p' else 'subprocess'}\
        \nCUDA доступна: {cudaAwailable}"
    )
    
    #Основной цикл работы программы
    while True:     
        #Сохраняем значение в метриках
        metrics.setHandledFiles()
        metrics.setQueue()
           
        #Получаем новый файл
        newFile = checkNewFile(metrics.handledFiles)
        
        #Если файл не None
        if newFile:
            metrics.handledFiles.append(newFile)
            
            #Если нет свободных потоков добаляем в очередь
            if metrics.threadConut >= metrics.threadCountMax:
                metrics.queue.append(newFile)
                
                logger.info(f"Файл {newFile} добавлен в очередь")
            
            else:
                #Логирование
                logger.info(f"Файл {newFile} взят в обработку")
                
                #Запуск нового процесса
                if WORK_MODE == "p":
                    multiprocessing.Process(
                        target=worker,
                        args=(newFile, pipe, metrics),
                        name=f"Thread-{metrics.threadConut}"
                    ).start()
                elif WORK_MODE == "t":
                    threading.Thread(
                        target=worker,
                        args=(newFile, pipe, metrics),
                        name=f"Thread-{metrics.threadConut}"
                    ).start()                    
                
                metrics.threadConut += 1
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        #Логируем ошибку
        logger.critical(f"Ошибка в основном цикле программы: {e}")
        traceback.print_exc()
    finally:
        #Логируем стандартное завершение программы
        logger.info("Программа завершила работу")
        
        #Сохраняем метрики
        metrics.setHandledFiles()
        metrics.setQueue()