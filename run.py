import multiprocessing
import subprocess
# To run Machideau
def startJarvis():
        print("Process is running.")
        from main import start
        start()
    

if __name__ == '__main__':
        p = multiprocessing.Process(target=startJarvis)
        p.start()
        p.join()

        print("system stop")