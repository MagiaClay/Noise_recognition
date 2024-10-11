import pyaudio
import wave
from Volum_authentic import arctan_compressor
import numpy as np
from scipy.interpolate import interp1d
from scipy.io import wavfile

# 命名规则 MR01_ID_Speed_Lable.wav
MR_num = 'CT'
speed = '230'
labels = ['moveDown', 'moveUp', 'normalV', 'moveIn', 'moveOut', 'normalIn', 'normalOut']
time = 15 # 慢了
max_idx = 200


# 注意更改默认麦克风
# 此处改为自动循环手动收集数据集，主要收集上噪音和下噪音
# 先进行机床下降的噪声收集，其次是上升，往返循环
# 此外需要构建CSV表进行存储，或者单独建一个


def get_audio(filepath, time):
    aa = str(input("是否开始录音？   （y/n）"))
    if aa == str("y"):
        CHUNK = 1024  # 每个缓冲多少帧
        FORMAT = pyaudio.paInt16  # 16位
        CHANNELS = 1  # 声道数
        RATE = 16000  # 采样率 8kHz
        RECORD_SECONDS = time  # 多少秒
        WAVE_OUTPUT_FILENAME = filepath  # 保存路径
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*" * 10, "开始录音：请在16秒内输入语音")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        volum_up(WAVE_OUTPUT_FILENAME, WAVE_OUTPUT_FILENAME)
    elif aa == str("n"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(filepath, time)


def get_audio_normal(filepath, time):
    CHUNK = 1024  # 每个缓冲多少帧
    FORMAT = pyaudio.paInt16  # 16位
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率 8kHz
    RECORD_SECONDS = time  # 多少秒
    WAVE_OUTPUT_FILENAME = filepath  # 保存路径
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*" * 10, "开始录音：请在14秒内输入语音")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    volum_up(WAVE_OUTPUT_FILENAME, WAVE_OUTPUT_FILENAME)
    print("*" * 10, "录音结束")

def volum_up(dir_path, save_path):
    sr, x = wavfile.read(dir_path)
    x = x / np.abs(x).max()  # x scale between -1 and 1
    x3 = arctan_compressor(x)  # 反三角增益函数
    x3 = np.int16(x3 * 32767)  # 将Int音频数组转换为float36， 即解压制
    wavfile.write(save_path, sr, x3)


def mr_move_noise(time):
    idx = 102  # 采集指引，每次尖端
    while idx < max_idx:
        if idx % 2 == 0:
            # MoveDown
            print(f'现在开始记录MoveDown，第{idx}次： ')
            save_path = "AudioDaraset/CT_MoveDown/"
            save_name = MR_num + '_' + str(idx) + '_' + speed + '_' + labels[0] + '.wav'
            path = save_path + save_name  # 完整路径
            get_audio(path, time)
            print("MoveDown完成")
        else:
            # MoveUp
            print(f'现在开始记录MoveUp，第{idx}次： ')
            save_path = "AudioDaraset/CT_MoveUP/"
            save_name = MR_num + '_' + str(idx) + '_' + speed + '_' + labels[1] + '.wav'
            path = save_path + save_name  # 完整路径
            get_audio(path, time)
            print("MoveUp完成")
        idx += 1
    print('All down')


def normal_voice(time):
    idx = 0
    aa  = str(input("是否开始录音？   （y/n）"))
    if aa == str("y"):
        while idx < (max_idx * 2):
            if idx % 2 == 0:
                # MoveDown
                print(f'现在开始记录MoveOut，第{idx}次： ')
                save_path = "D:/Code/Noise/NoiseRecogniztion/AudioDaraset/NormalOut/"
                save_name = MR_num + '_' + str(idx) + '_' + speed + '_' + labels[6] + '.wav'
                path = save_path + save_name  # 完整路径
                get_audio_normal(path, time)
                print("normalout完成")
            else:
                # MoveUp
                print(f'现在开始记录MoveIn，第{idx}次： ')
                save_path = "D:/Code/Noise/NoiseRecogniztion/AudioDaraset/NormalIn/"
                save_name = MR_num + '_' + str(idx) + '_' + speed + '_' + labels[5] + '.wav'
                path = save_path + save_name  # 完整路径
                get_audio_normal(path, time)
                print("normalIn完成")
            idx += 1
    else:
        print('s输入错误')
    print('All down')


if __name__ == '__main__':
    mr_move_noise(time=time) # 记录垂直运动
    # normal_voice(time) # 记录水平运动
