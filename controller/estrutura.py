import math

class Estrutura():
    def __init__(self, tam_mod, qtd_mod, qtd_mesas, inv_mesa) -> None:
        self.tam_mod = tam_mod
        self.qtd_mod = qtd_mod
        self.qtd_mesas = qtd_mesas
        self.inv_mesa = inv_mesa

        self.tam_tot = ((self.tam_mod*self.qtd_mod)-21+(7*self.qtd_mod))/3; 'Largura total da mesa em [mm]'
        self.aux = math.floor(self.tam_tot/3005); 'quantidade de quantos espaçamentos de 3005 há no tamanho total'
        self.gap = self.tam_tot-(self.aux*3005); 'Sobra em [mm] do espaçamento'
        self.qtd_eixo = self.aux+1
        self.qtd_barra = None

        if self.gap>2400:
            self.gap_final = 500
            self.qtd_eixo += 1
            self.tam_sp = self.tam_tot-6010
            self.qtd_barra = (round((self.tam_sp/3005))+2)*3*qtd_mesas
        else:
            self.gap_final = self.gap/2
            self.tam_sp = (self.tam_tot-(2*(3005+self.gap_final)))
            self.qtd_barra = ((self.tam_sp/3005)+4)*3*qtd_mesas

        if(inv_mesa):
            self.i1810101 = 1
            self.qtd_barra += 3
        else:
            self.i1810101 = 0

        self.qtd_ctv = round(self.qtd_eixo/3)

        self.i5603112 = self.qtd_eixo*self.qtd_mesas
        self.i5603113 = self.i5603112
        self.i5601003 = (self.i5603112+self.i5603113)*4
        self.i5601002 = (self.i5603112+self.i5603113)*5
        self.i5601001 = (self.i5603112+self.i5603113)*6
        self.i5601101 = (self.i5603112+self.i5603113)/2.5
        self.i5603111 = self.i5603112*4
        self.i5603115 = self.i5603112
        self.i5603001 = self.qtd_ctv*self.qtd_mesas*2
        self.i5603002 = self.i5603001
        self.i5603110 = self.i5603115*6
        self.i5603011 = self.qtd_barra
        self.i1000207 = math.ceil((self.i5603112+self.i5603113)/5)*5
        self.i1030002 = self.i1000207*2
        self.i1020004 = self.i1000207
        self.i1000209 = math.ceil((((self.i5603111*2)+self.i5603110+(self.i5603001*8))*1.03)/5)*5
        self.i1030006 = self.i1000209*2 if self.inv_mesa else (self.i1000209*2)+12*self.i1810101
        self.i1020007 = self.i1000209
        self.i1000102 = self.i5603112*8
        self.i5601303 = math.ceil((self.i1000102/60))
        self.i5603009 = (self.qtd_mod/3+1)*6*self.qtd_mesas
        self.i1000304 = math.ceil((((self.i5603110*2)+(self.i5603009*2))*1.05)/5)*5
        self.i1000212 = math.ceil((self.i5603009*2)/5)*5
        self.i1020009 = self.i1000212
        self.i5605015 = self.qtd_mesas*12
        self.i7010006 = math.ceil((self.i5603009*0.1)/30)*30
        self.i5603010 = math.ceil(self.qtd_barra/80)
        self.i5601201 = self.i5603112*0.8

    def get_bill(self):
        return {
            'BOM':{
                '1': {'codigo':'5603112', 'descricao': 'PERFIL UE P1 - PILAR 150X60X2,65X1500MMM', 'quantidade': self.i5603112},
                '2': {'codigo':'5603113', 'descricao': 'PERFIL UE P2 - PILAR 150X60X2,65X723MM', 'quantidade': self.i5603113},
                '3': {'codigo':'5601003', 'descricao': 'FUNDACAO VERGALHO 2M CA-50 8,00MM CORTE DOBRA', 'quantidade': self.i5601003},
                '4': {'codigo':'5601002', 'descricao': 'FUNDACAO ESTRIVO DIAM.340MM CA-60 5,00MM NERVURADO', 'quantidade': self.i5601002},
                '5': {'codigo':'5601001', 'descricao': 'FUNDACAO ESTRIVO DIAM.190MM CA-60 4,20MM NERVURADO', 'quantidade': self.i5601001},
                '6': {'codigo':'5601101', 'descricao': 'ARAME RECOZIDO 18 TORCIDO', 'quantidade': self.i5601101},
                '7': {'codigo':'5603111', 'descricao': 'PERFIL L1" X 1/8"x 875 - MAO FRANCESA', 'quantidade': self.i5603111},
                '8': {'codigo':'5603115', 'descricao': 'PERFIL UE 100X50X17X2,25X 6000 - VIIGA', 'quantidade': self.i5603115},
                '9': {'codigo':'5603001', 'descricao': 'CT1 E CT2  - L1" X 1/8"X3250MM - CT1 - CONTRAVENTAMENTO', 'quantidade': self.i5603001},
                '10': {'codigo':'5603002', 'descricao': 'CT3 E CT4 - L1" X  1/8"X 3090MM - CONTRAVENTAMENTO', 'quantidade': self.i5603002},
                '11': {'codigo':'5603110', 'descricao': 'PERFIL L 2"X 1/8"X100MM - APOIO DE TERCAS', 'quantidade': self.i5603110},
                '12': {'codigo':'5603011', 'descricao': 'TUBO 80X40X1.5 X 6,010MM  - TERCAS CENTRAIS GALVANIZADAS À FOGO', 'quantidade': self.i5603011},
                '13': {'codigo':'1810101', 'descricao': 'BARRA ROSCADA 3/8"', 'quantidade': self.i1810101},
                '14': {'codigo':'1000207', 'descricao': 'PARAFUSO SEXTAVADO 1/2" X 1.1/4" SEXT 3/4" G.A13UNC R.I. ZINFOGO', 'quantidade': self.i1000207},
                '15': {'codigo':'1030002', 'descricao': 'ARRUELA LISA 1/2\' ZINFOGO', 'quantidade': self.i1030002},
                '16': {'codigo':'1020004', 'descricao': 'PORCA ASTM A563 G.A 13UNC 1/2" SEXT 3/4" ZINFOGO', 'quantidade': self.i1020004},
                '17': {'codigo':'1000209', 'descricao': 'PARAFUSO 3/8"X1.1/2" SEXT 9/16" RP A307 G.A 16UNC ZINFOGO', 'quantidade': self.i1000209},
                '18': {'codigo':'1030006', 'descricao': 'ARRUELA LISA 7/16 - para o parafuso 3/8', 'quantidade': self.i1030006},
                '19': {'codigo':'1020007', 'descricao': 'PORCA SEXTAVADA 3/8" SEXT 9/16" ASTM A563 G.A 16UNC ZINFOGO', 'quantidade': self.i1020007},
                '20': {'codigo':'1000212', 'descricao': 'PARAFUSO INOX SEXTAVADO RI M8X20 DIN933 A2', 'quantidade': self.i1000212},
                '21': {'codigo':'1020009', 'descricao': 'PORCA INOX 304 SEXT M8 FLANGEADA C/ SERRILHA DIN6923 A2', 'quantidade': self.i1020009},
                '22': {'codigo':'1000304', 'descricao': 'PARAFUSO BROC PB 12 14X1" HWH 5/16" TCP3 ECOSEAL', 'quantidade': self.i1000304},
                '23': {'codigo':'1000102', 'descricao': 'PARAFUSO FIXADOR HARDBOLT M10X150MM SEXT 9/16\' ECOSEAL 10K', 'quantidade': self.i1000102},
                '24': {'codigo':'5601303', 'descricao': 'BROCA TRYCUT SDS 10X255X315MM', 'quantidade': self.i5601303},
                '25': {'codigo':'5603009', 'descricao': 'CANTONEIRA 10CM MODELO 1 (OBILONGO DIST. 55MM)', 'quantidade': self.i5603009},
                '26': {'codigo':'5605015', 'descricao': 'TAMPA PONTEIRA PVC 80X40', 'quantidade': self.i5605015},
                '27': {'codigo':'7010006', 'descricao': 'FITA INSUTAPE (ARREDONDAR DE 30 EM 30 M)', 'quantidade': self.i7010006},
                '28': {'codigo':'5603010', 'descricao': 'SPRAY DE GALVANIZACAO A FRIO', 'quantidade': self.i5603010},
                '29': {'codigo':'5601201', 'descricao': 'TUBO PAPELAO 4000 X 400 X 5', 'quantidade': self.i5601201}
            }
        }

#if __name__ == "__main__":
#    obj = Structure(1048,300,1,False)
#    print(obj.get_bill())