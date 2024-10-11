import numpy as np
from scipy.interpolate import interp1d
from scipy.io import wavfile


# 此脚本用于收集噪音时对文件进行预处理
def apply_transfer(signal, transfer, interpolation='linear'):
    constant = np.linspace(-1, 1, len(transfer))  # 等差切分
    interpolator = interp1d(constant, transfer, interpolation)  # 一维线性插值，将离散函数还原成连续函数，
    return interpolator(signal)


# hard limiting, 将声音放大x倍，更改动态范围限制器
def limiter(x, treshold=0.8):
    transfer_len = 1000
    transfer = np.concatenate([np.repeat(-1, int(((1 - treshold) / 2) * transfer_len)),
                               np.linspace(-1, 1, int(treshold * transfer_len)),
                               np.repeat(1, int(((1 - treshold) / 2) * transfer_len))])
    return apply_transfer(x, transfer)


# smooth compression: if factor is small, its near linear, the bigger it is the
# stronger the compression
# 进行硬拐点压缩已将声音值的振幅降低到阈值以上，然后通过振幅增益因子放大整个信号
def arctan_compressor(x, factor=2):
    constant = np.linspace(-1, 1, 1000)  # 在-1 到 1 内返回1000个间隔
    transfer = np.arctan(factor * constant)  # 对数组构成的内容做2倍反函数
    transfer /= np.abs(transfer).max()  # 除以极值降低到最大阈值以内
    return apply_transfer(x, transfer)


if __name__ == '__main__':
    sr, x = wavfile.read("D:/Code/Noise/NoiseRecogniztion/utils/01_0_moveDown.wav")
    x = x / np.abs(x).max()  # x scale between -1 and 1

    x2 = limiter(x)
    x2 = np.int16(x2 * 32767)
    wavfile.write("output_limit.wav", sr, x2)

    x3 = arctan_compressor(x)
    x3 = np.int16(x3 * 32767)
    wavfile.write("output_comp.wav", sr, x3)
