import pyvisa
import argparse
from PIL import Image
import io


# argparser = argparse.ArgumentParser()
# argparser.add_argument('-a', '--address', required=True, help='VISA address like "TCPIP::{ipaddress}::INSTR"')
# argparser.add_argument('-o', '--output', help='Output file name (default: "screen.png")', default='screen.png')
# args = argparser.parse_args()


rm = pyvisa.ResourceManager()

# inst = rm.open_resource(args.address)

# print(rm.list_resources())

inst = rm.open_resource('USB0::0xF4EC::0xEE38::SDSMMEBQ4R4674::INSTR')
# print(inst.query('*IDN?'))

# inst.write('*RST')
inst.write(':STOP')
inst.write('CSVS')
# inst.write('FLNM')
# inst.write('ACQuire:STATE STOP')

# bmp_bin = inst.query_binary_values(':DISP:DATA?', datatype='B', container=bytes)
# img = Image.open(io.BytesIO(bmp_bin))
# img.save(args.output, args.output.split('.')[-1])



