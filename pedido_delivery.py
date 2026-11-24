from datetime import datetime
from pedido import Pedido


class PedidoDelivery(Pedido):
    PEDIDO_MINIMO_VARIANTE_E = 45.0
    ENVIO_GRATIS_CERCADO = 180.0
    COSTO_CERCADO = 8.0
    MIN_RETRASO = 60

    def __init__(self, id_pedido, costo_envio=COSTO_CERCADO, zona="Cercado", hora_registro=None):
        super().__init__(id_pedido)
        self.costo_envio = costo_envio
        self.zona = zona
        self._hora_registro = hora_registro if hora_registro is not None else datetime.now()
        self._hora_entrega = None
        self._compensacion_retraso = 0.0

    @property
    def costo_envio(self):
        return self._costo_envio

    @costo_envio.setter
    def costo_envio(self, valor):
        if valor <= 0:
            raise ValueError("El costo de envío debe ser mayor que cero")
        self._costo_envio = round(float(valor), 2)

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La zona de delivery no puede estar vacía.")
        self._zona = valor.strip()

    @property
    def hora_registro(self):
        return self._hora_registro

    @property
    def compensacion_retraso(self):
        return self._compensacion_retraso

    def cal_recargo(self):
        subtotal = self.cal_subtotal()
        if subtotal < self.PEDIDO_MINIMO_VARIANTE_E:
            raise ValueError("El pedido mínimo para delivery es Bs 45.00.")
        if self._costo_envio == self.COSTO_CERCADO and subtotal >= self.ENVIO_GRATIS_CERCADO:
            return 0.0
        return round(self._costo_envio, 2)

    def cambiar_estado(self, nuevo_estado, hora_entrega=None):
        super().cambiar_estado(nuevo_estado)
        if self.estado_actual == "ENTREGADO":
            self._hora_entrega = hora_entrega if hora_entrega is not None else datetime.now()
            minutos = (self._hora_entrega - self._hora_registro).total_seconds() / 60
            if minutos > self.MINUTOS_RETRASO:
                self._compensacion_retraso = self.cal_recargo()
            else:
                self._compensacion_retraso = 0.0

    def realizar_pago(self, metodo_pago):
        if not metodo_pago.permitido_delivery():
            raise ValueError("El delivery solo acepta pago en efectivo o QR.")
        return super().realizar_pago(metodo_pago)