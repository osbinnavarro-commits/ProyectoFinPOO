import producto as Pr

class Plato(Pr):
    def __init__(self, nombre, precio, dia_venta):
        super().__init__(nombre, precio, "combo")
        self.dia_venta = dia_venta