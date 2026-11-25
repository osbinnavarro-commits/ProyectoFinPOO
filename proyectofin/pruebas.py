from datetime import date
from producto import Producto
from plato import Plato
from bebida import Bebida
from combo_producto import ComboProducto
from combo import Combo
from cliente import Cliente
from pedido import Pedido
from pedido_local import PedidoLocal
from pedido_llevar import PedidoLlevar
from pedido_delivery import PedidoDelivery
from metodo_pago import MetodoPago
from pago_efectivo import PagoEfectivo
from pago_qr import PagoQr
from pago_tarjeta import PagoTarjeta
from restaurante import Restaurante


def prueba_1_clases_abstractas():
    for clase, args in [
        (Producto, ("Test", 10.0)),
        (Pedido, (1,)),
        (MetodoPago, (10.0,)),
    ]:
        fallo = False
        try:
            clase(*args)
        except TypeError:
            fallo = True
        assert fallo, f"{clase.__name__} debe ser abstracta y lanzar TypeError"


def prueba_2_caso_referencia_variante_e():
    todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, todos)
    mocochinchi = Bebida("Mocochinchi", 6.0, 1.0)

    # Combo Valluno: (35 + 6) * 0.90 = Bs 36.90 (Variante E: 10% descuento)
    cp = ComboProducto([silpancho, mocochinchi])
    combo_valluno = Combo("Combo Valluno", cp)
    assert combo_valluno.cal_precio() == 36.90

    # 2 combos por delivery a Quillacollo (Bs 15): 73.80 + 15.00 = Bs 88.80
    pedido = PedidoDelivery(1, costo_envio=15.0, zona="quillacollo")
    pedido.agre_prod(combo_valluno, 2)
    assert pedido.cal_subtotal() == 73.80
    assert pedido.cal_recargo() == 15.0

    # Pago en efectivo Variante E: 88.80 redondeado hacia abajo a Bs 0,50 -> 88.50
    pago = PagoEfectivo(88.80, cod_recibo=101, monto_recibido=100.0)
    assert pago.cal_cambio(100.0) == 11.50
    comprobante = pedido.realizar_pago(pago)
    assert comprobante.monto == 88.50
    assert comprobante.fecha == date.today()


def prueba_3_combo_dentro_de_combo():
    todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, todos)
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    mocochinchi = Bebida("Mocochinchi", 6.0, 1.0)

    combo_valluno = Combo("Combo Valluno", ComboProducto([silpancho, mocochinchi]))
    combo_familiar = Combo("Combo Familiar", ComboProducto([combo_valluno, chicharron]))

    # (36.90 + 45.00) * 0.90 = 81.90 * 0.90 = Bs 73.71
    assert combo_familiar.cal_precio() == 73.71
    assert combo_familiar.esta_disp("domingo") is True
    assert combo_familiar.esta_disp("lunes") is False
    # 1 silpancho dentro del combo interno + 1 chicharrón = 2 platos (bebida = 0)
    assert combo_familiar.contar_plat() == 2


def prueba_4_envases_para_llevar_variante_e():
    todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, todos)
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    mocochinchi_vaso = Bebida("Mocochinchi Vaso", 6.0, 1.0)
    mocochinchi_jarra = Bebida("Mocochinchi Jarra", 6.0, 3.0)

    assert mocochinchi_jarra.cal_precio() == 18.0
    assert mocochinchi_jarra.precio_tipo == 3.0

    combo_valluno = Combo("Combo Valluno", ComboProducto([silpancho, mocochinchi_vaso]))
    combo_familiar = Combo("Combo Familiar", ComboProducto([combo_valluno, chicharron]))

    # Variante E: Bs 3 por plato, bebidas sin cargo (incluidos platos dentro de combos)
    pedido = PedidoLlevar(2)
    pedido.agre_prod(combo_familiar, 1)      # 2 platos
    pedido.agre_prod(mocochinchi_jarra, 1)   # 0 platos
    assert pedido.cal_subtotal() == 91.71
    assert pedido.cal_recargo() == 6.0       # 2 * Bs 3.00


def prueba_5_delivery_minimo_y_envio_gratis_variante_e():
    silpancho = Plato("Silpancho", 35.0, ["lunes"])

    # Pedido mínimo delivery Variante E: Bs 45
    p_bajo = PedidoDelivery(3, costo_envio=8.0, zona="cercado")
    p_bajo.agre_prod(silpancho, 1)  # Bs 35 < Bs 45
    fallo_min = False
    try:
        p_bajo.cal_recargo()
    except ValueError:
        fallo_min = True
    assert fallo_min, "Debe rechazar delivery menor a Bs 45"

    # Envío gratis desde Bs 180 solo Cercado
    p_cercado = PedidoDelivery(4, costo_envio=8.0, zona="cercado")
    p_cercado.agre_prod(silpancho, 6)  # Bs 210 >= Bs 180
    assert p_cercado.cal_recargo() == 0.0

    # En Quillacollo NO es gratis aunque pase de Bs 180
    p_quillacollo = PedidoDelivery(5, costo_envio=15.0, zona="quillacollo")
    p_quillacollo.agre_prod(silpancho, 6)
    assert p_quillacollo.cal_recargo() == 15.0

    # Otra zona de Bs 8 distinta de Cercado tampoco es gratis (valida por _zona)
    p_otra = PedidoDelivery(50, costo_envio=8.0, zona="colcapirhua")
    p_otra.agre_prod(silpancho, 6)
    assert p_otra.cal_recargo() == 8.0


