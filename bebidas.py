from producto import Producto

class Bebidas(Producto):
    def __init__(self, nombre, precio, precio_tipo):
        super().__init__(nombre, precio, es_combo = False)
        self.precio_tipo = precio_tipo

    @property
    def precio_tipo(self):
        return self.precio_tipo

    @precio_tipo.setter
    def precio_tipo(self, valor):
        if valor != 1.0 and valor != 3.0:
            raise ValueError("El precio el vaso debe ser 1.0 y de la jarra debe ser 3.0")
        self._precio_tipo = float(valor)

    def cal_precio(self):
        return round(self._precio * self._precio_tipo, 2)

    def esta_disp(self, dia):
        return True
    
    def contar_platos(self):
        return 0

