from datetime import date

class PagoPedido:
    def __init__(self, tipo_pago, pedido, fecha: date, monto: float):
        self._tipo_pago = tipo_pago
        self._pedido = pedido
        self._fecha = fecha
        self.monto = monto

    @property
    def tipo_pago(self):
        return self._tipo_pago

    @property
    def pedido(self):
        return self._pedido

    @property
    def fecha(self):
        return self._fecha

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if valor <= 0:
            raise ValueError("El monto del pago debe ser mayor que cero.")
        self._monto = round(float(valor), 2)