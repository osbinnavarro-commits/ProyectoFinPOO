from producto import Producto

class Plato(Producto):
    def __init__(self, nombre, precio, dia_venta: list):
        super().__init__(nombre, precio, es_combo = False)
        self.dia_venta = dia_venta

    @property
    def dia_venta(self):
        return list(self._dia_venta)

    @dia_venta.setter
    def dia_venta(self, valor: list) -> None:
        if not valor:
            raise ValueError("El plato debe tener al menos un día de venta.")
        self._dia_venta = [str(d).strip().lower() for d in valor]

    def cal_precio(self):
        return round(self._precio, 2)

    def esta_disp(self, dia):
        return dia.strip().lower() in self._dia_venta

    def contar_platos(self):
        return 1