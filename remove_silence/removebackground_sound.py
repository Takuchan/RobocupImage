import showWavefromSound

class removebackground_sound:
    def main(self):
        obj = showWavefromSound.showWavefromSound()
        print(obj.show_wavePlot())
    
if __name__ == "__main__":
    obj = removebackground_sound()
    obj.main()