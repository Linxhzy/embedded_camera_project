'''
调用麦克风录制5秒的音频并保存到dataset/raw/
'''
import pyaudio
import wave
import os
import time
CHUNK = 1024#音频块大小
FORMAT = pyaudio.paInt16#16位整数
CHANNELS = 1#单声道
RATE=16000#采样率
RECORD_SECONDS = 5#5秒
Filename = "dataset/raw/test_audio2.wav"
def record_audio():
    p = pyaudio.PyAudio()
    #打开麦克风
    try:
        stream = p.open(format = FORMAT,channels=CHANNELS,rate = RATE,input=True,frames_per_buffer=CHUNK)
    except Exception as e:
        print("失败")
        return
    print("开始录音...")
    frames=[]
    for i in range(0,int(RATE*RECORD_SECONDS/CHUNK)):
        data = stream.read(CHUNK)
        frames.append(data)
        time.sleep(CHUNK/RATE)
    print("结束")
    stream.stop_stream()
    stream.close()
    p.terminate()
    filename = Filename
    wf = wave.open(filename,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"文件保存在{filename}")
if __name__=="__main__":
    input("开始录音")
    record_audio()

