import pandas as pd

def process_csv_file(input_file, output_file):
    # Читаем исходный CSV файл
    df = pd.read_csv(input_file, header=None)
    
    # Выводим первые несколько строк для проверки
    print("Original DataFrame:")
    print(df.head())
    
    # Отбрасываем первые две строки заголовка
    df = df.iloc[2:]
    
    # Выводим DataFrame после удаления заголовка
    print("\nDataFrame after dropping the header rows:")
    print(df.head())
    
    # Проверяем количество столбцов
    if df.shape[1] != 5:
        raise ValueError("Expected 5 columns in the original data, but got {}".format(df.shape[1]))
    
    # Оставляем только первые два столбца (время и напряжение)
    df = df[[0, 1]]
    
    # Переименовываем столбцы
    df.columns = ['Time_s', 'Voltage_V']
    
    # Преобразуем данные в числовой формат
    df['Time_s'] = df['Time_s'].astype(float)
    df['Voltage_V'] = df['Voltage_V'].astype(float)
    
    # Преобразуем время из секунд в миллисекунды
    df['Time_ms'] = df['Time_s'] * 1000
    
    # Выбираем нужные столбцы и переименовываем их
    df = df[['Time_ms', 'Voltage_V']]
    df.columns = ['Time (ms)', 'Voltage (V)']
    
    # Сохраняем результат в новый файл Excel
    df.to_excel(output_file, index=False)
    print("\nProcessed DataFrame saved to", output_file)

# Пример использования функции
input_file = 'E:/csv.csv'
output_file = 'E:/output.xlsx'
process_csv_file(input_file, output_file)