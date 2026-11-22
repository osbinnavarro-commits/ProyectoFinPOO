class ProductoPedido:
    def __init__(self, producto, cantidad, pedido, estado = "REGISTRADO", precio_unitario = None):
        self._producto = producto
        self.cantidad = cantidad
        self._pedido = pedido
        self._estado = estado
        self.precio_unitario = precio_unitario if precio_unitario is not None else producto.cal_precio()
        self._pago = round(self._precio_unitario * self._cantidad, 2)

    @property
    def pago(self):
        self._pago = round(self._precio_unitario * self._cantidad, 2)
        return self._pago

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 1 or valor > 20:
            raise ValueError("La cantidad debe estar entre 1 y 20.")
        self._cantidad = int(valor)

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    @property
    def producto(self):
        return self._producto

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor):
        if valor <= 0:
            raise ValueError("El precio unitario debe ser mayor que cero.")
        self._precio_unitario = round(float(valor), 2)

    @property
    def pedido(self):
        return self._pedido