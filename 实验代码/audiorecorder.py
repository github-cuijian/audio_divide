import pyaudio
import wave
import time
import os
import numpy as np

def audiorecorder(path):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 16000
    RECORD_SECONDS = 60     # 设置录音时间
    WAVE_OUTPUT_FILENAME = path

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音,请说话......")
    time.sleep(0.7)

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if(i%15==0):
            print(i/15)
        data = stream.read(CHUNK)
        frames.append(data)
    print("录音结束.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def record_ten(path):
    path1 = 'D:\\崔健学习资料\\编程\\python\\数字信号处理实验\\实验代码\\audiosample\\'
    path2 = path
    file_dir = os.listdir(path1)
    i = 0
    for file in file_dir:
        if not os.path.isdir(file):
            file_name = path2 + file
            print('next number is: ', file[0])
            time.sleep(1)
            audiorecorder(file_name)
            time.sleep(1)
        else:
            print('can not!!!')
    print('recording finished')

if __name__ == '__main__':
    path = 'D:\\崔健学习资料\\编程\\python\\audio_divide\\实验代码\\audio\\'
    # record_ten(path)
    audiorecorder(path + '1.wav')