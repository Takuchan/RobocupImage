import sounddevice as sd
import numpy as np
duration = 100  # 10秒間収音する


class streamsound:
    def __init__(self) -> None:
        sd.default.device = [0, 1] # Input, Outputデバイス指定

    
    def callback(self, indata, frames, time, status):
        # indata.shape=(n_samples, n_channels)
        # print root mean square in the current frame
        print(np.sqrt(np.mean(indata**2)))
        
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
        objec.callback()
    
if __name__ == "__main__":
    obj = reader()
    obj.main()

