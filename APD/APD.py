import collections

class AutomataPushDown:
    def __init__(self, transiciones, estado_inicial, estado_final, modo_aceptacion, simbolo_inicial_pila='R'):
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final # Puede ser un string para estado final o un estado si es por pila vacía
        self.modo_aceptacion = modo_aceptacion # 'estado_final' o 'pila_vacia'
        self.simbolo_inicial_pila = simbolo_inicial_pila # Símbolo inicial de la pila, ej. 'R'

    def acepta_cadena(self, cadena):
        # Cola para almacenar las configuraciones pendientes a explorar (estado, pila, índice de la cadena)
        configuraciones_pendientes = collections.deque([(self.estado_inicial, tuple([self.simbolo_inicial_pila]), 0)])
        # Conjunto para evitar ciclos infinitos y re-explorar configuraciones ya visitadas
        configuraciones_visitadas = set()

        while configuraciones_pendientes:
            estado_actual, pila_actual_tupla, i = configuraciones_pendientes.popleft()
            pila_actual_lista = list(pila_actual_tupla) # Convertir tupla a lista para modificar la pila

            configuracion_actual_key = (estado_actual, tuple(pila_actual_lista), i)
            if configuracion_actual_key in configuraciones_visitadas:
                continue # Ya exploramos esta configuración, evitar bucles
            configuraciones_visitadas.add(configuracion_actual_key)

            # Verificar si la cadena ha sido completamente leída
            if i == len(cadena):
                # Si se llegó al final de la cadena, verificar la condición de aceptación
                if self.modo_aceptacion == 'estado_final' and estado_actual == self.estado_final:
                    return True # Aceptada por estado final
                if self.modo_aceptacion == 'pila_vacia' and not pila_actual_lista:
                    return True # Aceptada por pila vacía
                # Si no se cumple ninguna condición de aceptación al final de la cadena,
                # pero aún hay transiciones épsilon posibles, se seguirán explorando.

            # Si la pila está vacía y no hemos aceptado (y no es el modo pila_vacia en el final de cadena),
            # esta rama no puede avanzar.
            if not pila_actual_lista:
                continue 
            
            tope_pila = pila_actual_lista[-1] # Obtener el símbolo en la cima de la pila

            # Determinar el símbolo de entrada actual: carácter de la cadena o 'E' (epsilon) si la cadena ya se consumió
            simbolo_entrada_actual = cadena[i] if i < len(cadena) else 'E'
            
            transicion_encontrada_data = None
            simbolo_consumido_por_transicion = None

            # 1. Prioridad: Buscar transición consumiendo un símbolo de la cadena (si hay entrada disponible)
            if i < len(cadena) and (estado_actual, simbolo_entrada_actual, tope_pila) in self.transiciones:
                transicion_encontrada_data = self.transiciones[(estado_actual, simbolo_entrada_actual, tope_pila)]
                simbolo_consumido_por_transicion = simbolo_entrada_actual
            # 2. Si no hay transición consumiendo símbolo, buscar una transición épsilon
            elif (estado_actual, 'E', tope_pila) in self.transiciones:
                transicion_encontrada_data = self.transiciones[(estado_actual, 'E', tope_pila)]
                simbolo_consumido_por_transicion = 'E'

            # Si no se encontró ninguna transición válida, esta rama de ejecución muere
            if transicion_encontrada_data is None:
                continue

            # Aplicar la transición encontrada
            nuevo_estado, accion_pila = transicion_encontrada_data
            
            nueva_pila_para_rama = pila_actual_lista[:] # Copiar la pila para la nueva configuración

            # Error de lógica: Si el tope de pila no coincide (no debería pasar en un APD determinista bien definido)
            if not nueva_pila_para_rama or nueva_pila_para_rama[-1] != tope_pila:
                continue 
            
            nueva_pila_para_rama.pop() # Siempre se hace un pop del tope de pila al aplicar una transición

            # Realizar la acción de push si la transición lo indica
            if accion_pila.startswith('push'):
                simbolos_a_apilar = accion_pila[5:-1] # Extraer los símbolos a apilar (ej. 'AR' de 'push(AR)')
                # Apilar símbolos en orden inverso para que el primero quede al fondo (ej. 'AR' -> R luego A)
                for s in reversed(simbolos_a_apilar): 
                    nueva_pila_para_rama.append(s)
            elif accion_pila == 'pop':
                pass # El pop ya se hizo arriba

            # Avanzar el índice de la cadena solo si se consumió un símbolo real
            nuevo_i = i
            if simbolo_consumido_por_transicion != 'E': 
                nuevo_i += 1
            
            # Añadir la nueva configuración a la cola para seguir explorando
            configuraciones_pendientes.append((nuevo_estado, tuple(nueva_pila_para_rama), nuevo_i))

        # Si todas las configuraciones han sido exploradas y ninguna llevó a la aceptación
        return False