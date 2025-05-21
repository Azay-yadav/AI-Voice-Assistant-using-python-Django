import multiprocessing
import time

# To run Jarvis
def startJarvis():
    print("Process 1 is running.")
    from main import start
    start()  # This will call eel.start(...)

# To run hotword (after frontend loads)
def listenHotword():
    print("Process 2 is running.")
    time.sleep(3)  # Wait for frontend to load controller.js
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    # Start frontend first
    p1 = multiprocessing.Process(target=startJarvis)
    p1.start()

    # Start hotword after frontend is loaded
    p2 = multiprocessing.Process(target=listenHotword)
    p2.start()

    # Wait for main app to finish
    p1.join()

    # Kill hotword process if still running
    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stopped.")
