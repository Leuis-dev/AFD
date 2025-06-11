class AutomataPushDown:
    def __init__(self, transiciones, estado_inicial, estado_final, modo_aceptacion, simbolo_inicial_pila='R'):
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final if isinstance(estado_final, list) else [estado_final]
        self.modo_aceptacion = modo_aceptacion  # 'estado_final' o 'pila_vacia'
        self.stack = [simbolo_inicial_pila]

    def transicion(self, estado, simbolo, tope):
        return self.transiciones.get((estado, simbolo, tope))

    def acepta_cadena(self, cadena):
        pila = self.stack.copy()
        estado_actual = self.estado_inicial
        i = 0  # índice de la palabra

        while True:
            if not pila:
                return False  # La pila no debería vaciarse prematuramente

            tope = pila[-1]
            simbolo = cadena[i] if i < len(cadena) else 'E'

            # Probar primero con el símbolo actual
            resultado = self.transicion(estado_actual, simbolo, tope)

            # Si no hay transición con el símbolo actual, intentamos con 'E' (ε-transición)
            if resultado is None and simbolo != 'E':
                resultado = self.transicion(estado_actual, 'E', tope)

            if resultado is None:
                break  # No hay transición válida, se detiene

            nuevo_estado, accion = resultado

            if accion.startswith('push'):
                pila.append(accion[5:-1])  # Extrae el símbolo dentro de push()
            elif accion == 'pop':
                pila.pop()
            elif accion == 'nop':
                pass  # No hacer nada
            else:
                return False  # Acción inválida

            estado_actual = nuevo_estado

            if simbolo != 'E':
                i += 1  # Sólo avanzamos si consumimos un símbolo de entrada

            if i >= len(cadena) and simbolo == 'E':
                break  # Terminamos cuando no quedan más símbolos que consumir y no hay más ε-transiciones

        if self.modo_aceptacion == 'estado_final':
            return estado_actual in self.estado_final

        elif self.modo_aceptacion == 'pila_vacia':
            return len(pila) == 0

        else:
            return False  # Modo inválido
