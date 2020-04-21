# -*- coding: utf-8 -*-


import speech_recognition as sr

IBM_USERNAME = '861322624@qq.com'
IBM_PASSWORD = 'Rl1711437'


if __name__ == '__main__':
    r = sr.Recognizer()
    # 语音文件输入
    harvard = sr.AudioFile('./harvard.wav')
    with harvard as source:
        audio = r.record(source)
    # print(type(audio))
    # 语音输入
    # mic = sr.Microphone()  # 麦克风
    # sr.Microphone.list_microphone_names()
    # with mic as source:
    #     r.adjust_for_ambient_noise(source)
    #     audio = r.listen(source)
    # 别的需要密匙，谷歌需要翻墙用不了
    text = r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language='zh-CN')
    print(type(text))
    print(text)
