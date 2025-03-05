import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE

# Setup LoRa board
BOARD.setup()

class LoRaReceiver(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceiver, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_freq(433.0)  # Ensure same frequency as sender
        self.set_pa_config(pa_select=1)
        self.set_sync_word(0x12)  # Ensure same sync word as sender
        self.set_spreading_factor(7)  # Must match sender
        self.set_dio_mapping([0, 0, 0, 0, 0, 0])  # Map DIO0 to RX Done
        self.set_mode(MODE.RXCONT)  # Continuous receive mode

    def on_rx_done(self):
        payload = self.read_payload(nocheck=True)
        message = bytes(payload).decode(errors='ignore')  # Decode received bytes
        print(f" Received: {message}")
        self.send_ack()
        self.set_mode(MODE.RXCONT)  # Continue receiving
    
    def send_ack(self):
        ack_message = "ACK"
        print(" Sending Acknowledgment")
        self.write_payload(list(ack_message.encode()))  # Encode string to bytes
        self.set_mode(MODE.TX)  # Start transmission
        time.sleep(1)
        self.set_mode(MODE.RXCONT)  # Switch back to receive mode

# Run the receiver
lora = LoRaReceiver(verbose=False)

try:
    while True:
        time.sleep(1)  # Keep script running
except KeyboardInterrupt:
    print("\n Stopping LoRa receiver...")
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
