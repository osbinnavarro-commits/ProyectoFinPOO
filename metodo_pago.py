from abc import ABC, abstractmethod
from datetime import date


class MetodoPago(ABC):
    def __init__(self, monto, fecha: date = None):
        self.monto = monto
        self.fecha = fecha if fecha is not None else date.today()

    @property
    def monto(self):
        return self._monto

    @monto.setter
    def monto(self, valor):
        if valor <= 0:
            raise ValueError("El monto debe ser mayor que cero.")
        self._monto = round(float(valor), 2)

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    def procesar_pago(self):
        return self.proc_pago()

    @abstractmethod
    def proc_pago(self):
        pass

    def permitido_delivery(self):
        return True