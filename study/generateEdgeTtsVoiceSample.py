import edge_tts
import asyncio

async def generateMp3(voice):
	print("声音：%s"%voice);
	output = '%s.mp3'%voice
	text = "现在是%s在播音"%voice[6:]
	tts = edge_tts.Communicate(text=text, voice=voice)
	await tts.save(output)

async def main():
	tasks = []
	with open("voices.txt", "r") as file:
		for line in file:
			if line.startswith("Name: zh-CN-"):
				voice = line[6:].strip()
				tasks.append(generateMp3(voice))
	results = await asyncio.gather(*tasks)
	for result in results:
		print(result)

if __name__ == '__main__':
	asyncio.run(main())