import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE

# Setup LoRa board
BOARD.setup()

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_freq(433.0)  # Set frequency to 433 MHz
        self.set_pa_config(pa_select=1)
        self.set_sync_word(0x12)  # Sync word (must match receiver)
        self.set_spreading_factor(7)  # SF = 7 (good balance of range/speed)
        self.set_dio_mapping([1, 0, 0, 0, 0, 0])  # Map DIO0 to TX Done

    def send(self, message):
        print(f"🚀 Sending: {message}")
        self.write_payload(list(message.encode()))  # Convert string to bytes
        self.set_mode(MODE.TX)  # Start transmission

    def on_tx_done(self):
        print("✅ Transmission complete!")
        self.set_mode(MODE.STDBY)  # Return to standby mode
        time.sleep(1)  # Small delay before next transmission

# Initialize LoRa Sender
lora = LoRaSender(verbose=False)
counter = 0

try:
    while True:
        lora.send(f"Hello {counter}")
        counter += 1
        time.sleep(3)  # Send a message every 3 seconds
except KeyboardInterrupt:
    print("\n❌ Stopping LoRa sender...")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
