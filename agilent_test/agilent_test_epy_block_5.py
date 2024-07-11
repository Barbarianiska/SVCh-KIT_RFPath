from gnuradio import gr
import numpy as np

class VariableUpdater(gr.sync_block):
    def __init__(self, var_holder=0):
        gr.sync_block.__init__(
            self,
            name="Variable Updater",
            in_sig=[np.float32],  # Входной сигнал типа float
            out_sig=[]
        )
        self.var_holder = var_holder

    def work(self, input_items, output_items):
        in_data = input_items[0]

        # Обновление переменной
        self.var_holder['variable'] = in_data[-1]  # Обновляем переменную последним значением входного сигнала

        return len(in_data)

class VariableUser(gr.sync_block):
    def __init__(self, var_holder):
        gr.sync_block.__init__(
            self,
            name="Variable User",
            in_sig=[np.float32],  # Входной сигнал типа float
            out_sig=[np.float32]  # Выходной сигнал типа float
        )
        self.var_holder = var_holder

    def work(self, input_items, output_items):
        in_data = input_items[0]
        out_data = output_items[0]

        # Использование обновленной переменной
        variable = self.var_holder['variable']

        # Выполнение каких-либо вычислений с использованием переменной
        out_data[:] = in_data * variable  # Например, умножение входного сигнала на переменную

        return len(out_data)

# Контейнер для переменной
var_holder = {'variable': 1.0}

# Создание блоков
variable_updater = VariableUpdater(var_holder)
variable_user = VariableUser(var_holder)

# Регистрация блоков для использования в GNU Radio
def register():
    return [variable_updater, variable_user]
