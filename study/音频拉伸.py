from pydub import AudioSegment 
import os
import librosa
import pyrubberband
import soundfile as sf

y, sr = librosa.load(filepath, sr=None)
y_stretched = pyrubberband.time_stretch(y, sr, 1.5)
sf.write(analyzed_filepath, y_stretched, sr, format='wav')


files = os.listdir(os.getcwd())
wavs = [f for f in files if f.startswith("合成语音") and f.endswith(".wav")]

# 打印文件列表
for wav in wavs:
	audio = AudioSegment.from_file(wav)
	倍数 = 10000/len(audio)
	y, sr = librosa.load(wav, sr=None)
	y_stretched = pyrubberband.time_stretch(y, sr, 倍数)
	sf.write(f"拉伸{wav}", y_stretched, sr, format='wav')
	print(f"{wav}拉伸了{倍数}倍")
