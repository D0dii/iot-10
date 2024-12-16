#!/usr/bin/env python3

import time
import os
import board
import neopixel
import RPi.GPIO as GPIO
from mfrc522 import MFRC522
from datetime import datetime

# Constants
LED_PIN = board.D18        # GPIO pin for WS2812 LEDs
BUZZER_PIN = 21            # GPIO pin for buzzer (BCM numbering)
NUM_PIXELS = 8             # Number of WS2812 LEDs
BRIGHTNESS = 1.0 / 32      # LED brightness
LOG_FILE = "rfid_log.txt"  # File to log RFID scans

# Initialize WS2812 LEDs
pixels = neopixel.NeoPixel(LED_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

# Initialize GPIO for buzzer
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def beep_buzzer(duration=0.1):
    """Beep the buzzer for the specified duration."""
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def led_feedback():
    """Display a visual LED pattern on successful card scan."""
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), 
        (255, 255, 0), (0, 255, 255), (255, 0, 255), 
        (255, 255, 255), (63, 63, 63)
    ]
    for i, color in enumerate(colors):
        pixels[i] = color
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.show()

def log_rfid(uid):
    """Log the UID of the card and the current timestamp to a file."""
    with open(LOG_FILE, "a") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Card UID: {uid} at {timestamp}\n")
        print(f"Card UID: {uid} logged at {timestamp}")

def rfid_read():
    """Read RFID card and handle feedback and logging."""
    reader = MFRC522()
    scanned_uids = set()

    print("Place the card near the reader...")

    try:
        while True:
            (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
            if status == reader.MI_OK:
                (status, uid) = reader.MFRC522_Anticoll()
                if status == reader.MI_OK:
                    uid_str = '-'.join([str(x) for x in uid])
                    if uid_str not in scanned_uids:
                        print(f"Card detected: {uid_str}")
                        scanned_uids.add(uid_str)
                        log_rfid(uid_str)
                        beep_buzzer()
                        led_feedback()
                    else:
                        print("Card already scanned. Waiting for a new card...")
                    time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        GPIO.cleanup()

def test():
    print("\nStarting RFID reader with LED and buzzer feedback...")
    rfid_read()

if __name__ == "__main__":
    if os.getuid() == 0:
        test()
    else:
        print("\nThis program must be run with root privileges. Use 'sudo' to run it.")

