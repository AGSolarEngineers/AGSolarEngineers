import numpy as np
import math
from model.module import Module

class Mesa():
    def __init__(self, module: Module, module_amount: int):
      self._module = module
      self._module_amount = module_amount
      self._power_plant_power = self.module_amount*(self.module.power/1000)
      self._rows_margin = 5
      self._rows_amount = 0
      self._tables_amount = []
      self.calculate_rows()
    
    # region Getters & Setters

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
    def power_plant_power(self):
        return self._power_plant_power

    @power_plant_power.setter
    def power_plant_power(self, value):
        self._power_plant_power = value

    @power_plant_power.deleter
    def power_plant_power(self):
        del self._power_plant_power

    @property
    def rows_margin(self):
        return self._rows_margin

    @rows_margin.setter
    def rows_margin(self, value):
        self._rows_margin = value

    @rows_margin.deleter
    def rows_margin(self):
        del self._rows_margin

    @property
    def rows_amount(self):
        return self._rows_amount

    @rows_amount.setter
    def rows_amount(self, value):
        self._rows_amount = value

    @rows_amount.deleter
    def rows_amount(self):
        del self._rows_amount

    @property
    def tables_amount(self):
        return self._tables_amount

    @tables_amount.setter
    def tables_amount(self, value):
        self._tables_amount = value

    @tables_amount.deleter
    def tables_amount(self):
        del self._tables_amount

    # endregion

    def calculate_rows(self):
        if self.power_plant_power > 40:
            if self.power_plant_power > 800:
                # Se a potência da usina for superior à 800 kWp, limitação da quantidade de fileiras de 100 +/- 20
                self.rows_amount = 100
                self.rows_margin = 20
            else:
                # Se a potência estiver entre 40 e 800, aplicar fórmula logarítmica abaixo (levar em consideração log como ln, Logaritmo natural)
                self.rows_amount = 25.258*np.log(self.power_plant_power)-84.863
            # Array do limite menor e maior para o cálculo da mesa
            self.lim_fileiras = [round(self.rows_amount)-self.rows_margin, round(self.rows_amount)+self.rows_margin]
            # print('lim_fileiras: ', self.lim_fileiras)
            qtd_mesas = [(self.module_amount/3)/obj for obj in self.lim_fileiras]
            qnt_mesas_final = self.found_best_array(qtd_mesas) if self.power_plant_power>=100 else 2
        else:
            qnt_mesas_final = 1

        fileiras_real_final = (self.module_amount/3)/qnt_mesas_final # type: ignore

        resto_fileiras = (self.module_amount/3)%qnt_mesas_final # type: ignore
        # Define quantidade de módulos por mesa em um array, a função full apenas preenche um array com o número desejado
        fileiras_mesa = np.full(qnt_mesas_final, math.floor(fileiras_real_final)) # type: ignore
        # Acréscimo de 1 fileira para cada resto que obteve
        for i in range(int(resto_fileiras)): fileiras_mesa[i] = fileiras_mesa[i]+1

        fileiras_mesa = [x * 3 for x in fileiras_mesa]

        frequencia = {}
        for num in fileiras_mesa:
            if num in frequencia:
                frequencia[num] += 1
            else:
                frequencia[num] = 1
        
        self.tables_amount = [[frequencia[num], num] for num in set(fileiras_mesa)]

    def found_best_array(self, _qtd_mesa):
        """Calcula a melhor disposição das mesas"""
        self.round_qtd_mesa = [round(obj) for obj in _qtd_mesa]
        self.minimum_value = None
        for i in range(self.round_qtd_mesa[1], self.round_qtd_mesa[0]+1):
            if self.module_amount%i == 0:
                if self.module_amount/3/i < self.rows_amount+self.rows_margin:
                    return i
            if self.minimum_value is None:
                self.minimum_value = i
            if self.module_amount/3/i < self.rows_amount+self.rows_margin:
                self.minimum_value = i if self.minimum_value > i else self.minimum_value
        return self.minimum_value