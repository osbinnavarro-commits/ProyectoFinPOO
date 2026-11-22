from datetime import date
from metodo_pago import MetodoPago


class PagoTarjeta(MetodoPago):
    def __init__(self, monto, comision: float = 0.03, fecha: date = None):
        super().__init__(monto, fecha)
        self.comision = comision

    @property
    def comision(self):
        return self._comision

    @comision.setter
    def comision(self, valor):
        if valor < 0:
            raise ValueError("La comisión no puede ser negativa.")
        self._comision = float(valor)

    def proc_pago(self):
        self._monto = round(self._monto * (1.0 + self._comision), 2)
        return True

    def permitido_delivery(self):
        return False