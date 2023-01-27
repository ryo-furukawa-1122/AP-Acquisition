import pyvisa
import time
import numpy as np
import nidaqmx as ni
import matplotlib.pyplot as plt
import csv

# input = ['Dev4/ai0']
# output = ['Dev4/ao0']

# def record(
#     outdata,
#     fs = 2 *1e6,
#     input_mapping=input,
#     output_mapping=output
# ):
#     nsamples = outdata.shape[0]
#     with ni.Task() as read_task, ni.Task() as write_task:
#         for o in output_mapping:
#             print(o)
#             aochan = write_task.ao_channels.add_ao_voltage_chan(o)
#             aochan.ao_max = 3.5   # output range of USB-4431
#             aochan.ao_min = -3.5

#         for i in input_mapping:
#             print(i)
#             aichan = read_task.ai_channels.add_ai_voltage_chan(i)
#             aichan.ai_min = -10
#             aichan.ai_max = 10

#         for task in (read_task, write_task):
#             task.timing.cfg_samp_clk_timing(rate=fs, source='OnboardClock', samps_per_chan=nsamples)
        
#         write_task.triggers.start_trigger.cfg_dig_edge_start_trig(read_task.triggers.start_trigger.term)
#         write_task.write(outdata, auto_start=False)
#         write_task.start()
#         indata = read_task.read(nsamples)
        
#     return indata

rm = pyvisa.ResourceManager()
resource_list = rm.list_resources()
func = rm.open_resource(resource_list[1])

func.write(":SOURce1:TRIGger[1]:BURst:SLOPe")

frequencies = np.arange(200, 900, 20)  #in kHz
voltage_amp = 2  #AC 10 V

func.write(f":SOURce1:VOLTage:LEVelIMMediate:AMPLitude {voltage_amp} VPP")

# sr = 500 * 1e3
# duration = 100 * 1e-3
# samples = int(sr * duration)

# trig_timing = 50 * 1e-3
# trig_duration = 5 * 1e-3
# trig_voltage = 3
# trig_rise = int(sr * trig_timing)
# trig_fall = int(sr * (trig_timing + trig_duration))

# t = np.linspace(0, duration, samples, endpoint=False)
# sig = np.zeros(samples)
# sig[trig_rise:trig_fall] = trig_voltage

all_data = {int(f): [] for f in frequencies}

trials = 1
p_voltage = {}
for frequency in frequencies:
    print(f"Setting frequency to {frequency}")
    func.write(f":SOURce1:FREQuency:FIXed {frequency}k")

    for trial in range(trials):
        func.write(":OUTPut1:STATe ON")
        trial_data = {}

        # indata = record(
        #     sig,
        #     fs = 20 * 1e6,
        #     input_mapping=input,
        #     output_mapping=output
        # )

        # trial_data[frequency] = indata
        # all_data[frequency] += [indata]

        func.write(":OUTPut1:STATe OFF")
        time.sleep(0.5)

    # p_voltage[frequency] = all_data.mean()
    time.sleep(0.5)


#Figure
plt.subplot(211)
# plt.plot(t, sig)
plt.title("Trigger")
plt.ylabel('Voltage (V)')
plt.xlabel('Time (s)')

plt.subplot(212)
for frequency in frequencies:
    plt.plot(t, p_voltage[frequency], label=(f'{frequency} kHz'))
plt.title('Recorded signal')
plt.legend()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (s)')

plt.tight_layout()
plt.show()


#Save
# with open(f'data/{frequency}.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(t, trial_data)
