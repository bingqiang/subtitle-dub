import pysrt
import pyttsx3
from pydub import AudioSegment
import os
import tempfile
import sys
import re
import math

_output_format_ = "mp3"

# 为文字生成语音wav文件
def generate_text_audio(text, output_file, rate=200):
	print(f"为“{text}”生成音频，语速{rate}，输出{output_file}")
	engine = pyttsx3.init()
	engine.setProperty('rate', rate) 
	engine.save_to_file(text, output_file)
	engine.runAndWait()
	print(f"为“{text}”生成结束")

# 将文件名中的非法字符替换为下横线
def escape_filename(srt):
	return re.sub(r'[\/\\\:\*\?\"\<\>\|]','_', srt)

# 为字幕片段生成音频文件名
def sub_wav_name(sub):
	return escape_filename(str(sub.start)) + ".wav"

# 为字幕片段生成wav
def generate_sub_audio(sub, output_folder):
	print(f"开始为【{sub.start}】段生成音频")
	# wav标准名称以字幕片段开始时间命名
	wav_name = sub_wav_name(sub)
	print(f"音频文件名称{wav_name}")
	wav_file = os.path.join(output_folder, wav_name)
	# 按标准名称检查wav文件，如果存在，则：
	if os.path.exists(wav_file): 
		print(f"{os.path.abspath(wav_file)}已存在，不重复生成。");
		return
	# 按原速为片段内容合成临时wav
	temp_wav = tempfile.mktemp(suffix='.wav', prefix='tmp', dir=output_folder)
	print("临时文件", temp_wav)
	generate_text_audio(sub.text, temp_wav)
	# 检查临时wav时长
	temp_audio = AudioSegment.from_file(temp_wav, format="wav")
	sub_len = sub.duration.ordinal
	print(f"字幕时长{sub_len}，音频时长{len(temp_audio)}")
	if len(temp_audio) > sub_len or len(temp_audio) < sub_len - 700:
	# 如时长大于或严重小于字幕片段时长，则：
		# 根据wav时长和字幕片段计算应采用的语速
		new_rate = math.ceil(len(temp_audio)/sub_len * 200)
		# 循环尝试用更合适的语速创建音频
		while True:
			# 删除旧临时wav
			os.remove(temp_wav)
			# 用新的语速合成临时wav
			print(f"音频时长不合格，语速改为{new_rate}再合成")
			generate_text_audio(sub.text, temp_wav, new_rate)
			# 语速调快一档留待下个循环使用
			new_rate = round(new_rate * 1.1)
			# 检查临时wav时长
			temp_audio = AudioSegment.from_file(temp_wav, format="wav")
			# 如时长小于等于字幕片段时长，则跳出循环
			print(f"字幕时长{sub_len}，音频时长{len(temp_audio)}")
			if len(temp_audio) <= sub_len:
				print("音频时长合格")
				break
			if new_rate >= 450*1.1:
				print("已使用最高语速，音频时长仍不合格")
				break
	# 将临时wav时长用静默补齐，使之与字幕片段时长相等
	padding = sub_len - len(temp_audio)
	if padding > 0:
		print(f"音频补齐{padding}静默")
		temp_audio += AudioSegment.silent(padding)
	# 将补长后的wav导出为标准名称（以字幕片段开始时间命名）
	print(f"音频存储{wav_name}")
	temp_audio.export(os.path.join(output_folder, wav_name), format="wav")
	# 删除临时wav
	print(f"删除临时文件{temp_wav}")
	os.remove(temp_wav)

def generate_audio(srt_file, output_folder):
	srt_name = os.path.splitext(os.path.basename(srt_file))[0]
	print(f"字幕名称{srt_name}")
	# 输出文件查重
	output_file = os.path.join(output_folder, srt_name + "." + _output_format_)
	if os.path.exists(output_file): 
		print(f"{os.path.abspath(output_file)}已存在，请删除后再试。");
		return
		
	print(">>>>>>>>>>  开始分段合成音频 <<<<<<<<<<")
	# 分析srt为字幕片段列表
	subs = pysrt.open(srt_file)
	# 循环字幕片段列表：为字幕片段生成wav
	work_folder = os.path.join(output_folder, srt_name + "_work")
	print("工作目录：" + os.path.abspath(work_folder))
	if not os.path.exists(work_folder):
		os.makedirs(work_folder)
		print("创建工作目录")
	for sub in subs:
		print(f"=========当前段：【{sub.start}】：{sub.text}==========")
		generate_sub_audio(sub, work_folder)
		
	print(">>>>>>>>>>  开始整合音频 <<<<<<<<<<")
	# 循环字幕片段列表，拼接音频：
	audio = AudioSegment.empty() # 整合的音频
	for sub in subs:
		print(f"========= 当前段：【{sub.start}】==========")
		sub_wav = sub_wav_name(sub)
		sub_wav_segment = AudioSegment.from_wav(os.path.join(work_folder, sub_wav))
		print(f"段起点{sub.start.ordinal}，已整合音频长度{len(audio)}")
		# 如与已整合音频无重叠（当前段始点不早于已整合的音频结尾），则填补静默时间并拼接
		if sub.start.ordinal >= len(audio):
			print("无重叠，填补静默后追加")
			audio += AudioSegment.silent(sub.start.ordinal - len(audio))
			# 将片段相应的wav追加到音频中
			audio += sub_wav_segment
		# 如与已整合音频有重叠（已整合音频结尾晚于当前字幕段起点），则将音频对齐后叠加
		else:
			print("有重叠")
			# 当前段音频前补齐静默
			aligned_seg = AudioSegment.silent(sub.start.ordinal) + sub_wav_segment
			# 重叠已整合的音频和已对齐的当前字幕片段音频，谁长以谁为基准
			if len(aligned_seg)> len(audio):
				print(f"当前段结尾{len(aligned_seg)}，超出已整合结尾（{len(audio)}，以当前段为基准重叠")
				audio = aligned_seg.overlay(audio)
			else:
				print(f"当前段结尾{len(aligned_seg)}，未超过已整合结尾（{len(audio)}，以已整合音频为基准重叠")
				audio = audio.overlay(aligned_seg)
	# 将整合好的音频输出
	print(f"音频片段连接完成，保存为{output_file}")
	audio.export(output_file, format=_output_format_)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"usage: {sys.argv[0]} <srt_file_name>")
		exit()
	srt_file = sys.argv[1]
	output_folder = "."
	print(f"字幕文件：{os.path.abspath(srt_file)}")
	print(f"输出文件夹：{os.path.abspath(output_folder)}")
	generate_audio(srt_file, output_folder)