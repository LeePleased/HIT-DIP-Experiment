# coding=utf-8
import wave
import pyaudio
import threading
from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt

from app import butter_bandpass_filter


# 定义过程常量.
CHUNK_SIZE = 64
AUGMENT_LIMIT = 4000

# 读取 .wav 音频文件.
file_path = "data/wav/banjo.wav"
wav_file = wave.open(file_path, "rb")

# 实例化 audio 对象, 流读入.
audio = pyaudio.PyAudio()
r_stream = audio.open(
    format=audio.get_format_from_width(wav_file.getsampwidth()),
    channels=wav_file.getnchannels(),
    rate=wav_file.getframerate(),
    output=True
)

data = None
smp_rate = wav_file.getframerate()

# 声明一个线程锁,
lock = threading.Lock()


def make_graph(y, x=None):
    return 

    if x is None:
        x = np.arange(y.shape[0])

    for serial in range(0, x.shape[0]):
        plt.plot([x[serial], x[serial]], [0, y[serial]], c="b")
        plt.scatter([x[serial]], [y[serial]], c="r", s=10)


def freq_analysis():
    # plt.ion()

    while True:
        if data is None:
            continue

        lock.acquire()
        plt.clf()

        channel_0 = data[:, 0]
        channel_1 = data[:, 1]

        plt.subplot(241)
        make_graph(channel_0)
        # plt.ylim(-33000, 33000)
        plt.plot(channel_0, c="r")
        plt.title("Time domain: 0")

        plt.subplot(242)
        freq_0 = np.fft.fft(channel_0)
        make_graph(freq_0)
        plt.plot(np.abs(freq_0), c="b")
        plt.yticks([])
        plt.title("Frequency domain: 0")

        plt.subplot(243)
        f_channel_0 = butter_bandpass_filter(channel_0, 0.1, AUGMENT_LIMIT, smp_rate, 5)
        plt.plot(f_channel_0, c="black")
        plt.yticks([])
        plt.title("Filtered time: 0")

        plt.subplot(244)
        f_freq_0 = np.fft.fft(f_channel_0)
        plt.plot(np.abs(f_freq_0), c="green")
        plt.yticks([])
        plt.title("Filter frequency: 0")

        plt.subplot(245)
        make_graph(channel_1)
        # plt.ylim(-33000, 33000)
        plt.plot(channel_1, c="r")
        plt.title("Time domain: 1")

        plt.subplot(246)
        freq_1 = np.abs(np.fft.fft(channel_1))
        make_graph(freq_1)
        plt.yticks([])
        plt.plot(np.abs(freq_1), c="b")
        plt.title("Frequency domain: 1")

        plt.subplot(247)
        f_channel_1 = butter_bandpass_filter(channel_1, 0.01, AUGMENT_LIMIT, smp_rate, 4)
        plt.plot(f_channel_1, c="black")
        plt.yticks([])
        plt.title("Filtered time: 1")

        plt.subplot(248)
        f_freq_1 = np.fft.ifft(f_channel_1)
        plt.plot(np.abs(f_freq_1), c="green")
        plt.yticks([])
        plt.title("Filtered frequency: 1")

        lock.release()
        plt.pause(0.01)


thread = threading.Thread(target=freq_analysis)
thread.start()

while True:
    music = wav_file.readframes(CHUNK_SIZE)
    r_stream.write(music)

    if music == "":
        break

    if not lock.locked():
        data = deepcopy(np.fromstring(music, dtype=np.short).reshape(-1, 2))

# 歌曲结束, 结束进程.
thread.join()
