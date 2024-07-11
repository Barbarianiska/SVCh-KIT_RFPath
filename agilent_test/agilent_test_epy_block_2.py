import numpy as np
from gnuradio import gr

class adc_block(gr.sync_block):
    def __init__(self, samp_rate=32000, fsym=200):
        # Инициализация блока
        gr.sync_block.__init__(self,
                               name="adc_block",
                               in_sig=[np.float32],
                               out_sig=[np.uint8])
        self.samp_rate = samp_rate
        self.fsym = fsym
        self.N_sym = int(samp_rate / fsym)

    def work(self, input_items, output_items):
        in0 = input_items[0]  # Входной массив
        out = output_items[0]  # Выходной массив
        num_symbols = len(in0) // self.N_sym  # Количество символов
        out_idx = 0  # Индекс для записи в выходной массив
        print (self.N_sym)
        for i in range(num_symbols):
            
            symbol = in0[i * self.N_sym: (i + 1) * self.N_sym]  # Извлечение символа
            max_val = np.max(symbol)-40  # Максимальное значение символа
            min_val = np.min(symbol)-40  # Минимальное значение символа
            
            # Установка старшего и младшего битов
            high_signal = max_val > 10
            low_signal = min_val < -10

            if high_signal and low_signal:
                out[out_idx] = 0b11  # Сигнал и выше, и ниже нуля
            elif high_signal:
                out[out_idx] = 0b10  # Сигнал выше нуля
            elif low_signal:
                out[out_idx] = 0b01  # Сигнал ниже нуля
            else:
                out[out_idx] = 0b00  # Плоский сигнал
            print (out[out_idx])
            out_idx += 1  # Увеличение индекса выхода

        return out_idx  # Возвращает количество записанных байтов
