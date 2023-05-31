import numpy as np
import nidaqmx as ni
from nidaqmx import constants
from scipy import signal

fs = 100000
dur = 10
n_samp = fs * dur

chunk_dur = 1
chunk_size = fs * chunk_dur        # チャンクサイズ
n_chunk = int(n_samp / chunk_size)  # チャンク数

# def get_wav_chunk(i: int):
#     start = i * chunk_dur
#     end = start + chunk_dur
#     t = np.arange(start, end, 1/fs)  # 1チャンク分の
#     wav = np.sin(2 * np.pi * t)      #  1 Hz sin波
#     return wav

def gate(i: int):
    start = i * chunk_dur
    end = start + chunk_dur
    t = np.arange(start, end, 1/fs)  # 1チャンク分の
    wav = (signal.square(2*np.pi*(3)*t)+1)/2
    return wav

with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")  # タスクにoutputチャンネル追加
    task.timing.cfg_samp_clk_timing(
        rate = fs,              # サンプリングレート
        samps_per_chan = n_samp # 全体のサンプル数
    )
    task.out_stream.output_buf_size = chunk_size * 2 # バッファサイズをチャンク数の2倍に
    task.out_stream.regen_mode = constants.RegenerationMode.DONT_ALLOW_REGENERATION # 波形の再生成を禁止
    for i_chunk in range(n_chunk):
        chunk = gate(i_chunk)
        task.write(chunk, auto_start=True)  # 波形出力
    task.wait_until_done()              # 待機
    task.stop()                         # 終了
