from abc import ABC, abstractmethod

class Producto(ABC):
    def __init__(self, nombre, precio, es_combo = False):
        self.nombre = nombre
        self.precio = precio
        self._combo = es_combo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El producto debe tener un nombre")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero")
        self._precio = round(float(valor), 2)

    @abstractmethod 

    def cal_precio(self):
        pass 

    @abstractmethod 

    def esta_disp(self, dia):
        pass

    def combo(self):
        return self.combo




