import RPi.GPIO as GPIO
import time

PIR_PIN = 6  # GPIO connected to PIR sensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("Waiting for motion...")

try:
    while True:
        if GPIO.input(PIR_PIN):  # Motion detected
            print("Motion detected!")
            time.sleep(1)  # Avoid multiple detections
        else:
            print("No motion")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
