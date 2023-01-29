import pyvisa
import time

rm = pyvisa.ResourceManager()
resource_list = rm.list_resources()
print(resource_list)
inst = rm.open_resource('USB0::0x0D4A::0x000D::9338635::INSTR')
inst.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 2 VPP")

frequencies = [200, 300, 400, 500]

for frequency in frequencies:
    inst.write(":OUTPut1:STATe ON")
    print(f"Setting frequency to {frequency}")
    inst.write(f":SOURce1:FREQuency:FIXed {frequency}k")
    inst.write("*TRG")
    inst.write(':SOURce1:BURSt:TRIGger:NCYCles 50')
    inst.write(":OUTPut1:STATe OFF")
    time.sleep(1)
