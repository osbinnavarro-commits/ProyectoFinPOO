from abc import ABC, methodabstract  
class Producto(ABC):
    def __init__(self, nombre, precio, combo):
        self.nombre = nombre
        self.precio = precio
        self.combo = combo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = round(float(valor), 2)

    @abstractmethod 

    def cal_precio(self):
        pass 

    @abstractmethod 

    def esta_disp(self, dia):
        pass

    def combo(self):
        return self.combo


