import json

class Metrics:
    #Максимальное количество потоков
    def getMaxThread() -> int:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        return data['thread_count_max']
    
    #Количество запущенных потоков
    def getThreadsCount() -> int:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        return data['thread_count']
    
    def setThreadsCount(count: int) -> None:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        data['thread_count'] = count
        with open('metrics/variables.json', 'w') as f:
            json.dump(data, f)
            
    #Очередь задач
    def getQueue() -> list:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        return data['queue']
    
    def setQueue(queue: list) -> None:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        data['queue'] = queue
        with open('metrics/variables.json', 'w') as f:
            json.dump(data, f)
            
    #Обработанные файлы
    def getHandledFiles() -> list:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        return data['handled_files']
    
    def setHandledFiles(handledFiles: list) -> None:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        data['handled_files'] = handledFiles
        with open('metrics/variables.json', 'w') as f:
            json.dump(data, f)
            
    #Версия программы
    def getVersion() -> str:
        with open('metrics/variables.json', 'r') as f:
            data = json.load(f)
        return data['version']