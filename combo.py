from producto import Producto
from combo_producto import ComboProducto

class Combo(Producto):
    def __init__(self, nombre, combo_producto: ComboProducto):
        self._combo_producto = combo_producto
        self._combo_producto._combo_dueno = self
        super().__init__(nombre, combo_producto.cal_precio(), es_combo = True)

    @property
    def combo_producto(self):
        return self._combo_producto

    def cal_precio(self):
        self._precio = self._combo_producto.cal_precio()
        return self._precio

    def esta_disp(self, dia):
        return self._combo_producto.esta_disp(dia)

    def contar_platos(self):
        return self._combo_producto.contar_platos()