from pedido import Pedido

class PedidoDelivery(Pedido):
    PEDIDO_MINIMO_VARIANTE_E = 45.0
    ENVIO_GRATIS_CERCADO = 180.0
    COSTO_CERCADO = 8.0
    MINUTO_LIMITE_RETRASO = 60

    def __init__(self, id_pedido, costo_envio = COSTO_CERCADO, zona = "cercado"):
        super().__init__(id_pedido)
        self.costo_envio = costo_envio
        self.zona = zona
        self._minutos_entrega = 0

    @property
    def costo_envio(self):
        return self._costo_envio

    @costo_envio.setter
    def costo_envio(self, valor):
        if valor <= 0:
            raise ValueError("El costo de envío debe ser mayor que cero.")
        self._costo_envio = round(float(valor), 2)

    @property
    def zona(self):
        return self._zona

    @zona.setter
    def zona(self, valor):
        z = str(valor).strip().lower()
        if not z:
            raise ValueError("La zona de delivery no puede estar vacia")
        self._zona = z
    
    @property
    def minutos_entrega(self):
        return self._minutos_entrega

    def registrar_tiempo_entrega(self, minutos):
        if minutos < 0:
            raise ValueError("Los minutos de entrega no pueden ser negativos.")
        self._minutos_entrega = int(minutos)

    def tiene_retraso(self):
        return self._minutos_entrega > self.MINUTO_LIMITE_RETRASO

    def cal_recargo(self):
        subtotal = self.cal_subtotal()
        if subtotal < self.PEDIDO_MINIMO_VARIANTE_E:
            raise ValueError("El pedido mínimo para delivery es Bs 45.00.")
        if self.tiene_retraso():
            return 0.0
        if self._zona == "cercado" and subtotal >= self.ENVIO_GRATIS_CERCADO:
            return 0.0
        return round(self._costo_envio, 2)

    def realizar_pago(self, metodo_pago):
        if not metodo_pago.permitido_delivery():
            raise ValueError("El delivery solo acepta pago en efectivo o QR.")
        return super().realizar_pago(metodo_pago)