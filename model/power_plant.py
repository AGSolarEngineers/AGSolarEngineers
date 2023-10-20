from model.concrete import Concreto
from model.estrutura import Estrutura
from model.tables import Mesa
from model.module import Module

class PowerPlant():
    def __init__(self, customers_name: str, cost_center: str, location: str, power: float, module: Module, inverter_table: bool):
        self._customers_name = customers_name
        self._cost_center = cost_center
        self._location = location
        self._power = round(power, 3)
        self._module = module
        self._module_amount = 0
        self._real_power = 0
        self._inverter_table = inverter_table
        self._tables = Mesa(module, 0)
        self._concrete = Concreto(0, 1.6, 0.15, 0.4, 0.2, 'H21')
        self._structures = []
        self.calculate_optmize()
    
    # region Getters & Setters

    @property
    def customers_name(self):
        return self._customers_name

    @customers_name.setter
    def customers_name(self, value):
        self._customers_name = value

    @customers_name.deleter
    def customers_name(self):
        del self._customers_name

    @property
    def cost_center(self):
        return self._cost_center

    @cost_center.setter
    def cost_center(self, value):
        self._cost_center = value

    @cost_center.deleter
    def cost_center(self):
        del self._cost_center

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @location.deleter
    def location(self):
        del self._location

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @power.deleter
    def power(self):
        del self._power

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value

    @module.deleter
    def module(self):
        del self._module

    @property
    def module_amount(self):
        return self._module_amount

    @module_amount.setter
    def module_amount(self, value):
        self._module_amount = value

    @module_amount.deleter
    def module_amount(self):
        del self._module_amount

    @property
    def real_power(self):
        return self._real_power

    @real_power.setter
    def real_power(self, value):
        self._real_power = value

    @real_power.deleter
    def real_power(self):
        del self._real_power

    @property
    def tables(self):
        return self._tables

    @tables.setter
    def tables(self, value):
        self._tables = value

    @tables.deleter
    def tables(self):
        del self._tables

    @property
    def inverter_table(self):
        return self._inverter_table

    @inverter_table.setter
    def inverter_table(self, value):
        self._inverter_table = value

    @inverter_table.deleter
    def inverter_table(self):
        del self._inverter_table

    @property
    def concrete(self):
        return self._concrete

    @concrete.setter
    def concrete(self, value):
        self._concrete = value

    @concrete.deleter
    def concrete(self):
        del self._concrete

    @property
    def structures(self):
        return self._structures

    @structures.setter
    def structures(self, value):
        self._structures = value

    @structures.deleter
    def structures(self):
        del self._structures
    # endregion

    def calculate_optmize(self):
        self.module_amount = round(3*round((self.power/(self.module.power/1e3))/3), 3)
        self.calculate_module_amount_defined()
        
    def calculate_module_amount_defined(self):
        self.structures = []
        self.real_power = self.module_amount*self.module.power/1e3
        self.tables = Mesa(self.module, self.module_amount)
        for table in self.tables.tables_amount:
            if not self.structures:
                structure = Estrutura(self.module, table[1], table[0], self.inverter_table)
            else:
                structure = Estrutura(self.module, table[1], table[0], False)
            self.structures.append(structure)
        structure_total = Estrutura(self.module, 0, 0, False)
        for dict in structure_total.bom:
            for structure in self.structures:
                structure_total.bom[dict]['quantidade'] = round(structure_total.bom[dict]['quantidade']+structure.bom[dict]['quantidade'],1)
                # print(structure_total.bom[dict]['quantidade'].__class__, structure.bom[dict]['quantidade'].__class__)
        self.structures.append(structure_total)
        self.concrete.base_amount = structure_total.bom['5603112']['quantidade']*2
        self.concrete.calculate_volume()

if __name__=='__main__':
    power_plant = PowerPlant('Rafael', '7.0000', 'Na Sua', 105.68, Module(1134, 2261, 540, 0, 0, 0, 0), True)