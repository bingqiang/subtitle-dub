分析srt为字幕片段列表
循环字幕片段列表：
	为字幕片段生成mp3
创建配音音频
循环字幕片段列表：
	如果片段不是第一个，则：
		计算本片段开头与上片段结尾的时间间隔长度
		在音频中追加该长度的静默
	将片段相应的mp3追加到音频中
配音音频保存为文件

函数 为每个字幕片段生成mp3：
	mp3标准名称以字幕片段开始时间命名
	按标准名称检查mp3文件，如果存在，则：
		打印“文件已存在”
		返回
	按原速为片段内容合成临时mp3
	检查临时mp3时长
	如时长大于或严重小于字幕片段时长，则：
		根据mp3时长和字幕片段计算应采用的语速
		用新的语速合成临时mp3
		检查临时mp3时长
		如时长大于字幕片段时长，则：
			将临时mp3按比例加速
	将临时mp3时长用静默补齐，使之与字幕片段时长相等
	将临时mp3改名为标准名称（以字幕片段开始时间命名）

