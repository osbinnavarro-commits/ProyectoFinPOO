from datetime import date
from metodo_pago import MetodoPago

class PagoEfectivo(MetodoPago):
    def __init__(self, monto, cod_recibo, fecha: date = None, monto_recibido = None):
        super().__init__(monto, fecha)
        self.cod_recibo = cod_recibo
        self._monto_recibido = monto_recibido

    @property
    def cod_recibo(self):
        return self._cod_recibo

    @cod_recibo.setter
    def cod_recibo(self, valor):
        if valor <= 0:
            raise ValueError("El código de recibo debe ser positivo.")
        self._cod_recibo = int(valor)

    def _monto_redondeado(self):
        centavos = round(self._monto * 100)
        return round(((centavos // 50) * 50) / 100.0, 2)

    def cal_cambio(self, monto_recibido):
        total = self._monto_redondeado()
        if monto_recibido < total:
            raise ValueError("El monto recibido no cubre el total.")
        return round(monto_recibido - total, 2)

    def proc_pago(self):
        total = self._monto_redondeado()
        if self._monto_recibido is not None:
            self.cal_cambio(self._monto_recibido)
        self._monto = total
        return True