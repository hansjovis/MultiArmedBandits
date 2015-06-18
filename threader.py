import threading
import main
import os
from algorithm import Algorithm
from dataHandler import DataGenerator

its_per_thread = 100
n_threads      = 5

def merge(n):
    algorithm = Algorithm()
    last = algorithm.lastmodel()
    models = [algorithm.load('model{}'.format(i)) for i in range(last-n+1, last+1)]
    model = DataGenerator(models)
    algorithm.predictor = model
    algorithm.save()

class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        main.main(its_per_thread, True)

# Create a few threads
threads = []
for i in range(n_threads):
    t = MainThread()
    threads.append(t)
    t.start()

# Wait for threads to finish
for t in threads:
    t.join()

merge(n_threads)
