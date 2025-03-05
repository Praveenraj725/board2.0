import time
import RPi.GPIO as GPIO
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE  # Import MODE constants

# Disable warnings and setup board
GPIO.setwarnings(False)
BOARD.setup()

class MyLoRa(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)  # Start in sleep mode
        self.set_freq(868E6)  # Set frequency to 868 MHz
        self.set_pa_config(pa_select=1)  # Power amplifier setting
        self.set_sync_word(0x12)  # Sync word (should match receiver)
        self.set_spreading_factor(7)  # Adjust spreading factor

    def on_tx_done(self):
        print(" Transmission Done.")
        self.set_mode(MODE.STDBY)  # Return to standby mode after sending

lora = MyLoRa()

def send_message(message):
    print(f"Sending: {message}")
    lora.write_payload(list(message.encode()))
    lora.set_mode(MODE.TX)  # Use MODE.TX instead of LoRa.MODE_TX

if __name__ == "__main__":
    try:
        while True:
            send_message("Hi")
            time.sleep(5)  # Delay between transmissions
    except KeyboardInterrupt:
        print("Stopping LoRa transmission...")
    finally:
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()  # Properly shutdown LoRa module
        GPIO.cleanup()  # Clean up GPIO
