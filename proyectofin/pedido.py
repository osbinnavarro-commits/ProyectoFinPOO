from abc import ABC, abstractmethod
from producto_pedido import ProductoPedido
from pago_pedido import PagoPedido


class Pedido(ABC):
    TRANSICIONES = {
        "REGISTRADO": ["EN_PREPARACION", "CANCELADO"],
        "EN_PREPARACION": ["LISTO"],
        "LISTO": ["ENTREGADO"],
        "ENTREGADO": [],
        "CANCELADO": [],
    }

    def __init__(self, id_pedido):
        self.id_pedido = id_pedido
        self._tipo_estado = ["REGISTRADO"]
        self._productos_pedido = []
        self._pagos_pedido = []

    @property
    def id_pedido(self):
        return self._id_pedido

    @id_pedido.setter
    def id_pedido(self, valor) -> None:
        if valor <= 0:
            raise ValueError("El id_pedido debe ser positivo.")
        self._id_pedido = int(valor)

    @property
    def tipo_estado(self):
        return list(self._tipo_estado)

    @property
    def estado_actual(self):
        return self._tipo_estado[-1]

    @property
    def productos_pedido(self):
        return list(self._productos_pedido)

    @property
    def pagos_pedido(self):
        return list(self._pagos_pedido)

    def agre_prod(self, producto, cantidad):
        if self.estado_actual != "REGISTRADO":
            raise ValueError("Solo se pueden agregar productos en REGISTRADO.")
        item = ProductoPedido(producto, cantidad, self, self.estado_actual)
        self._productos_pedido.append(item)
        return item

    def quit_prod(self, producto):
        if self.estado_actual != "REGISTRADO":
            raise ValueError("Solo se pueden quitar productos en REGISTRADO.")
        for i, item in enumerate(self._productos_pedido):
            if item.producto is producto:
                self._productos_pedido.pop(i)
                return
        raise ValueError("El producto no está en el pedido.")

    def cal_subtotal(self):
        subtotal = 0.0
        for item in self._productos_pedido:
            subtotal += item.producto.cal_precio() * item.cantidad
        return round(subtotal, 2)

    def cambiar_estado(self, nuevo_estado):
        estado = nuevo_estado.strip().upper()
        if estado not in self.TRANSICIONES:
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        if estado not in self.TRANSICIONES[self.estado_actual]:
            raise ValueError(f"No se puede pasar de {self.estado_actual} a {estado}.")
        self._tipo_estado.append(estado)
        for item in self._productos_pedido:
            item.estado = estado

    def realizar_pago(self, metodo_pago):
        total = round(self.cal_subtotal() + self.cal_recargo(), 2)
        metodo_pago.monto = total
        if not metodo_pago.procesar_pago():
            raise ValueError("No se pudo procesar el pago.")
        registro = PagoPedido(metodo_pago, self, metodo_pago.fecha, metodo_pago.monto)
        self._pagos_pedido.append(registro)
        return registro

    @abstractmethod
    def cal_recargo(self):
        pass