from restaurante import Restaurante
from plato import Plato
from bebida import Bebida
from cliente import Cliente
from pago_efectivo import PagoEfectivo
from pago_qr import PagoQr
from pago_tarjeta import PagoTarjeta


def cargar_datos_iniciales(rest: Restaurante) -> None:
    todos = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    silpancho = Plato("Silpancho", 35.0, todos)
    pique = Plato("Pique Macho", 48.0, todos)
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    sopa_mani = Plato("Sopa de Maní", 18.0, todos)
    mocochinchi_vaso = Bebida("Mocochinchi (Vaso)", 6.0, 1.0)
    mocochinchi_jarra = Bebida("Mocochinchi (Jarra)", 6.0, 3.0)

    for prod in [silpancho, pique, chicharron, sopa_mani, mocochinchi_vaso, mocochinchi_jarra]:
        rest.reg_productos(prod)

    rest.crear_combo("Combo Valluno", [silpancho, mocochinchi_vaso])


def mostrar_menu_productos(lista: list) -> None:
    if not lista:
        print("No hay productos disponibles.")
        return
    for i, prod in enumerate(lista, start=1):
        etiqueta = "Combo" if prod.combo() else "Producto"
        print(f"  {i}. {prod.nombre} ({etiqueta}) - Bs {prod.cal_precio():.2f}")


def opcion_registrar_producto(rest: Restaurante) -> None:
    print("\n1. Plato  2. Bebida  3. Combo")
    tipo = input("Tipo: ").strip()

    if tipo == "1":
        nombre = input("Nombre del plato: ")
        precio = float(input("Precio (Bs): "))
        dias_txt = input("Días de venta separados por coma (ej. lunes,martes o domingo): ")
        dias = []
        for d in dias_txt.split(","):
            if d.strip():
                dias.append(d.strip())
        rest.reg_productos(Plato(nombre, precio, dias))
        print("Plato registrado.")

    elif tipo == "2":
        nombre = input("Nombre de la bebida: ")
        precio = float(input("Precio por vaso (Bs): "))
        pres = float(input("Presentación (1 = Vaso, 3 = Jarra): ").strip())
        rest.reg_productos(Bebida(nombre, precio, pres))
        print("Bebida registrada.")

    elif tipo == "3":
        mostrar_menu_productos(rest.list_producto)
        nombre = input("Nombre del combo: ")
        indices_txt = input("Números de productos separados por coma (mínimo 2): ")
        seleccionados = []
        for idx in indices_txt.split(","):
            num = int(idx.strip()) - 1
            seleccionados.append(rest.list_producto[num])
        combo = rest.crear_combo(nombre, seleccionados)
        print(f"Combo '{combo.nombre}' creado a Bs {combo.cal_precio():.2f} (10% desc.).")

    else:
        print("Opción no válida.")


def opcion_listar_menu_dia(rest: Restaurante) -> None:
    dia = input("\nDía de la semana (ej. lunes, domingo): ").strip()
    print(f"\n--- Menú disponible ({dia}) ---")
    mostrar_menu_productos(rest.listar_menu_dia(dia))


def opcion_registrar_cliente(rest: Restaurante) -> None:
    nombre = input("\nNombre completo: ")
    ci = input("CI: ")
    telefono = input("Teléfono (8 dígitos, empieza en 6 o 7): ")
    direccion = input("Dirección (opcional): ")
    cliente = Cliente(nombre, ci, telefono, direccion)
    rest.reg_cliente(cliente)
    print(f"Cliente '{cliente.nombre}' registrado.")


