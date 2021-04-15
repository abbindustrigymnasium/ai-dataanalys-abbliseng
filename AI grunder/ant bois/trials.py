import logging
import threading
import time

def thread_function(name):
    print("Hewwo from "+str(name)+"!")
    time.sleep(2)
    print("Bahbah from "+str(name)+" 0/")

if __name__ == "__main__":
    print("Starting this bad boi")
    for i in range(10):
        x = threading.Thread(target=thread_function, args=(i,))
        x.start()
    # print("Time to gooo")
    print("Going! :D")