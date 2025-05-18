#Проверка работы нейронной сети
def neuroTest():
    from seversdk import transcribe, transribeInit

    model = transribeInit()
    print(transcribe(model, "test.mp3"))
    
neuroTest()