def opcion_crear_pedido(rest: Restaurante) -> None:
    ci = input("\nCI del cliente: ")
    cliente = rest.buscar_cliente(ci)
    if cliente is None:
        print("Cliente no encontrado. Regístralo primero.")
        return

    print("Tipo de pedido: 1. Local  2. Para llevar  3. Delivery")
    tipo = input("Opción: ").strip()

    if tipo == "1":
        mesa = int(input("Número de mesa (1 a 15): "))
        pedido = rest.crear_pedido_local(cliente, mesa)
    elif tipo == "2":
        pedido = rest.crear_pedido_llevar(cliente)
    elif tipo == "3":
        print("Zonas: cercado (Bs 8), quillacollo (Bs 15), sacaba (Bs 15), vinto (Bs 20)")
        zona = input("Zona de entrega: ")
        pedido = rest.crear_pedido_delivery(cliente, zona)
    else:
        print("Tipo inválido.")
        return

    print(f"Pedido #{pedido.id_pedido} creado en estado {pedido.estado_actual}.")
    gestionar_items_pedido(rest, pedido)


def gestionar_items_pedido(rest: Restaurante, pedido) -> None:
    while True:
        print("\n1. Agregar producto  2. Quitar producto  3. Terminar")
        op = input("Opción: ").strip()
        if op == "1":
            mostrar_menu_productos(rest.list_producto)
            num = int(input("Número de producto: ")) - 1
            cant = int(input("Cantidad (1 a 20): "))
            pedido.agre_prod(rest.list_producto[num], cant)
            print("Producto agregado.")
        elif op == "2":
            if not pedido.productos_pedido:
                print("El pedido no tiene productos.")
                continue
            for i, item in enumerate(pedido.productos_pedido, start=1):
                print(f"  {i}. {item.producto.nombre} x{item.cantidad}")
            num = int(input("Número a quitar: ")) - 1
            pedido.quit_prod(pedido.productos_pedido[num].producto)
            print("Producto quitado.")
        elif op == "3":
            break
        else:
            print("Opción no válida.")


def opcion_ver_detalle(rest: Restaurante) -> None:
    id_ped = int(input("\nID del pedido: "))
    pedido = rest.buscar_pedido(id_ped)
    if pedido is None:
        print("Pedido no encontrado.")
        return

    print(f"\n--- Pedido #{pedido.id_pedido} ({pedido.__class__.__name__}) ---")
    print(f"Estado actual: {pedido.estado_actual}")
    print(f"Historial de estados: {pedido.tipo_estado}")
    for item in pedido.productos_pedido:
        print(f"  - {item.producto.nombre} x{item.cantidad} (Bs {item.precio_unitario:.2f} c/u) = Bs {item.pago:.2f}")

    info = rest.detalle_pedido(pedido)
    print(f"Subtotal: Bs {info['subtotal']:.2f}")
    print(f"Recargo (envases/envío): Bs {info['recargo']:.2f}")
    print(f"Total: Bs {info['total']:.2f}")


def opcion_cambiar_estado(rest: Restaurante) -> None:
    id_ped = int(input("\nID del pedido: "))
    pedido = rest.buscar_pedido(id_ped)
    if pedido is None:
        print("Pedido no encontrado.")
        return
    print(f"Estado actual: {pedido.estado_actual}")
    nuevo = input("Nuevo estado (EN_PREPARACION, LISTO, ENTREGADO, CANCELADO): ")
    pedido.cambiar_estado(nuevo)
    print(f"Estado actualizado a {pedido.estado_actual}.")


def opcion_registrar_tiempo_delivery(rest: Restaurante) -> None:
    id_ped = int(input("\nID del pedido de delivery: "))
    pedido = rest.buscar_pedido(id_ped)
    if pedido is None:
        print("Pedido no encontrado.")
        return
    if not hasattr(pedido, "registrar_tiempo_entrega"):
        print("Este pedido no es de delivery.")
        return
    minutos = int(input("Minutos transcurridos hasta la entrega: "))
    pedido.registrar_tiempo_entrega(minutos)
    if pedido.tiene_retraso():
        print("Retraso detectado (> 60 min): se aplica devolución del costo de envío (Bs 0.00).")
    else:
        print("Entrega dentro de tiempo (<= 60 min): tarifa normal de envío.")


