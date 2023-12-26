from pydub import AudioSegment 
import os

files = os.listdir(os.getcwd())
wavs = [f for f in files if f.startswith("合成语音") and f.endswith(".wav")]
for wav in wavs:
	audio = AudioSegment.from_file(wav)
	rate = int(wav[4:-4])
	print(f"{wav}语速{rate}长度{len(audio)}，乘积{rate*len(audio)}")

wavs = [f for f in files if f.startswith("补长合成语音") and f.endswith(".wav")]
for wav in wavs:
	audio = AudioSegment.from_file(wav)
	print(f"{wav}长度{len(audio)}")

wavs = [f for f in files if f.startswith("拉伸合成语音") and f.endswith(".wav")]
for wav in wavs:
	audio = AudioSegment.from_file(wav)
	rate =float(wav[6:-4])
	print(f"{wav}倍速{rate}长度{len(audio)}，乘积{rate*len(audio)}")
