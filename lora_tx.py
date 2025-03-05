import time
import RPi.GPIO as GPIO
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD

# Disable warnings
GPIO.setwarnings(False)

# Ensure SPI and GPIO are initialized
BOARD.setup()

class MyLoRa(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)

    def on_tx_done(self):
        print("Transmission Done.")
        self.set_mode(LoRa.MODE_SLEEP)

lora = MyLoRa()
lora.set_mode(LoRa.MODE_TX)
lora.set_frequency(868E6)

def send_message(message):
    lora.write_payload(list(message.encode()))
    lora.set_mode(LoRa.MODE_TX)
    print(f"Sent: {message}")

if __name__ == "__main__":
    try:
        while True:
            send_message("Hi")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping LoRa transmission...")
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
