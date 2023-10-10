import numpy as np
import math

class Mesa():
    def __init__(self, tam_mod: int, qtd_mod: int, pot_mod: float):
        self.tam_mod = tam_mod; 'largura do módulo em [mm]'
        self.qtd_mod = qtd_mod; 'Quantidade de módulos na usina'
        self.pot_mod = pot_mod; 'Potência dos módulos da usina'
        self.pot_usi = qtd_mod*pot_mod/1000; 'Potência Total da usina'
        self.margem_fileiras = 5; 'margem de quantidade de fileiras para cálculo posterior'
        # Se a potência da usina for inferior à 40 kWp, limitação para uma mesa
        if self.pot_usi > 40:
            if self.pot_usi > 800:
                # Se a potência da usina for superior à 800 kWp, limitação da quantidade de fileiras de 100 +/- 20
                self.qtd_fileiras_mesa = 100
                self.margem_fileiras = 20
            else:
                # Se a potência estiver entre 40 e 800, aplicar fórmula logarítmica abaixo (levar em consideração log como ln, Logaritmo natural)
                self.qtd_fileiras_mesa = 25.258*np.log(self.pot_usi)-84.863
            # Array do limite menor e maior para o cálculo da mesa
            self.lim_fileiras = [round(self.qtd_fileiras_mesa)-self.margem_fileiras, round(self.qtd_fileiras_mesa)+self.margem_fileiras]
            print('lim_fileiras: ', self.lim_fileiras)
            self.qtd_mesas = [(self.qtd_mod/3)/obj for obj in self.lim_fileiras]
            self.qnt_mesas_final = self.found_best_array(self.qtd_mesas) if self.pot_usi>=100 else 2
        else:
            self.qnt_mesas_final = 1

        self.fileiras_real_final = (self.qtd_mod/3)/self.qnt_mesas_final # type: ignore

        self.resto_fileiras = (self.qtd_mod/3)%self.qnt_mesas_final # type: ignore
        # Define quantidade de módulos por mesa em um array, a função full apenas preenche um array com o número desejado
        self.fileiras_mesa = np.full(self.qnt_mesas_final, math.floor(self.fileiras_real_final)) # type: ignore
        # Acréscimo de 1 fileira para cada resto que obteve
        for i in range(int(self.resto_fileiras)): self.fileiras_mesa[i] = self.fileiras_mesa[i]+1

    def found_best_array(self, _qtd_mesa):
        """Calcula a melhor disposição das mesas"""
        self.round_qtd_mesa = [round(obj) for obj in _qtd_mesa]
        self.minimum_value = None
        for i in range(self.round_qtd_mesa[1], self.round_qtd_mesa[0]+1):
            if self.qtd_mod%i == 0:
                if self.qtd_mod/3/i < self.qtd_fileiras_mesa+self.margem_fileiras:
                    return i
            if self.minimum_value is None:
                self.minimum_value = i
            if self.qtd_mod/3/i < self.qtd_fileiras_mesa+self.margem_fileiras:
                self.minimum_value = i if self.minimum_value > i else self.minimum_value
        return self.minimum_value

    def get_infos(self):
        print('Potência da usina: ', self.pot_usi)
        print('Quantidade de mesas: ', self.qnt_mesas_final)
        print('Quantidade de fileiras de módulos por mesa: ', self.fileiras_mesa)
        return self.fileiras_mesa


if __name__ == "__main__":
    obj = Mesa(1134, 192, 540)
    obj.get_infos()