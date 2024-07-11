from gnuradio import gr
import numpy as np

class CumulativeAveraging(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="Cumulative Averaging",
            in_sig=[np.float32],  # Входной сигнал типа float
            out_sig=[np.float32]  # Выходной сигнал типа float
        )
        self.cumulative_avg = 0.0
        self.count = 0

    def work(self, input_items, output_items):
        in_data = input_items[0]
        out_data = output_items[0]

        # Накопительное усреднение
        for value in in_data:
            self.count += 1
            self.cumulative_avg += (value - self.cumulative_avg) / self.count

        # Заполнение выходного буфера значением усредненного результата
        out_data[:] = self.cumulative_avg

        # Возвращение количества обработанных выходных элементов
        return len(out_data)