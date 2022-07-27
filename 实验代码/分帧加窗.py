from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt


def enframe(x0, win, inc=None, number=None):

    if np.shape(x0)[1] != 1:
        x = np.average(x0, axis=1)
    else:
        x = x0
    nx = len(x)
    if isinstance(win, list) or isinstance(win, np.ndarray):
        nwin = len(win)
        nlen = nwin  # 帧长=窗长
    elif isinstance(win, int):
        nwin = 1
        nlen = win  # 设置为帧长
    elif isinstance(win, float):
        nwin = 1
        nlen = int(win)  # 设置为帧长
    if inc is None:
        ninc = nlen
    else:
        ninc = int(inc)
    nf = (nx - nlen + ninc) // ninc
    frameout = np.zeros((nf, nlen))
    indf = np.multiply(ninc, np.array([i for i in range(nf)]))
    for i in range(nf):
        frameout[i, :] = x[indf[i]:indf[i] + nlen]
    if isinstance(win, list) or isinstance(win, np.ndarray):
        frameout = np.multiply(frameout, np.array(win))
    if number is None:
        return frameout
    else:
        number = min(number, nf)
        return frameout[:number]


def emphasis(x):
    len = len(x)
    a = 0.97
    y = np.zeros(len - 1)
    for i in range(1, len):
        y[i] = x[i] - a*x[i - 1]
    y = y/np.max(y)
    return y


if __name__ == "__main__":
    #fs, data, nbits = wavfile.read('C3_1_y.wav')
    fs, data = wavfile.read('C3_1_y.wav')

    inc = 100
    wlen = 200
    en = enframe(data, wlen, inc)
    i = input('其实帧(i):')
    i = int(i)
    tlabel = i
    plt.subplot(4, 1, 1)
    x = [i for i in range((tlabel - 1) * inc, (tlabel - 1) * inc + wlen)]
    plt.plot(x, en[tlabel, :])
    plt.xlim([(i - 1) * inc + 1, (i + 2) * inc + wlen])
    plt.title('(a)当前波形帧号{}'.format(tlabel))

    plt.subplot(4, 1, 2)
    x = [i for i in range((tlabel + 1 - 1) * inc, (tlabel + 1 - 1) * inc + wlen)]
    plt.plot(x, en[i + 1, :])
    plt.xlim([(i - 1) * inc + 1, (i + 2) * inc + wlen])
    plt.title('(b)当前波形帧号{}'.format(tlabel + 1))

    plt.subplot(4, 1, 3)
    x = [i for i in range((tlabel + 2 - 1) * inc, (tlabel + 2 - 1) * inc + wlen)]
    plt.plot(x, en[i + 2, :])
    plt.xlim([(i - 1) * inc + 1, (i + 2) * inc + wlen])
    plt.title('(c)当前波形帧号{}'.format(tlabel + 2))

    plt.subplot(4, 1, 4)
    x = [i for i in range((tlabel + 3 - 1) * inc, (tlabel + 3 - 1) * inc + wlen)]
    plt.plot(x, en[i + 3, :])
    plt.xlim([(i - 1) * inc + 1, (i + 2) * inc + wlen])
    plt.title('(d)当前波形帧号{}'.format(tlabel + 3))

    #plt.show()
    plt.savefig('images/en.png')
    plt.close()
