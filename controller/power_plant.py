class PowerPlant():
    def __init__(self, total_power: float, module_power: float):
        self._total_power = total_power
        self._module_power = module_power
        self._panels_amount = 3*round((total_power/module_power)/3)
        self.total_power = self.panels_amount*self.module_power
    
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

    @panels_amount.setter
    def panels_amount(self, value):
       self._panels_amount = value
    
    @total_power.setter
    def total_power(self, value):
        self._total_power = value

    @module_power.setter
    def module_power(self, value):
        self._module_power = value

    @panels_amount.deleter
    def panels_amount(self):
       del self._panels_amount

    @total_power.deleter
    def total_power(self):
        del self._total_power

    @module_power.deleter
    def module_power(self):
        del self._module_power

    # endregion

if __name__ == '__main__':
    power_plant = PowerPlant(105.0, 0.54)