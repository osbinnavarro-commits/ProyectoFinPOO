from pedido import Pedido

class PedidoLocal(Pedido):
    _mesas_ocupadas = set()

    def __init__(self, id_pedido, mesa):
        super().__init__(id_pedido)
        self.mesa = mesa
        PedidoLocal._mesas_ocupadas.add(self._mesa)

    @property
    def mesa(self):
        return self._mesa

    @mesa.setter
    def mesa(self, valor):
        if valor < 1 or valor > 15:
            raise ValueError("La mesa debe estar entre 1 y 15.")
        if valor in PedidoLocal._mesas_ocupadas:
            raise ValueError(f"La mesa {valor} ya tiene un pedido abierto.")
        self._mesa = int(valor)

    def cambiar_estado(self, nuevo_estado):
        super().cambiar_estado(nuevo_estado)
        if self.estado_actual in ("ENTREGADO", "CANCELADO"):
            PedidoLocal._mesas_ocupadas.discard(self._mesa)

    def cal_recargo(self):
        return 0.0