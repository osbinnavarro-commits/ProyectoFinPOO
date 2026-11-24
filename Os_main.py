from plato import Plato
from bebidas import Bebidas
from combo_producto import ComboProducto
from combo import Combo
from cliente import Cliente
from pedido_llevar import PedidoLlevar
from pago_efectivo import PagoEfectivo

todos_los_dias = [
    "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"
]

# 1. Crear los platos y bebidas del menú (objetos)
silpancho = Plato("Silpancho", 35.0, todos_los_dias)
pique = Plato("Pique Macho", 48.0, todos_los_dias)
chicharron = Plato("Chicharrón", 45.0, ["domingo"])
sopa_mani = Plato("Sopa de Maní", 18.0, todos_los_dias)
mocochinchi = Bebidas("Mocochinchi", 6.0, 1.0)

menu = [silpancho, pique, chicharron, sopa_mani, mocochinchi]

# 2. Armar un combo (Variante E: 10% descuento)
cp = ComboProducto([chicharron, mocochinchi])
combo_valluno = Combo("Combo Valluno", cp)
menu.append(combo_valluno)

# 3. Registrar un cliente y un pedido para llevar (Variante E: Bs 3 por plato)
cliente = Cliente("Juan Pérez", "1234567", "71234567", "Av. América")
pedido = PedidoLlevar(1)
pedido.agregar_producto(combo_valluno, 1)
cliente.realizar_pedido(pedido)

# 4. Mostrar resultado y cobrar en efectivo (Variante E: redondeo abajo a Bs 0,50)
subtotal = pedido.cal_subtotal()
recargo = pedido.cal_recargo()
total = round(subtotal + recargo, 2)

pago = PagoEfectivo(total, cod_recibo=101, monto_recibido=79.8)
cambio = pago.cal_cambio(pago._monto_recibido)
registro = pedido.realizar_pago(pago)

print(f"Cliente: {cliente.nombre}")
print(f"Subtotal: Bs {subtotal:.2f}")
print(f"Envases (Variante E): Bs {recargo:.2f}")
print(f"Total cobrado en efectivo: Bs {registro.monto:.2f}")
print(f"Cambio: Bs {cambio:.2f}")