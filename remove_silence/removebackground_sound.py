import sounddevice as sd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

device_list = sd.query_devices()
print(device_list)

sd.default.device = [0, 1]  # Input, Outputデバイス指定

class rmbackgroundsound:
    def callback(self, indata, frames, time, status):
        # indata.shape=(n_samples, n_channels)
        data = indata[::self.downsample, 0]
        shift = len(data)
        self.plotdata = np.roll(self.plotdata, -shift, axis=0)
        self.plotdata[-shift:] = data

    def update_plot(self, frame):
        """This is called by matplotlib for each plot update."""
        self.line.set_ydata(self.plotdata)
        return self.line,

    def main(self):
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


if __name__ == "__main__":
    rbs = rmbackgroundsound()
    rbs.main()
