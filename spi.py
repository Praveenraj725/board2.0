import spidev
import RPi.GPIO as GPIO
import time

GPIO.cleanup()  # Free up any previously allocated GPIO
# LoRa SX1278 Pin Configuration
NSS_PIN = 8  # Chip Select
RESET_PIN = 22  # Reset Pin

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(NSS_PIN, GPIO.OUT)
GPIO.setup(RESET_PIN, GPIO.OUT)
GPIO.output(NSS_PIN, GPIO.HIGH)  # Default state

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0,0)  # SPI Bus 0, Device 0
spi.max_speed_hz = 1000000  # Lower speed for stability
spi.mode = 0

# Reset LoRa Module
def reset_lora():
    GPIO.output(RESET_PIN, GPIO.LOW)
    time.sleep(0.05)  # Increased delay for stability
    GPIO.output(RESET_PIN, GPIO.HIGH)
    time.sleep(0.1)

# Read Register
def read_register(register):
    GPIO.output(NSS_PIN, GPIO.LOW)
    response = spi.xfer2([register & 0x7F, 0x00])
    GPIO.output(NSS_PIN, GPIO.HIGH)
    return response[1]

# Check LoRa Version
def check_lora_version():
    reset_lora()
    time.sleep(0.1)  # Allow time after reset
    version = read_register(0x42)

    if version == 0 or version == 255:
        print("❌ LoRa Module Not Detected. Check wiring & SPI config.")
    else:
        print(f"✅ LoRa Module Version: {version}")

# Run Version Check
check_lora_version()

# Cleanup
spi.close()
GPIO.cleanup()

