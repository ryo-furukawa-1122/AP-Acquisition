import pyvisa
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv

def binaryToDecimal(n):
    return int(n, 2)

try:
    rm = pyvisa.ResourceManager()
    # print(rm.list_resources())
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
except:
    print('Failed to connect to oscilloscope...')
    sys.exit(0)
osci.timeout = 30000

fs = osci.query('SARA?')
fs = fs[len('SARA '):-5]
fs = float(fs)
print(fs)

# fs = 20e6
# osci.write(f'SARA, {fs}')

# fsref = osci.query('SARA?')
# fsref = fsref[len('SARA '):-5]
# print(f'Setted at {fsref} Hz')

vd = osci.query('C2:VDIV?')
vd = vd[len('C2:VDIV '):-2]
vd = float(vd)
print(vd)

voff = osci.query('C2:OFST?')
voff = voff[len('C2:OFST '):-2]
voff = float(voff)
print(voff)

osci.write(':STOP')
osci.write('WFSU SP, 1, NP, 0, FP, 0')
osci.write('C2:WF? DAT2')
osci.chunk_size = 1024**3

osci.write('CSVS_SAVE SAVE, OFF')
osci.write('GET_CSV? SAVE, ON')
osci.write('*SAV')
osci.write('SCSV YES')

wave = osci.query_binary_values('C2:WF? DAT2', datatype='b', is_big_endian=True)
# print(f'test: {wave[0]}')

wave = list(map(float, wave))
wave = np.array(wave)
v = wave * (vd / 25) - voff

x = np.arange(0, len(wave), 1)
print(len(x))
t = x/fs

#csv
save_csv = np.c_[t, v]
np.savetxt('data/sample.csv', save_csv, delimiter=',')

#Figure
plt.plot(t*1e6, v*1e3, color='black')
plt.xlabel('Time (\u03bcs)')
plt.ylabel('Voltage (mV)')
plt.show()