def prueba_6_encapsulacion_validaciones_y_estados():
    # Teléfono inválido (no empieza en 6 o 7)
    fallo_tel = False
    try:
        Cliente("Ana", "111", "51234567")
    except ValueError:
        fallo_tel = True
    assert fallo_tel

    # Precio <= 0 inválido
    fallo_precio = False
    try:
        Plato("Test", 0, ["lunes"])
    except ValueError:
        fallo_precio = True
    assert fallo_precio

    # Cantidad fuera de 1..20 y modificación fuera de REGISTRADO
    silpancho = Plato("Silpancho", 35.0, ["lunes"])
    p = PedidoLlevar(6)
    fallo_cant = False
    try:
        p.agre_prod(silpancho, 25)
    except ValueError:
        fallo_cant = True
    assert fallo_cant

    p.agre_prod(silpancho, 1)

    # Lista interna blindada (modificar la copia no altera el pedido)
    copia = p.productos_pedido
    copia.clear()
    assert len(p.productos_pedido) == 1

    p.cambiar_estado("EN_PREPARACION")

    fallo_estado = False
    try:
        p.agre_prod(silpancho, 1)
    except ValueError:
        fallo_estado = True
    assert fallo_estado

    fallo_cancelar = False
    try:
        p.cambiar_estado("CANCELADO")
    except ValueError:
        fallo_cancelar = True
    assert fallo_cancelar


def prueba_7_pedido_local_y_mesas():
    p1 = PedidoLocal(7, mesa=5)
    assert p1.cal_recargo() == 0.0

    # No se permiten dos pedidos abiertos en la misma mesa
    fallo_mesa = False
    try:
        PedidoLocal(8, mesa=5)
    except ValueError:
        fallo_mesa = True
    assert fallo_mesa

    # Al finalizar el pedido, la mesa 5 se libera
    p1.cambiar_estado("EN_PREPARACION")
    p1.cambiar_estado("LISTO")
    p1.cambiar_estado("ENTREGADO")

    p2 = PedidoLocal(9, mesa=5)
    assert p2.mesa == 5
    p2.cambiar_estado("CANCELADO")


def prueba_8_pagos_qr_tarjeta_y_restriccion_delivery():
    # QR inválido (menos de 10 dígitos)
    fallo_qr = False
    try:
        PagoQr(50.0, "12345")
    except ValueError:
        fallo_qr = True
    assert fallo_qr

    pago_qr = PagoQr(50.0, "1234567890")
    assert pago_qr.procesar_pago() is True

    # Tarjeta aplica 3% de comisión
    pago_tarj = PagoTarjeta(100.0)
    assert pago_tarj.procesar_pago() is True
    assert pago_tarj.monto == 103.0

    # Delivery rechaza pago con tarjeta
    silpancho = Plato("Silpancho", 35.0, ["lunes"])
    p_del = PedidoDelivery(10, costo_envio=15.0, zona="quillacollo")
    p_del.agre_prod(silpancho, 2)
    fallo_tarj = False
    try:
        p_del.realizar_pago(PagoTarjeta(85.0))
    except ValueError:
        fallo_tarj = True
    assert fallo_tarj


def prueba_9_restaurante_y_reportes():
    rest = Restaurante("Sabor Valluno")
    silpancho = Plato("Silpancho", 35.0, ["lunes", "domingo"])
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    rest.reg_productos(silpancho)
    rest.reg_productos(chicharron)

    assert len(rest.listar_menu_dia("lunes")) == 1
    assert len(rest.listar_menu_dia("domingo")) == 2

    cliente = Cliente("Carlos", "7654321", "67654321", "Av. Blanco Galindo")
    rest.reg_cliente(cliente)
    pedido = rest.crear_pedido_llevar(cliente)
    pedido.agre_prod(silpancho, 2)  # 70 + 6 = 76
    pago = PagoQr(76.0, "0987654321")
    pedido.realizar_pago(pago)
    rest.reg_met_pago(pago)

    rep = rest.reporte_ventas()
    assert rep["ventas_por_tipo"]["PedidoLlevar"] == 76.0
    assert rep["top_3_productos"][0] == ("Silpancho", 2)
    assert len(cliente.historial()) == 1


def prueba_10_retraso_delivery_regla_9():
    silpancho = Plato("Silpancho", 35.0, ["lunes"])
    p = PedidoDelivery(11, costo_envio=15.0, zona="quillacollo")
    p.agre_prod(silpancho, 2)  # Bs 70 >= Bs 45

    # Entrega en 45 min: sin retraso -> cobra Bs 15
    p.registrar_tiempo_entrega(45)
    assert p.tiene_retraso() is False
    assert p.cal_recargo() == 15.0

    # Entrega en 65 min (> 60 min): con retraso -> devolución del envío (Bs 0)
    p.registrar_tiempo_entrega(65)
    assert p.tiene_retraso() is True
    assert p.cal_recargo() == 0.0


if __name__ == "__main__":
    prueba_1_clases_abstractas()
    prueba_2_caso_referencia_variante_e()
    prueba_3_combo_dentro_de_combo()
    prueba_4_envases_para_llevar_variante_e()
    prueba_5_delivery_minimo_y_envio_gratis_variante_e()
    prueba_6_encapsulacion_validaciones_y_estados()
    prueba_7_pedido_local_y_mesas()
    prueba_8_pagos_qr_tarjeta_y_restriccion_delivery()
    prueba_9_restaurante_y_reportes()
    prueba_10_retraso_delivery_regla_9()
    print("OK: Las 10 pruebas de la Variante E (incluyendo _zona y Regla 9) pasaron correctamente.")