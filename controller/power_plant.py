from model.tables import Mesa


class PowerPlant():
    def __init__(self, total_power: float, module_power: int, module_length: int):
        self._total_power = round(total_power, 3)
        self._module_power = round(module_power/1000, 3)
        self._module_length = module_length 
        self._panels_amount = round(3*round((self._total_power/self._module_power)/3), 3)
        self.total_power = round(self.panels_amount*self.module_power, 3)
        self.mesas = Mesa(self.module_length, self.panels_amount, self.module_power)

        
    # region getters & setters

    @property
    def panels_amount(self):
       return self._panels_amount

    @property
    def total_power(self):
        return self._total_power

    @property
    def module_power(self):
        return self._module_power

    @property
    def module_length(self):
        return self._module_length

    @panels_amount.setter
    def panels_amount(self, value):
       self._panels_amount = round(value, 3)
    
    @total_power.setter
    def total_power(self, value):
        self._total_power = round(value, 3)

    @module_power.setter
    def module_power(self, value):
        self._module_power = round(value, 3)

    @module_length.setter
    def module_length(self, value):
        self._module_length = round(value, 3)

    @panels_amount.deleter
    def panels_amount(self):
       del self._panels_amount

    @total_power.deleter
    def total_power(self):
        del self._total_power

    @module_power.deleter
    def module_power(self):
        del self._module_power

    @module_length.deleter
    def module_length(self):
        del self._module_length

    # endregion

if __name__ == '__main__':
    power_plant = PowerPlant(105.0, 540, 1134)