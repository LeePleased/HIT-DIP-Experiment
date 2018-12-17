# coding=utf-8
import tqdm
import numpy as np
from scipy import signal
from scipy.io import wavfile


def butter_bandpass_filter(data, low_cut, high_cut, fs, order=5):
    b, a = butter_bandpass(low_cut, high_cut, fs, order)
    y = signal.lfilter(b, a, data)
    return y


def butter_bandpass(low_cut, high_cut, fs, order):
    nyq = 0.5 * fs
    low = low_cut / nyq
    high = high_cut / nyq

    b, a = signal.butter(order, [low, high], btype='bandpass')
    return b, a


if __name__ == "__main__":
    IN_PATH = "data/wav/demons.wav"
    OUT_PATH = "filter/demons.wav"
    AUGMENT_LIMIT = 3000
    CHUNK_SIZE = 64

    wav_file = wavfile.read(IN_PATH)
    freq, sample = wav_file
    total_len = len(sample)

    channel_0, channel_1 = [], []
    for i in tqdm.tqdm(range(0, len(sample), CHUNK_SIZE)):

        seg_sample = sample[i: i + CHUNK_SIZE]
        seg_0 = seg_sample[:, 0]
        seg_1 = seg_sample[:, 1]

        f_seg_0 = butter_bandpass_filter(seg_0, 0.1, AUGMENT_LIMIT, freq, 5)
        f_seg_1 = butter_bandpass_filter(seg_1, 0.01, AUGMENT_LIMIT, freq, 4)

        channel_0.extend(f_seg_0.tolist())
        channel_1.extend(f_seg_1.tolist())

    f_channel = np.array([channel_0, channel_1], dtype=np.short).transpose()
    wavfile.write(OUT_PATH, freq, f_channel)

