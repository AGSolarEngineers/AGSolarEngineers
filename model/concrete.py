import math


class Concreto():
    def __init__(self, base_amount: int, height_buried: float, ray_buried: float, height_exposed: float, ray_exposed: float, feature: str):
        self._base_amount = base_amount
        self._height_buried = height_buried
        self._ray_buried = ray_buried
        self._height_exposed = height_exposed
        self._ray_exposed = ray_exposed
        self._feature = feature
        self._volume_buried = 0
        self._volume_exposed = 0
        self._volume_per_base = 0
        self._volume_total = 0
        self.calculate_volume()

    #region Getters & Setters

    @property
    def base_amount(self):
        return self._base_amount
    
    @base_amount.setter
    def base_amount(self, value):
        self._base_amount = value

    @base_amount.deleter
    def base_amount(self):
        del self._base_amount

    @property
    def height_buried(self):
        return self._height_buried
    
    @height_buried.setter
    def height_buried(self, value):
        self._height_buried = value

    @height_buried.deleter
    def height_buried(self):
        del self._height_buried

    @property
    def ray_buried(self):
        return self._ray_buried
    
    @ray_buried.setter
    def ray_buried(self, value):
        self._ray_buried = value

    @ray_buried.deleter
    def ray_buried(self):
        del self._ray_buried

    @property
    def height_exposed(self):
        return self._height_exposed
    
    @height_exposed.setter
    def height_exposed(self, value):
        self._height_exposed = value

    @height_exposed.deleter
    def height_exposed(self):
        del self._height_exposed

    @property
    def ray_exposed(self):
        return self._ray_exposed
    
    @ray_exposed.setter
    def ray_exposed(self, value):
        self._ray_exposed = value

    @ray_exposed.deleter
    def ray_exposed(self):
        del self._ray_exposed

    @property
    def feature(self):
        return self._feature
    
    @feature.setter
    def feature(self, value):
        self._feature = value

    @feature.deleter
    def feature(self):
        del self._feature

    @property
    def volume_buried(self):
        return self._volume_buried
    
    @volume_buried.setter
    def volume_buried(self, value):
        self._volume_buried = value

    @volume_buried.deleter
    def volume_buried(self):
        del self._volume_buried
    
    @property
    def volume_exposed(self):
        return self._volume_exposed
    
    @volume_exposed.setter
    def volume_exposed(self, value):
        self._volume_exposed = value

    @volume_exposed.deleter
    def volume_exposed(self):
        del self._volume_exposed
    
    @property
    def volume_per_base(self):
        return self._volume_per_base
    
    @volume_per_base.setter
    def volume_per_base(self, value):
        self._volume_per_base = value

    @volume_per_base.deleter
    def volume_per_base(self):
        del self._volume_per_base

    @property
    def volume_total(self):
        return self._volume_total
    
    @volume_total.setter
    def volume_total(self, value):
        self._volume_total = value

    @volume_total.deleter
    def volume_total(self):
        del self._volume_total

    #endregion

    def calculate_volume(self):
        self.volume_buried = math.pi*(self.ray_buried**2)*self.height_buried
        self.volume_exposed = math.pi*(self.ray_exposed**2)*self.height_exposed
        self.volume_per_base = self.volume_buried+self.volume_exposed
        self.volume_total = math.ceil(self.volume_per_base*self.base_amount*1.1)


if __name__ == '__main__':
    concreto = Concreto(474, 1.6, 0.15, 0.4, 0.2, 'H21')
    print(concreto.volume_total)