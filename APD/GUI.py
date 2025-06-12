import PySimpleGUI as sg
from APD import AutomataPushDown # Importa la clase AutomataPushDown desde APD.py

class Interfaz:
    def __init__(self):
        self.transiciones = {} # Diccionario para almacenar las transiciones del APD
        self.estado_final = '' # Almacena el estado final (un único string)
        self.estado_inicial = 'q0' # Almacena el estado inicial
        self.modo_aceptacion = 'estado_final' # Modo de aceptación por defecto

        fuente = ('Helvetica', 18) # Fuente para los elementos de la GUI

        # Definición del layout de la ventana principal
        self.ventana1_layout = [
            [sg.Text('Ingrese una transición por partes:', font=fuente)],
            [
                sg.Input(key='origen', size=(5, 1), font=fuente, justification='center'),
                sg.Text(',', font=fuente),
                sg.Input(key='simbolo', size=(3, 1), font=fuente, justification='center'),
                sg.Text(',', font=fuente),
                sg.Input(key='tope', size=(3, 1), font=fuente, justification='center'),
                sg.Text('→', font=fuente),
                sg.Input(key='destino', size=(5, 1), font=fuente, justification='center'),
                sg.Text(',', font=fuente),
                sg.Input(key='push', size=(6, 1), font=fuente, justification='center'),
                sg.Button('Agregar transición', font=fuente)
            ],[
                sg.Text('Use "E" para representar una transición vacía (ε)', font=fuente)],
            [sg.Listbox(values=[], size=(80, 10), key='lista_transiciones', font=fuente)], # Muestra las transiciones añadidas
            
            [sg.Text('Estado inicial:', font=fuente),
             sg.Input(key='origen_inicial', size=(5, 1), font=fuente, justification='center', default_text='q0')],
            
            [sg.Text('Modo de aceptación:', font=fuente),
             sg.Combo(values=['estado_final', 'pila_vacia'], default_value='estado_final', key='modo', font=fuente, enable_events=True)],
            
            [sg.Text('Estado final:', font=fuente, key='lbl_final'), # Etiqueta para el campo de estado final
             sg.Input(key='estado_final_input', font=fuente, visible=True)], # Campo de entrada para el estado final
            
            [sg.Button('Siguiente', font=fuente), sg.Button('Cancelar', font=fuente)]
        ]

        # Creación de la ventana principal
        self.ventana = sg.Window('Autómata Push Down', self.ventana1_layout, size=(1200, 800), font=fuente, finalize=True)

    def ejecutar(self):
        # Bucle principal de eventos de la ventana
        while True:
            evento, valores = self.ventana.read() # Lee eventos y valores de los elementos de la GUI

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break # Sale del bucle si se cierra la ventana o se presiona Cancelar

            if evento == 'Agregar transición':
                # Recoge los valores de los campos de entrada de la transición
                origen = valores['origen'].strip()
                simbolo = valores['simbolo'].strip()
                tope = valores['tope'].strip()
                destino = valores['destino'].strip()
                cadena_a_apilar = valores['push'].strip()

                # Validación simple de que todos los campos estén llenos
                if not all([origen, simbolo, tope, destino, cadena_a_apilar]):
                    sg.popup_error('Todos los campos de la transición deben ser llenados.')
                    continue

                # Determina la acción de pila para el APD (pop o push)
                accion_para_apd = ''
                if cadena_a_apilar == 'E': # 'E' en la GUI se traduce a 'pop' en el APD
                    accion_para_apd = 'pop'
                else: # Cualquier otra cosa es un 'push'
                    accion_para_apd = f'push({cadena_a_apilar})'

                # Crea la clave (origen, simbolo, tope) y el valor (destino, accion_pila) para el diccionario de transiciones
                key = (origen, simbolo, tope)
                value = (destino, accion_para_apd)

                self.transiciones[key] = value # Añade la transición al diccionario
                
                # Actualiza la lista de transiciones mostradas en la GUI
                self.ventana['lista_transiciones'].update(values=[
                    f"({k[0]}, {k[1]}, {k[2]}) → ({v[0]}, {v[1].replace('push(', '').replace(')', '').replace('pop', 'ε')})" 
                    for k, v in self.transiciones.items()
                ])
                
                # Limpia los campos de entrada de la transición
                for k in ['origen', 'simbolo', 'tope', 'destino', 'push']:
                    self.ventana[k].update('')
                
                self.ventana['origen'].set_focus() # Pone el foco de nuevo en el campo 'origen'

            elif evento == 'modo':
                # Actualiza el modo de aceptación y ajusta la visibilidad del campo "Estado final"
                self.modo_aceptacion = valores['modo']
                if self.modo_aceptacion == 'pila_vacia':
                    self.ventana['estado_final_input'].update(visible=False)
                    self.ventana['lbl_final'].update(visible=False)
                else:
                    self.ventana['estado_final_input'].update(visible=True)
                    self.ventana['lbl_final'].update(visible=True)

            elif evento == 'Siguiente':
                # Recoge el estado inicial y el estado final desde la GUI
                self.estado_inicial = valores['origen_inicial'].strip()
                self.estado_final = valores['estado_final_input'].strip() 

                # Validaciones antes de pasar a la ventana de prueba
                if not self.transiciones:
                    sg.popup_error('Debe agregar al menos una transición.')
                    continue
                if not self.estado_inicial:
                    sg.popup_error('Debe especificar un estado inicial.')
                    continue
                if self.modo_aceptacion == 'estado_final' and not self.estado_final:
                    sg.popup_error('Debe especificar un estado final para el modo de aceptación por estado final.')
                    continue
                
                self.mostrar_ventana_palabras() # Muestra la ventana para probar palabras
                break # Sale del bucle de la ventana principal

        self.ventana.close() # Cierra la ventana principal al salir del bucle

    def mostrar_ventana_palabras(self):
        fuente = ('Helvetica', 18)
        # Layout de la ventana para probar palabras
        layout = [
            [sg.Text('Ingrese palabras para probar:', font=fuente)],
            [sg.Input(key='palabra_test', font=fuente), sg.Button('Probar', font=fuente)],
            [sg.Listbox(values=[], size=(80, 10), key='resultados_prueba', font=fuente)], # Muestra los resultados de las pruebas
            [sg.Button('Volver', font=fuente)]
        ]

        ventana_prueba = sg.Window('Probar Palabras', layout, size=(800, 300), font=fuente)

        # Crea una instancia del Autómata de Pila con la configuración definida en la ventana anterior
        apd = AutomataPushDown(
            transiciones=self.transiciones,
            estado_inicial=self.estado_inicial,
            estado_final=self.estado_final,
            modo_aceptacion=self.modo_aceptacion
        )
        
        # Bucle de eventos para la ventana de prueba de palabras
        while True:
            evento, valores = ventana_prueba.read()

            if evento == sg.WIN_CLOSED or evento == 'Volver':
                break # Sale del bucle si se cierra la ventana o se presiona Volver

            if evento == 'Probar':
                palabra = valores['palabra_test'].strip()
                if not palabra:
                    sg.popup_warning('Ingrese una palabra para probar.')
                    continue

                # Prueba la palabra con el APD y obtiene el resultado
                resultado = apd.acepta_cadena(palabra)
                
                # Actualiza la lista de resultados en la GUI
                current_results = ventana_prueba['resultados_prueba'].get_list_values()
                current_results.append(f"'{palabra}': {'ACEPTADA' if resultado else 'RECHAZADA'}")
                ventana_prueba['resultados_prueba'].update(values=current_results)
                ventana_prueba['palabra_test'].update('') # Limpia el campo de entrada de palabra
        
        ventana_prueba.close() # Cierra la ventana de prueba

if __name__ == '__main__':
    gui = Interfaz()
    gui.ejecutar()