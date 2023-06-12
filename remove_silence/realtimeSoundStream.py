import sounddevice as sd
import numpy as np
import time as tm# time measurement
duration = 10  # 10秒間収音する


class streamsound:
    count = 0
    def __init__(self) -> None:
        sd.default.device = [0, 1] # Input, Outputデバイス指定
        self.timer_start = tm.perf_counter()
    
    def callback(self, indata, frames, time, status):
        # indata.shape=(n_samples, n_channels)
        # print root mean square in the current frame
        # print(np.sqrt(np.mean(indata**2)))
        self.count += 1
        pause_time = tm.time()
        print(pause_time-self.timer_start)
        print(self.count)
        
    def main(self):
        with sd.InputStream(
                channels=1, 
                dtype='float32', 
                callback=self.callback
            ):
            sd.sleep(int(duration * 1000))
    
    
class reader:
    def main(self):
        objec = streamsound()
        objec.main()
    
if __name__ == "__main__":
    obj = reader()
    obj.main()

