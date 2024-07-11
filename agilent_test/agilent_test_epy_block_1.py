import numpy as np
from gnuradio import gr

class custom_block(gr.basic_block):
    def __init__(self, samp_rate=32000, offset=40, active_start=0.001, active_end=0.004, period=0.005):
        gr.basic_block.__init__(self,
            name="Custom Block",
            in_sig=[np.float32],
            out_sig=[np.uint8])
        
        self.samp_rate = samp_rate
        self.offset = offset
        self.active_start = int(active_start * samp_rate)
        self.active_end = int(active_end * samp_rate)
        self.period = int(period * samp_rate)
        self.counter = 0

    def forecast(self, noutput_items, ninput_items_required):
        ninput_items_required[0] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        noutput_items = len(out)
        n = min(len(in0), noutput_items)

        # Determine if the block is in the active phase
        self.counter += n
        self.counter %= self.period  # Ensure counter stays within [0, self.period)
        
        active = self.active_start <= self.counter < self.active_end

        # Debug prints
        print(f"Counter: {self.counter}, Active: {active}, Active start: {self.active_start}, Active end: {self.active_end}, Period: {self.period}")

        if active:
            for i in range(n):
                # Apply offset
                signal = in0[i] + self.offset
                
                # Determine bit_up and bit_down
                bit_up = 1 if 25 <= signal <= 35 else 0
                bit_down = 1 if 45 <= signal <= 55 else 0
                
                # Construct byte
                byte_val = (bit_up << 1) | bit_down
                out[i] = byte_val

            # Debug prints
            print(f"Active phase: {n} items processed.")
            print(f"Input items: {in0[:10]}")
            print(f"Output items: {out[:10]}")
        else:
            # When inactive, output zeros
            out[:n] = [0] * n
            print(f"Inactive phase: {n} items set to zero.")

        # Tell runtime system how many input items we consumed and output items we produced
        self.consume(0, n)
        return n
