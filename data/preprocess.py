import os
from pydub import AudioSegment


def trans_mp3_to_wav(in_path, out_path):
    song = AudioSegment.from_mp3(in_path)
    song.export(out_path, format="wav")


if __name__ == "__main__":
    for file in os.listdir("mp3"):
        i_path = os.path.join("mp3", file)

        raw = file.split(".")[-2]
        o_path = os.path.join("wav", raw + ".wav")
        trans_mp3_to_wav(i_path, o_path)
