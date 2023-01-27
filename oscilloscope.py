import pyvisa
import sys
import numpy as np
import matplotlib.pyplot as plt

try:
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
except:
    print('Failed to connect to oscilloscope...')
    sys.exit(0)
osci.timeout = 30000

CHAN = 2
SAMPLE_RATE = osci.query('SARA?')
SAMPLE_RATE = SAMPLE_RATE[len('SARA '):-5]
SAMPLE_RATE = float(SAMPLE_RATE)
FS = 1e9

# osci.write('*RST')
# osci.write(':STOP')
osci.write('WFSU SP, 1, NP, 0, FP, 0')
osci.write('C2:WF? DAT2')
# osci.chunk_size = 1024**3

WAVEFORM = osci.query_binary_values('C2:WF? DAT2', datatype='i', is_big_endian=True)
# WAVEFORM = osci.query_binary_values('C2:WF? DAT2')

X = np.arange(0, len(WAVEFORM), 1)
TIME = X/FS
print(len(X))
# osci.write('FLNM')
# osci.write('ACQuire:STATE STOP')

plt.plot(TIME, WAVEFORM, color='black')
plt.show()



