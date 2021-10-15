import time
import board
from analogio import AnalogIn
import adafruit_simplemath

analog_in = AnalogIn(board.POTENTIOMETER)


def read_sld(samples, min_val, max_val):
    sum_samples = 0
    for _ in range(samples):
        sum_samples += analog_in.value
    sum_samples /= samples  # ok take the average

    return adafruit_simplemath.map_range(sum_samples, 100, 65535, min_val, max_val)
def read_sld_raw(samples):
    sum_samples = 0
    for _ in range(samples):
        sum_samples += analog_in.value
    sum_samples /= samples  # ok take the average

    return sum_samples


while True:
    print("Slider:", round(read_sld_raw(10)))
    time.sleep(0.1)