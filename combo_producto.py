class ComboProducto:
    DESCUENTO_E = 0.10

    def __init__(self, producto, combo = DESCUENTO_E):
        self._combo_dueno = None
        self.combo = combo
        self.producto = producto

    @property
    def producto(self):
        return list(self._producto)

    @producto.setter
    def producto(self, lista_productos):
        if len(lista_productos) < 2:
            raise ValueError("Un combo debe contener al menos 2 productos.")
        for prod in lista_productos:
            if self._combo_dueno is not None and prod is self._combo_dueno:
                raise ValueError("Un combo no puede contenerse a sí mismo.")
        self._producto = list(lista_productos)

    @property
    def combo(self):
        return self._combo

    @combo.setter
    def combo(self, valor):
        if valor < 0 or valor >= 1:
            raise ValueError("El descuento debe estar entre 0 y 1")
        self._combo = float(valor)

    def cal_precio(self):
        suma = 0.0
        for prod in self._producto:
            suma += prod.cal_precio()
        return round(suma * (1.0 - self._combo), 2)

    def esta_disp(self, dia):
        for prod in self._producto:
            if not prod.esta_disp(dia):
                return False
        return True

    def contar_platos(self):
        total = 0
        for prod in self._producto:
            total += prod.contar_platos()
        return total