import requests
import time
import zhtts
import os

real_path = os.path.split(os.path.realpath(__file__))[0]

lang_dict = {
    '中文':'zh',
    '英语':'en',
    '日语':'jp'
}

def tts(text, spd, lang):
    url = f"https://fanyi.baidu.com/gettts?lan={lang_dict[lang]}&text={text}&spd={spd}&source=web"

    payload = {}
    headers = {
        'Cookie': 'BAIDUID=543CBD0E4FB46C2FD5F44F7D81911F15:FG=1'
    }

    res = requests.request("GET", url, headers=headers, data=payload)
    cs=0
    while res.content == b'' and cs<11:
        cs+=1
        res = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(0.1)
    if res.status_code == 200:
        return res.content
    else:
        return None


def get_voice(text, spd, filename, gen_type, lang):
    if gen_type == '在线':
        voice = tts(text, spd, lang)
        if voice is None:
            print("TTS failed")
            return None
        with open(filename+ ".mp3", "wb") as f:
            f.write(voice)
        # audio = AudioSegment.from_mp3(filename+'.mp3')
        # audio.export(filename+'.wav', format="wav")
        # os.remove(filename+'.mp3')
    elif gen_type == '本地':
        # 暂时支持中文
        tts_model = zhtts.TTS()
        tts_model.text2wav(text, filename+'.wav')

    return filename
