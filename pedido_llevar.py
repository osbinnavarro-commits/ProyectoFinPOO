from pedido import Pedido


class PedidoLlevar(Pedido):
    COSTO_E = 3.0

    def __init__(self, id_pedido, costo_envase = COSTO_E):
        super().__init__(id_pedido)
        self.costo_envase = costo_envase

    @property
    def costo_envase(self):
        return self._costo_envase

    @costo_envase.setter
    def costo_envase(self, valor):
        if valor < 0:
            raise ValueError("El costo de envase no puede ser negativo.")
        self._costo_envase = round(float(valor), 2)

    def cal_recargo(self):
        total_platos = 0
        for item in self._productos_pedido:
            total_platos += item.producto.contar_plat() * item.cantidad
        return round(total_platos * self._costo_envase, 2)