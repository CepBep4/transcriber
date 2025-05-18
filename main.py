import threading
import multiprocessing
from worker import worker
from seversdk import logger, checkNewFile, Metrics, transribeInit

workMode = 't' # t - threadiing, p - multiprocess

def loadMetrics():
    #Версия программы
    version = Metrics.getVersion()
    
    #Максимальное число потоков
    MAX_THREADS = Metrics.getMaxThread()
    
    #Количество запущенных потокв
    threadsCount = Metrics.getThreadsCount()
    
    #Очередь задач
    queue = Metrics.getQueue()
    
    #Обработанные файлы
    handledFiles = Metrics.getHandledFiles()
    
    return (version, MAX_THREADS, threadsCount, queue, handledFiles)
    

#Менеджер по потокам, функция раздаёт задачи
def main():
    #Загружаем метрики
    version, MAX_THREADS, threadsCount, queue, handledFiles = loadMetrics()
    
    #Обнулям занятые потоки
    Metrics.setThreadsCount(0)
    threadsCount = 0
    
    #Обнуляем очередь
    Metrics.setQueue([])
    queue = []
    
    #Обнуляем обработанные файлы
    Metrics.setHandledFiles([])
    handledFiles = []
    
    #Инициализируем нейросеть, затем проверяем её
    pipe, cudaAwailable = transribeInit()
    
    #Логируем запуск программы
    logger.info(
        f"\nПрограмма запущена: True\
        \nMакс. кол-во потоков:{MAX_THREADS}\
        \nВерсия: {version}\
        \nРежим работы: {'threading' if workMode == 't' else 'multiprocessing' if workMode == 'p' else 'subprocess'}\
        \nCUDA доступна: {cudaAwailable}"
    )
    
    #Основной цикл работы программы
    while True:
        #Обновляем метрики
        version, MAX_THREADS, threadsCount, queue, handledFiles = loadMetrics()
        
        #Получаем новый файл
        newFile = checkNewFile(handledFiles)
        
        #Если файл не None
        if newFile:
            handledFiles.append(newFile)
            Metrics.setHandledFiles(handledFiles)
            
            #Если нет свободных потоков добаляем в очередь
            if threadsCount >= MAX_THREADS:
                queue.append(newFile)
                Metrics.setQueue(queue)
                
                logger.info(f"Файл {newFile} добавлен в очередь")
            
            else:
                #Логирование
                logger.info(f"Файл {newFile} взят в обработку")
                
                #Запуск нового процесса
                if workMode == "p":
                    multiprocessing.Process(
                        target=worker,
                        args=(newFile, pipe),
                        name=f"Thread-{threadsCount}"
                    ).start()
                elif workMode == "t":
                    threading.Thread(
                        target=worker,
                        args=(newFile, pipe),
                        name=f"Thread-{threadsCount}"
                    ).start()                    
                
                threadsCount += 1
                Metrics.setThreadsCount(threadsCount)
        
if __name__ == "__main__":
    main()
    #Логируем стандартное завершение программы
    logger.info("Программа завершила работу")