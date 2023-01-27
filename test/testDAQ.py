import nidaqmx as ni

with ni.Task() as task:
    print(task)
    task.ai_channels.add_ai_voltage_chan("Dev4/ai0")
    