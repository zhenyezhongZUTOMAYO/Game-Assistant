import time
import winsound
import threading
class timestamp:
    end=False
    def __init__(self,duration):
        self.duration=duration
    def is_time(self):
        while not self.end:
            winsound.Beep(400, 1000)
            time.sleep(0.2)
            winsound.Beep(300, 1000)
            time.sleep(0.2)
    def time_wake(self):
        time.sleep(self.duration * 60)
        thread_time = threading.Thread(target=self.is_time)
        thread_time.start()
        input(f"{self.duration}min计时已到!!!  任意键继续")
        self.end = True
def time_wake(duration):
    TimeStamp=timestamp(duration)
    TimeStamp.time_wake()
threads=[]
while(1):
    message=input('输入要计时的时间(min):')
    message=message.strip()
    if message==None:
        break
    if 's'==message[len(message)-1]:
        message=message.strip('s')
        duration=float(message)/60
    else:
        duration=float(message)
    if duration==0:
        break
    Thread_time=threading.Thread(target=time_wake , args=(duration,))
    threads.append(Thread_time)
    Thread_time.start()
for i in threads:
    i.join()