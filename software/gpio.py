from nicegui import ui,app,context
import RPi.GPIO as GPIO
import time as time
from enum import Enum
from index import pps_label,lock_label


class pin(Enum):
    LOCK = 10
    PPS = 9

def pps_callback(pin):
    global pps_label
    if pps_label is None:
        return
    for e in pps_label:
        e.name="radio_button_checked"
    time.sleep(0.3)
    for e in pps_label:
        e.name="radio_button_unchecked"

def lock_callback(pin):
    global lock_label
    if lock_label is None:
        return
    if GPIO.input(pin):
        for e in lock_label:
            e.name="lock_open_right"
    else:
        for e in lock_label:
            e.name="lock"

def startup():
    print("statup")

    GPIO.setmode(GPIO.BCM)
    #PPS Signal
    GPIO.setup(pin.PPS.value,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    #Lock
    GPIO.setup(pin.LOCK.value,GPIO.IN,pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(pin.PPS.value, GPIO.RISING, callback=pps_callback)
    GPIO.add_event_detect(pin.LOCK.value, GPIO.BOTH, callback=lock_callback)

    app.storage.general["fixed_value"] = 0#rubidium.value_to_float(rubidium.read_current_value())