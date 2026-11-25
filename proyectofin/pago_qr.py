from datetime import date
from metodo_pago import MetodoPago

class PagoQr(MetodoPago):
    def __init__(self, monto, cal_trans, fecha: date = None):
        super().__init__(monto, fecha)
        self.cal_trans = cal_trans

    @property
    def cal_trans(self):
        return self._cal_trans

    @cal_trans.setter
    def cal_trans(self, valor):
        codigo = str(valor).strip()
        if len(codigo) != 10 or not codigo.isdigit():
            raise ValueError("El código de transacción QR debe tener 10 dígitos.")
        self._cal_trans = codigo

    def proc_pago(self):
        return len(self._cal_trans) == 10 and self._monto > 0