def opcion_cobrar_pedido(rest: Restaurante) -> None:
    id_ped = int(input("\nID del pedido a cobrar: "))
    pedido = rest.buscar_pedido(id_ped)
    if pedido is None:
        print("Pedido no encontrado.")
        return

    info = rest.detalle_pedido(pedido)
    total = info["total"]
    print(f"Total a pagar: Bs {total:.2f}")
    print("Método de pago: 1. Efectivo  2. QR  3. Tarjeta")
    op = input("Opción: ").strip()

    if op == "1":
        cod = int(input("Código de recibo (entero positivo): "))
        recibido = float(input("Monto recibido (Bs): "))
        metodo = PagoEfectivo(total, cod_recibo=cod, monto_recibido=recibido)
        cambio = metodo.cal_cambio(recibido)
        comprobante = pedido.realizar_pago(metodo)
        rest.reg_met_pago(metodo)
        print("\n--- COMPROBANTE (EFECTIVO) ---")
        print(f"Pedido #{pedido.id_pedido} | Recibo #{metodo.cod_recibo} | Fecha: {comprobante.fecha}")
        print(f"Total cobrado (redondeo Variante E): Bs {comprobante.monto:.2f}")
        print(f"Cambio: Bs {cambio:.2f}")

    elif op == "2":
        codigo_qr = input("Código de transacción QR (10 dígitos): ")
        metodo = PagoQr(total, cal_trans=codigo_qr)
        comprobante = pedido.realizar_pago(metodo)
        rest.reg_met_pago(metodo)
        print("\n--- COMPROBANTE (QR) ---")
        print(f"Pedido #{pedido.id_pedido} | Transacción: {codigo_qr} | Fecha: {comprobante.fecha}")
        print(f"Total cobrado: Bs {comprobante.monto:.2f}")

    elif op == "3":
        metodo = PagoTarjeta(total)
        comprobante = pedido.realizar_pago(metodo)
        rest.reg_met_pago(metodo)
        print("\n--- COMPROBANTE (TARJETA) ---")
        print(f"Pedido #{pedido.id_pedido} | Comisión 3% incluida | Fecha: {comprobante.fecha}")
        print(f"Total cobrado: Bs {comprobante.monto:.2f}")

    else:
        print("Opción no válida.")


def opcion_reporte_ventas(rest: Restaurante) -> None:
    rep = rest.reporte_ventas()
    print("\n--- REPORTE DE VENTAS DEL DÍA ---")
    for tipo, monto in rep["ventas_por_tipo"].items():
        print(f"  {tipo}: Bs {monto:.2f}")
    print("\nTop 3 productos más vendidos:")
    if not rep["top_3_productos"]:
        print("  Sin ventas registradas.")
    for nombre, cant in rep["top_3_productos"]:
        print(f"  - {nombre}: {cant} unidad(es)")


def main() -> None:
    rest = Restaurante("Sabor Valluno")
    cargar_datos_iniciales(rest)

    while True:
        print("\n=== SABOR VALLUNO (VARIANTE E) ===")
        print("1. Registrar producto o combo")
        print("2. Listar menú disponible por día")
        print("3. Registrar cliente")
        print("4. Crear pedido (y agregar/quitar productos)")
        print("5. Ver detalle de un pedido")
        print("6. Cambiar estado de un pedido")
        print("7. Cobrar pedido")
        print("8. Reporte de ventas del día")
        print("9. Registrar tiempo de entrega (Delivery - Regla 9)")
        print("0. Salir")

        opcion = input("Elige una opción: ").strip()
        try:
            if opcion == "1":
                opcion_registrar_producto(rest)
            elif opcion == "2":
                opcion_listar_menu_dia(rest)
            elif opcion == "3":
                opcion_registrar_cliente(rest)
            elif opcion == "4":
                opcion_crear_pedido(rest)
            elif opcion == "5":
                opcion_ver_detalle(rest)
            elif opcion == "6":
                opcion_cambiar_estado(rest)
            elif opcion == "7":
                opcion_cobrar_pedido(rest)
            elif opcion == "8":
                opcion_reporte_ventas(rest)
            elif opcion == "9":
                opcion_registrar_tiempo_delivery(rest)
            elif opcion == "0":
                print("Hasta luego.")
                break
            else:
                print("Opción no válida.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()