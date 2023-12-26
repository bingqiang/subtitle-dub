from pydub import AudioSegment 
import os

files = os.listdir(os.getcwd())
wavs = [f for f in files if f.startswith("合成语音") and f.endswith(".wav")]

# 打印文件列表
for wav in wavs:
	audio = AudioSegment.from_file(wav)
	if len(audio)<10000 :
		补长 = 10000 - len(audio)
		new_audio = audio + AudioSegment.silent(补长)
		new_audio.export(f"补长{wav}", format="wav")
		print(f"{wav}补长了{补长}毫秒")
