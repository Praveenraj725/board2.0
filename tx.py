import time
from SX127x.LoRa import LoRa
from SX127x.board_config import BOARD
from SX127x.constants import MODE

BOARD.setup()

class LoRaSender(LoRa):
    def __init__(self, verbose=False):
        super(LoRaSender, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_freq(433.0)  # ? Ensure same frequency as receiver
        self.set_pa_config(pa_select=1)
        self.set_sync_word(0x12)  # ? Ensure same sync word as receiver
        self.set_spreading_factor(7)  # ? Lower SF can improve reception


    def send(self, message):
        print(f"?? Sending: {message}")
        self.write_payload(list(message.encode()))
        self.set_mode(MODE.TX)
        time.sleep(2)  # ? Wait for transmission to complete
        self.set_mode(MODE.STDBY)  # ? Return to standby mode

# Run the sender
lora = LoRaSender(verbose=False)
counter = 0
while True:
    lora.send(f"Hello {counter}")
    counter += 1
