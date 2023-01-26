import pyvisa
import time

rm = pyvisa.ResourceManager()
resource_list = rm.list_resources()
inst = rm.open_resource(resource_list[0])
print(resource_list)
inst.write(":OUTPut1:STATe ON")

frequencies = [200, 300, 400, 500]

for frequency in frequencies:
    print(f"Setting frequency to {frequency}")
    inst.write(f":SOURce1:FREQuency:FIXed {frequency}k")
    time.sleep(0.5)
    # inst.write("*TRG")
    time.sleep(0.5)

inst.write(":OUTPut1:STATe OFF")