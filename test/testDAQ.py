import numpy as np
import nidaqmx as ni
from nidaqmx import constants
from scipy import signal

fs = 100e3
dur = 3 * 60  # in s
n_samp = int(fs * dur)
f = 20

def gate(i: int):
    t = np.arange(0, dur, 1/fs)
    wav = (signal.square(2*np.pi*f*t)+1)/2
    return wav

with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")
    for i_chunk in range(n_samp):
        chunk = gate(i_chunk)
        task.write(chunk, auto_start=True)
    task.wait_until_done()
    task.stop()
