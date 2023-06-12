import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import time

class showWavefromSound:
    count = 0
    def __init__(self):
        sd.default.device = [0, 1]  # Input, Outputデバイス指定

    def callback(self, indata, frames, time, status):
        # indata.shape=(n_samples, n_channels)
        self.count +=1
        data = indata[::self.downsample, 0]
        shift = len(data)
        self.plotdata = np.roll(self.plotdata, -shift, axis=0)
        self.plotdata[-shift:] = data
        self.wavedata = indata
        return indata
        

    def update_plot(self, frame):
        """This is called by matplotlib for each plot update."""
        self.line.set_ydata(self.plotdata)
        return self.line,

    def show_wavePlot(self):
        self.downsample = 10
        length = int(1000 * 44100 / (1000 * self.downsample))
        self.plotdata = np.zeros((length))

        fig, ax = plt.subplots()
        self.line, = ax.plot(self.plotdata)
        ax.set_ylim([-1.0, 1.0])
        ax.set_xlim([0, length])
        ax.yaxis.grid(True)
        fig.tight_layout()

        stream = sd.InputStream(
            channels=1,
            dtype='float32',
            callback=self.callback
        )
        ani = FuncAnimation(fig, self.update_plot, interval=30, blit=True)
        with stream:
            plt.show()
        return self.wavedata


if __name__ == "__main__":
    rbs = showWavefromSound ()
    rbs.show_wavePlot()
