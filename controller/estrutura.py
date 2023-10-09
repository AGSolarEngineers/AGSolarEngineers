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
            '5603112':['PERFIL UE P1 - PILAR 150X60X2,65X1500MMM',self.i5603112],
            '5603113':['PERFIL UE P2 - PILAR 150X60X2,65X723MM',self.i5603113],
            '5601003':['FUNDACAO VERGALHO 2M CA-50 8,00MM CORTE DOBRA',self.i5601003],
            '5601002':['FUNDACAO ESTRIVO DIAM.340MM CA-60 5,00MM NERVURADO',self.i5601002],
            '5601001':['FUNDACAO ESTRIVO DIAM.190MM CA-60 4,20MM NERVURADO',self.i5601001],
            '5601101':['ARAME RECOZIDO 18 TORCIDO',self.i5601101],
            '5603111':['PERFIL L1" X 1/8"x 875 - MAO FRANCESA',self.i5603111],
            '5603115':['PERFIL UE 100X50X17X2,25X 6000 - VIIGA',self.i5603115],
            '5603001':['CT1 E CT2  - L1" X 1/8"X3250MM - CT1 - CONTRAVENTAMENTO',self.i5603001],
            '5603002':['CT3 E CT4 - L1" X  1/8"X 3090MM - CONTRAVENTAMENTO',self.i5603002],
            '5603110':['PERFIL L 2"X 1/8"X100MM - APOIO DE TERCAS',self.i5603110],
            '5603011':['TUBO 80X40X1.5 X 6,010MM  - TERCAS CENTRAIS GALVANIZADAS À FOGO',self.i5603011],
            '1810101':['BARRA ROSCADA 3/8"',self.i1810101],
            '1000207':['PARAFUSO SEXTAVADO 1/2" X 1.1/4" SEXT 3/4" G.A13UNC R.I. ZINFOGO',self.i1000207],
            '1030002':['ARRUELA LISA 1/2\' ZINFOGO',self.i1030002],
            '1020004':['PORCA ASTM A563 G.A 13UNC 1/2" SEXT 3/4" ZINFOGO',self.i1020004],
            '1000209':['PARAFUSO 3/8"X1.1/2" SEXT 9/16" RP A307 G.A 16UNC ZINFOGO',self.i1000209],
            '1030006':['ARRUELA LISA 7/16 - para o parafuso 3/8',self.i1030006],
            '1020007':['PORCA SEXTAVADA 3/8" SEXT 9/16" ASTM A563 G.A 16UNC ZINFOGO',self.i1020007],
            '1000212':['PARAFUSO INOX SEXTAVADO RI M8X20 DIN933 A2',self.i1000212],
            '1020009':['PORCA INOX 304 SEXT M8 FLANGEADA C/ SERRILHA DIN6923 A2',self.i1020009],
            '1000304':['PARAFUSO BROC PB 12 14X1" HWH 5/16" TCP3 ECOSEAL',self.i1000304],
            '1000102':['PARAFUSO FIXADOR HARDBOLT M10X150MM SEXT 9/16\' ECOSEAL 10K',self.i1000102],
            '5601303':['BROCA TRYCUT SDS 10X255X315MM',self.i5601303],
            '5603009':['CANTONEIRA 10CM MODELO 1 (OBILONGO DIST. 55MM)',self.i5603009],
            '5605015':['TAMPA PONTEIRA PVC 80X40',self.i5605015],
            '7010006':['FITA INSUTAPE (ARREDONDAR DE 30 EM 30 M)',self.i7010006],
            '5603010':['SPRAY DE GALVANIZACAO A FRIO',self.i5603010],
            '5601201':['TUBO PAPELAO 4000 X 400 X 5',self.i5601201]
        }

    def get_codes(self):
        return[
            '5603112',
            '5603113',
            '5601003',
            '5601002',
            '5601001',
            '5601101',
            '5603111',
            '5603115',
            '5603001',
            '5603002',
            '5603110',
            '5603011',
            '1810101',
            '1000207',
            '1030002',
            '1020004',
            '1000209',
            '1030006',
            '1020007',
            '1000212',
            '1020009',
            '1000304',
            '1000102',
            '5601303',
            '5603009',
            '5605015',
            '7010006',
            '5603010',
            '5601201'
        ]

#if __name__ == "__main__":
#    obj = Structure(1048,300,1,False)
#    print(obj.get_bill())