class Cliente:
    def __init__(self, nombre, ci_cliente, telefono, direccion: str = ""):
        self.nombre = nombre
        self.ci_cliente = ci_cliente
        self.telefono = telefono
        self.direccion = direccion
        self._pedidos = []

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def ci_cliente(self):
        return self._ci_cliente

    @ci_cliente.setter
    def ci_cliente(self, valor):
        ci = str(valor).strip()
        if not ci:
            raise ValueError("El CI del cliente no puede estar vacío.")
        self._ci_cliente = ci

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        tel = str(valor).strip()
        if len(tel) != 8 or not tel.isdigit() or tel[0] not in ("6", "7"):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar en 6 o 7.")
        self._telefono = tel

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, valor):
        self._direccion = str(valor).strip()

    def realizar_pedido(self, pedido):
        if pedido is None:
            raise ValueError("El pedido no puede ser nulo.")
        self._pedidos.append(pedido)

    def historial(self):
        return list(self._pedidos)