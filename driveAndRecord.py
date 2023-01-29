# %%
import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys

# %%
# Connection to instruments
try:
    rm = pyvisa.ResourceManager()
    # resource_list = rm.list_resources()
    func = rm.open_resource('USB0::0x0D4A::0x000D::9338635::INSTR')
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
except:
    print('Failed to connect to instruments...')
    sys.exit(0)

# %%
def record(ch):
    fs = osci.query('SARA?')
    fs = fs[len('SARA '):-5]
    fs = float(fs)

    vd = osci.query(f'C{ch}:VDIV?')
    vd = vd[len(f'C{ch}:VDIV '):-2]
    vd = float(vd)

    voff = osci.query(f'C{ch}:OFST?')
    voff = voff[len(f'C{ch}:OFST '):-2]
    voff = float(voff)

    # osci.write(':STOP')
    osci.write('TRMD NORM')
    osci.write('WFSU SP, 1, NP, 0, FP, 0')
    osci.write(f'C{ch}:WF? DAT2')
    osci.chunk_size = 1024**3

    wave = osci.query_binary_values(f'C{ch}:WF? DAT2', datatype='b', is_big_endian=True)

    wave = list(map(float, wave))
    wave = np.array(wave)
    v = wave * (vd / 25) - voff  # in V

    x = np.arange(0, len(wave), 1)
    t = x/fs  # in s

    return np.c_[t, v]

# %%
# func.write(":SOURce1:BURst:STATe ON")  # Set at burst mode
func.write(':SOURce1:CONTinuous:IMMediate')

frequencies = np.arange(200, 900, 100)  # in kHz
voltage_amp = 2  # AC 10 V

func.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {voltage_amp} VPP")

all_data = [[0] for i in range(len(frequencies))]
p_voltage = [[0] for i in range(len(frequencies))]
# print(all_data)

# %%
ch = 2  # Channel of the oscilloscope
trials = 3
for i in range (len(frequencies)):
    all_data[i] = [0 for j in range(trials)]

# %%
for i in range(len(frequencies)):
    print(f"Setting frequency to {frequencies[i]}")
    func.write(f":SOURce1:FREQuency:FIXed {frequencies[i]}k")

    for j in range(-1, trials):
        if j == -1:
            print('Start')
        else:
            print(f'Trial: {j+1}')
            func.write(':OUTPut1:STATe ON')
            func.write('*TRG')
            # func.write(':SOURce1:BURSt:TRIGger:NCYCles 2000')  # 50 cycles
            indata = record(ch=2)
            func.write(":OUTPut1:STATe OFF")
            
            time.sleep(0.5)
            all_data[i][j] = indata[:, 1]

    all = np.array(all_data)
    p_voltage[i] = all.mean(axis=1)[i]
    time.sleep(0.5)

    t = indata[:, 0]

    # Figure
    plt.subplot(211)
    plt.title('Signal')
    plt.ylabel('Voltage (mV)')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.tick_params(labelbottom=False, labelleft=True, labelright=False, labeltop=False)
    for j in range(trials):
        plt.plot(t*1e6, all[i, j]*1e3, label=(f'{frequencies[i]} kHz'), color='black', alpha=0.5)

    plt.subplot(212)
    plt.plot(t*1e6, p_voltage[i]*1e3, label=(f'{frequencies[i]} kHz'), color='black')
    plt.title('Mean signal')
    plt.legend()
    plt.ylabel('Voltage (mV)')
    plt.xlabel('Time (\u03bcs)')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)

    # plt.tight_layout()
    plt.legend().remove()
    plt.show()
    plt.savefig(f'data/{frequencies[i]}.png')
    plt.close()

    #csv
    save_csv = np.c_[t, p_voltage[i]]
    np.savetxt(f'data/{frequencies[i]}.csv', save_csv, delimiter=',')

# %%
