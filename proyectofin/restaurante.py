from combo_producto import ComboProducto
from combo import Combo
from pedido_local import PedidoLocal
from pedido_llevar import PedidoLlevar
from pedido_delivery import PedidoDelivery


class Restaurante:
    ZONAS_DELIVERY = {
        "cercado": 8.0,
        "quillacollo": 15.0,
        "sacaba": 15.0,
        "vinto": 20.0,
    }

    def __init__(self, nombre: str = "Sabor Valluno"):
        self._nombre = nombre
        self._list_pedido = []
        self._list_producto = []
        self._list_combos = []
        self._list_met_pago = []
        self._list_cliente = []
        self._siguiente_id = 1

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def list_pedido(self) -> list:
        return list(self._list_pedido)

    @property
    def list_producto(self) -> list:
        return list(self._list_producto)

    @property
    def list_combos(self) -> list:
        return list(self._list_combos)

    @property
    def list_met_pago(self) -> list:
        return list(self._list_met_pago)

    @property
    def list_cliente(self) -> list:
        return list(self._list_cliente)

    # --- Métodos principales de tu diagrama v2 ---
    def reg_productos(self, producto) -> None:
        self._list_producto.append(producto)
        if producto.combo():
            self._list_combos.append(producto)

    def reg_pedido(self, pedido, cliente=None) -> None:
        self._list_pedido.append(pedido)
        if cliente is not None:
            cliente.realizar_pedido(pedido)

    def reg_cliente(self, cliente) -> None:
        if self.buscar_cliente(cliente.ci_cliente) is not None:
            raise ValueError(f"Ya existe un cliente con CI {cliente.ci_cliente}.")
        self._list_cliente.append(cliente)

    def reg_met_pago(self, metodo_pago) -> None:
        self._list_met_pago.append(metodo_pago)

    # --- Métodos auxiliares para combos, menú, pedidos y reportes ---
    def crear_combo(self, nombre: str, productos: list) -> Combo:
        cp = ComboProducto(productos)
        combo = Combo(nombre, cp)
        self.reg_productos(combo)
        return combo

    def listar_menu_dia(self, dia: str) -> list:
        disponibles = []
        for prod in self._list_producto:
            if prod.esta_disp(dia):
                disponibles.append(prod)
        return disponibles

    def buscar_cliente(self, ci_cliente: str):
        ci = str(ci_cliente).strip()
        for cliente in self._list_cliente:
            if str(cliente.ci_cliente) == ci:
                return cliente
        return None

    def _generar_id(self) -> int:
        id_actual = self._siguiente_id
        self._siguiente_id += 1
        return id_actual

    def crear_pedido_local(self, cliente, mesa: int) -> PedidoLocal:
        pedido = PedidoLocal(self._generar_id(), mesa)
        self.reg_pedido(pedido, cliente)
        return pedido

    def crear_pedido_llevar(self, cliente) -> PedidoLlevar:
        pedido = PedidoLlevar(self._generar_id())
        self.reg_pedido(pedido, cliente)
        return pedido

    def crear_pedido_delivery(self, cliente, zona: str) -> PedidoDelivery:
        zona_norm = zona.strip().lower()
        if zona_norm not in self.ZONAS_DELIVERY:
            raise ValueError(f"Zona no válida. Permitidas: {list(self.ZONAS_DELIVERY.keys())}")
        pedido = PedidoDelivery(
            self._generar_id(),
            costo_envio=self.ZONAS_DELIVERY[zona_norm],
            zona=zona_norm,
        )
        self.reg_pedido(pedido, cliente)
        return pedido

    def buscar_pedido(self, id_pedido: int):
        for pedido in self._list_pedido:
            if pedido.id_pedido == id_pedido:
                return pedido
        return None

    def detalle_pedido(self, pedido) -> dict:
        subtotal = pedido.cal_subtotal()
        recargo = pedido.cal_recargo()
        total = round(subtotal + recargo, 2)
        return {
            "id_pedido": pedido.id_pedido,
            "tipo": pedido.__class__.__name__,
            "estado": pedido.estado_actual,
            "subtotal": subtotal,
            "recargo": recargo,
            "total": total,
        }

    def reporte_ventas(self) -> dict:
        ventas_por_tipo = {
            "PedidoLocal": 0.0,
            "PedidoLlevar": 0.0,
            "PedidoDelivery": 0.0,
        }
        conteo_productos = {}

        for pedido in self._list_pedido:
            if pedido.estado_actual == "CANCELADO":
                continue

            tipo = pedido.__class__.__name__
            if pedido.pagos_pedido:
                monto = 0.0
                for pago in pedido.pagos_pedido:
                    monto += pago.monto
            else:
                monto = round(pedido.cal_subtotal() + pedido.cal_recargo(), 2)

            ventas_por_tipo[tipo] = round(ventas_por_tipo.get(tipo, 0.0) + monto, 2)

            for item in pedido.productos_pedido:
                nombre_prod = item.producto.nombre
                conteo_productos[nombre_prod] = conteo_productos.get(nombre_prod, 0) + item.cantidad

        ordenados = sorted(conteo_productos.items(), key=lambda x: x[1], reverse=True)
        return {
            "ventas_por_tipo": ventas_por_tipo,
            "top_3_productos": ordenados[:3],
        }