import multiprocessing
from playsound import playsound
import time
p = multiprocessing.Process(target=playsound, args=("beep-02.mp3",))
p.start()
time.sleep(1)
p.terminate()