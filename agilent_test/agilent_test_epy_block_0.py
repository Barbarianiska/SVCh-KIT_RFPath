import numpy as np
from gnuradio import gr

class MyBlock(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="My Block",
            in_sig=[np.float32],
            out_sig=[np.uint8])

    def work(self, input_items, output_items):
        # Получаем входной сигнал
        input_signal = input_items[0]
        
        # Добавляем постоянную смещения 40
        input_signal_with_offset = input_signal + 40
        
        # Инициализируем bit_up и bit_down
        bit_up = False
        bit_down = False
        
        # Проверяем наличие колебаний в заданных интервалах для bit_up
        for value in input_signal_with_offset:
            if 45 <= value <= 55:
                bit_up = True
                break
        
        # Проверяем наличие колебаний в заданных интервалах для bit_down
        for value in input_signal_with_offset:
            if 25 <= value <= 45:
                bit_down = True
                break
                
        # Формируем байт на основе найденных битов
        if bit_up and bit_down:
            byte_value = 0b00000011  # 11
        elif bit_up:
            byte_value = 0b00000010  # 10
        elif bit_down:
            byte_value = 0b00000001  # 01
        else:
            byte_value = 0b00000000  # 00
        
        # Заполняем выходной массив
        output_items[0][:] = byte_value
        
        # Возвращаем количество обработанных элементов
        return len(output_items[0])