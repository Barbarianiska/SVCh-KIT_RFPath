import pandas as pd
import struct

def convert_to_bin(input_file, output_file):
    # Читаем данные из Excel файла
    df = pd.read_excel(input_file)
    
    # Отбрасываем заголовки
    df = df.iloc[2:]
    
    # Убираем столбец времени, оставляем только значения напряжения
    voltages = df.iloc[:, 1]
    
    with open(output_file, 'wb') as bin_file:
        for voltage in voltages:
            # Вычитаем 3.2421875
            voltage_adjusted = voltage - 3
            
            # Переводим напряжение в ЕМР с использованием исправленной формулы
            emr_value = round(voltage_adjusted * 4096 )
            
            # Проверяем диапазон значений
            if emr_value < 0 or emr_value > 4095:
                raise ValueError("EMR value out of range: {}".format(emr_value))
            
            # Получаем шестнадцатеричные цифры
            w = (emr_value >> 12) & 0xF
            x = (emr_value >> 8) & 0xF
            y = (emr_value >> 4) & 0xF
            z = emr_value & 0xF
            
            # Преобразуем в формат wxyz -> z0xy
            transformed_value = (z << 12) | (0 << 8) | (x << 4) | y
            
            # Проверяем диапазон преобразованного значения
            if transformed_value < 0 or transformed_value > 65535:
                raise ValueError("Transformed value out of range: {}".format(transformed_value))
            
            # Печать промежуточных значений для отладки
            print(f"Original: {voltage:.6f}, Adjusted: {voltage_adjusted:.6f}, EMR: {emr_value:04X}, Transformed: {transformed_value:04X}")
            
            # Записываем значение в бинарный файл
            bin_file.write(struct.pack('>H', transformed_value))
    
    print(f"Data successfully converted and saved to {output_file}")
    
# Пример использования функции
input_file = 'E:/output.xlsx'
output_file = 'E:/output.bin'
convert_to_bin(input_file, output_file)