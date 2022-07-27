import numpy as np
from 分帧加窗 import enframe


def STEn(x, win, inc, number=None):
    """
    计算短时能量函数
    :param x:
    :param win:
    :param inc:
    :return:
    """
    X = enframe(x, win, inc, number)
    s = np.multiply(X, X)
    return np.sum(s, axis=1)


def STMn(x, win, inc):
    """
    计算短时平均幅度计算函数
    :param x:
    :param win:
    :param inc:
    :return:
    """
    X = enframe(x, win, inc)
    s = np.abs(X)
    return np.mean(s, axis=1)


def STZcr(x, win, inc, number=None, delta=0):
    """
    计算短时过零率
    :param x:
    :param win:
    :param inc:
    :return:
    """
    absx = np.abs(x)
    x = x - np.mean(x)
    x = np.where(absx < delta, 0, x)
    X = enframe(x, win, inc, number)
    X1 = X[:, :-1]
    X2 = X[:, 1:]
    s = np.multiply(X1, X2)
    sgn = np.where(s < 0, 1, 0)
    return np.sum(sgn, axis=1)


def FrameTimeC(frameNum, frameLen, inc, fs):
    """
    计算帧长
    :param frameNum:
    :param frameLen:
    :param inc:
    :param fs:
    :return:
    """
    ll = np.array([i for i in range(frameNum)])
    return ((ll - 1) * inc + frameLen / 2) / fs
