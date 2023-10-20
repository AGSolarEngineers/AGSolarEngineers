class Module():
    def __init__(self, length, height, power, voltage_operating, current_operating, voltage_open_circuit, current_short_circuit):
        self._length = length
        self._height = height
        self._power = power
        self._voltage_operating = voltage_operating
        self._current_operating = current_operating
        self._voltage_open_circuit = voltage_open_circuit
        self._current_short_circuit = current_short_circuit

    # region Getter and Setter 

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        self._length = value

    @length.deleter
    def length(self):
        del self._length
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    @height.deleter
    def height(self):
        del self._height
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
    def voltage_operating(self):
        return self._voltage_operating
    
    @voltage_operating.setter
    def voltage_operating(self, value):
        self._voltage_operating = value

    @voltage_operating.deleter
    def voltage_operating(self):
        del self._voltage_operating
    @property
    def current_operating(self):
        return self._current_operating
    
    @current_operating.setter
    def current_operating(self, value):
        self._current_operating = value

    @current_operating.deleter
    def current_operating(self):
        del self._current_operating
    @property
    def voltage_open_circuit(self):
        return self._voltage_open_circuit
    
    @voltage_open_circuit.setter
    def voltage_open_circuit(self, value):
        self._voltage_open_circuit = value

    @voltage_open_circuit.deleter
    def voltage_open_circuit(self):
        del self._voltage_open_circuit
    @property
    def current_short_circuit(self):
        return self._current_short_circuit
    
    @current_short_circuit.setter
    def current_short_circuit(self, value):
        self._current_short_circuit = value

    @current_short_circuit.deleter
    def current_short_circuit(self):
        del self._current_short_circuit

    # endregion
