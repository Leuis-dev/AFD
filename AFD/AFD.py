class AutomataFinitoDeterminista:
	def __init__(self, transiciones, estado_inicial, estados_finales):
		self.transiciones = transiciones
		self.estado_inicial = estado_inicial
		self.estados_finales = estados_finales

	def transicion(self, estado, simbolo):
		return self.transiciones.get((estado, simbolo))

	def acepta_cadena(self, cadena):
		estado_actual = self.estado_inicial
		for simbolo in cadena:
			estado_actual = self.transicion(estado_actual, simbolo)
			if estado_actual is None:
				return False
		return estado_actual in self.estados_finales
