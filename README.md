# 数字信号处理大作业-用波特沃斯滤波器处理音频信号

该仓库基于 Python 的 scipy, pyaudio 等库实现了对 mp3/wav 格式的音频信号进行实时频谱解析、滤波变换等。使用步骤：

> + 如果是 .mp3 格式的文件需要在 data 下新建文件夹 vaw，然后运行 python preprocessing.py；
> + 可以通过修改 demo.py 的配置参数然后 python 运行实时观察音频信号的频谱变化和滤波曲线；
> + 可以通过运行 app.py 并修改其内置参数（指定输入 wav 文件路径, 输出路径）对音频文件滤波；

实验环境：Ubuntu 16.04 + Python2.7（提示一下，我在 Python 3.6 下安装 pyaudio 要么失败，要么用不了）。
