import numpy
import ffmpeg
from pydub import AudioSegment
from pydub.silence import split_on_silence

# 入力 
stream = ffmpeg.input("Oreomeme.mp4") 
# 出力 
stream = ffmpeg.output(stream, "finished.wav") 
# 実行
ffmpeg.run(stream)


SOURCE_FILE =  'finished.wav'

sound = AudioSegment.from_file(SOURCE_FILE)

org_ms = len(sound)
print('original: {:.2f} [min]'.format(org_ms/60/1000))

for silence_thresh in range(-20, -60, -5):
    chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=silence_thresh, keep_silence=100)
    if not chunks:
        continue
    cutted_sound = sum(chunks)
    cutted_ms = len(cutted_sound)
    print('silence_thresh = {}: {:.2f} [min]'.format(silence_thresh, cutted_ms/60/1000))
    cutted_sound.export('silence_removed_{}.mp3'.format(silence_thresh), format='mp3')