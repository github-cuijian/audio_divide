from end_detection import vad_TwoThr, STEn, STZcr
from windows import *
from timefeature import FrameTimeC
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pyaudio
import wave


def demonstrate(amp, zcr, voiceseg, frameTime):
    """
    图示语音分割效果
    :param amp:
    :param zcr:
    :param voiceseg:
    :param frameTime:
    :return:
    """
    ampth = np.mean(amp[:NIS])
    zcrth = np.mean(zcr[:NIS])
    amp2 = 1 * ampth
    amp1 = 2 * ampth
    zcr2 = 2 * zcrth

    plt.subplot(3, 1, 1)
    plt.plot(time, data)

    plt.subplot(3, 1, 2)
    plt.plot(frameTime, amp)
    plt.plot(frameTime[3], amp2, '.k')
    plt.plot(frameTime[6], amp1, '.k')

    plt.subplot(3, 1, 3)
    plt.plot(frameTime, zcr)
    plt.plot(frameTime[3], zcr2, '.k')

    for i in range(vsl):
        plt.subplot(3, 1, 1)
        plt.plot(frameTime[voiceseg[i]['start']], 1, '.k')
        plt.plot(frameTime[voiceseg[i]['end']], 1, 'or')


        # plt.subplot(3, 1, 2)
        # plt.plot(frameTime[voiceseg[i]['start']], 1, '.k')
        # plt.plot(frameTime[voiceseg[i]['end']], 1, 'or')
        #
        # plt.subplot(3, 1, 3)
        # plt.plot(frameTime[voiceseg[i]['start']], 1, '.k')
        # plt.plot(frameTime[voiceseg[i]['end']], 1, 'or')

    plt.savefig('audio\\TwoThr.png')
    plt.show()
    plt.close()


if __name__ == '__main__':
    fs, data = wavfile.read('audio\\1.wav')
    original_data = data.copy()

    if data.dtype == 'int8':
        bits = 8
    elif data.dtype == 'int16':
        bits = 16
    elif data.dtype == 'int64':
        bits = 64
    data = data / (2 ** (bits - 1))

    N = len(data)
    wlen = 200      # 窗的宽度
    inc = 80        #非重叠部分宽度
    IS = 0.2
    overlap = wlen - inc
    NIS = int((IS * fs - wlen) // inc + 1)
    fn = (N - wlen) // inc + 1

    frameTime = FrameTimeC(fn, wlen, inc, fs)
    time = [i / fs for i in range(N)]

    wlen = hamming_window(wlen)
    voiceseg, vsl, SF, NF, amp, zcr = vad_TwoThr(data, wlen, inc, NIS)


    for i in range(vsl):
        # 将语音分段保存
        subaudio = original_data[voiceseg[i]['start'] * inc:voiceseg[i]['end'] * inc]
        wavfile.write(f'audio\\sub{i}.wav', fs, subaudio)
        # 打印每段语音的信息
        start = frameTime[voiceseg[i]['start']]
        end = frameTime[voiceseg[i]['end']]
        duration = frameTime[voiceseg[i]['duration']]
        print(f'第{i + 1}段声音，从{start}开始，到{end}结束，持续{duration}秒。')

    # 画图展示
    demonstrate(amp, zcr, voiceseg, frameTime)

