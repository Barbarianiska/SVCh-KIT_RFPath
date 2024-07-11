from gnuradio import gr
import numpy as np

class FrequencyDetector(gr.sync_block):
    def __init__(self, sample_rate=32000):
        gr.sync_block.__init__(
            self,
            name="Frequency Detector",
            in_sig=[np.float32],  # Входной сигнал типа float
            out_sig=[np.float32]  # Выходной сигнал типа float
        )
        self.sample_rate = 32000

    def work(self, input_items, output_items):
        in_data = input_items[0]-40
        out_data = output_items[0]

        # Поиск пересечений нуля
        zero_crossings = np.where(np.diff(np.sign(in_data)))[0]

        # Определение времени между пересечениями нуля
        periods = np.diff(zero_crossings) / float(self.sample_rate)

        # Определение частоты как обратной величины периода
        if len(periods) > 0:
            frequency = 1.0 / periods
            # Усреднение значений частоты
            avg_frequency = np.mean(frequency)
        else:
            avg_frequency = 0.0

        # Заполнение выходного буфера значениями частоты
        out_data.fill(avg_frequency)

        # Возвращение количества обработанных выходных элементов
        return len(output_items[0])