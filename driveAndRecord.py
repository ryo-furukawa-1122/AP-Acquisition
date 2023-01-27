import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv

# Connection to instruments
try:
    rm = pyvisa.ResourceManager()
    # resource_list = rm.list_resources()
    func = rm.open_resource('USB0::-adress of multifunction generator-')
    osci = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
except:
    print('Failed to connect to instruments...')
    sys.exit(0)

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

    osci.write(':STOP')
    osci.write('WFSU SP, 1, NP, 0, FP, 0')
    osci.write(f'C{ch}:WF? DAT2')
    osci.chunk_size = 1024**3

    wave = osci.query_binary_values(f'C{ch}:WF? DAT2', datatype='b', is_big_endian=True)

    wave = list(map(float, wave))
    wave = np.array(wave)
    v = wave * (vd / 25) - voff  # in V

    x = np.arange(0, len(wave), 1)
    t = x/fs  # in s

    return np._[t, v]

func.write(":SOURce1:BURst:STATe ON")  # Set at burst mode

frequencies = np.arange(200, 900, 20)  # in kHz
voltage_amp = 2  # AC 10 V

func.write(f":SOURce1:VOLTage:LEVelIMMediate:AMPLitude {voltage_amp} VPP")

all_data = {int(f): [] for f in frequencies}
p_voltage = {int(f): [] for f in frequencies}

ch = 2  # Channel of the oscilloscope
trials = 1
for frequency in frequencies:
    all_data[frequency] = {int(trial): [] for trial in trials}

for frequency in frequencies:
    print(f"Setting frequency to {frequency}")
    func.write(f":SOURce1:FREQuency:FIXed {frequency}k")

    for trial in trials:
        func.write(":OUTPut1:*TRG")
        func.write(':OUTPut1:STATe ')
        trial_data = {}

        indata = record(ch=2)

        trial_data[frequency] = indata[:, 1]
        all_data[frequency] += [indata[:, 1]]

        func.write(":OUTPut1:STATe OFF")
        time.sleep(0.5)

    p_voltage[frequency] = all_data.mean()
    time.sleep(0.5)

    t = indata[:, 0]

    # Figure
    plt.subplot(211)
    plt.title('Signal')
    plt.ylabel('Voltage (mV)')
    for trial in trials:
        plt.plot(t*1e6, all_data[frequency, trial]*1e3, label=(f'{frequency} kHz'))

    plt.subplot(212)
    plt.plot(t*1e6, p_voltage[frequency]*1e3, label=(f'{frequency} kHz'))
    plt.title('Mean signal')
    plt.legend()
    plt.ylabel('Voltage (mV)')
    plt.xlabel('Time (\u03bcs)')

    plt.tight_layout()
    plt.savefig(f'data/{frequency}.png')

    #csv
    save_csv = np.c_[t, p_voltage[frequency]]
    np.savetxt(f'data/{frequency}.csv', save_csv, delimiter=',')



#Save
# with open(f'data/{frequency}.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(t, trial_data)
