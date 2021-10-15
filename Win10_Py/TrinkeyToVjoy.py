"""
Takes raw Trinkey output from COM to vjoy controller instance inputs
"""
import sys
import serial
import pyvjoy
from serial.tools import list_ports

#variable definition
#Default Slider deadzone: full range
SLDR_MIN = 0
SLDR_MAX = 65535
#vjoy device ID
DEV_ID = 1
#Slider deadzones
SLDR_MIN_0 = 100
SLDR_MAX_0 = 65515

SLDR_MIN_1 = 50
SLDR_MAX_1 = 65250

#vjoy axis range
AXIS_MIN = 1
AXIS_MAX = 32768

#Ask for trinkey ID
trkID = int(input("Insert Trinkey ID for calibration: "))

#trinkey id elif switch
if trkID == 0:
    SLDR_MIN = SLDR_MIN_0
    SLDR_MAX = SLDR_MAX_0
elif trkID == 1:
    SLDR_MIN = SLDR_MIN_1
    SLDR_MAX = SLDR_MAX_1
else:
    print("Unrecognized Trinkey ID. Will use default value.")

#Search for ports
slider_trinkey_port = None
ports = list_ports.comports(include_links=False)
for p in ports:
    if p.pid is not None:
        print("Port:", p.device, "-", hex(p.pid), end="\t")
        if p.pid == 0x8102:
            slider_trinkey_port = p
            print("Found Slider Trinkey")
            trinkey = serial.Serial(p.device)
            break
else:
    print("Slider Trinkey port not found.")
    sys.exit()

#pyvjoy init
dev = pyvjoy.VJoyDevice(1)

#Loop for input decoding and pyvjoy comm
while True:
    x = trinkey.readline().decode('utf-8')
    if not x.startswith("Slider: "):
        continue

    #Read Slider position from Serial port
    sliderPos = int(float(x.split(": ")[1]))
    #Calculate slider pos without deadzone clamp
    sliderFracPos = float(sliderPos - SLDR_MIN) / (SLDR_MAX - SLDR_MIN)


    #Calculate axis position relative to slider position
    axisPos = int(sliderFracPos * (AXIS_MAX - AXIS_MIN)) + AXIS_MIN

    
    #Clamp lower limit
    axisPos = max(AXIS_MIN, axisPos)
    #Clamp upper limit
    axisPos = min(AXIS_MAX, axisPos)

    #Write to API and update, print log to console
    dev.data.wAxisX = axisPos
    dev.update()
    print("Axis X set to ", axisPos)


    