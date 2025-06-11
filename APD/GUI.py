import PySimpleGUI as sg
from APD import AutomataPushDown

class Interfaz:
    def __init__(self):
        self.transiciones = {}
        self.transiciones_lista = []
        self.modo_aceptacion = 'estado_final'
        self.estado_final = ''

        fuente = ('Helvetica', 18)
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
            [sg.Listbox(values=[], size=(80, 10), key='lista_transiciones', font=fuente)],
            [sg.Text('Modo de aceptación:', font=fuente),
             sg.Combo(values=['estado_final', 'pila_vacia'], default_value='estado_final', key='modo', font=fuente, enable_events=True)],
            [sg.Text('Estado(s) final(es):', font=fuente, key='lbl_final'),
             sg.Input(key='estado_final', font=fuente, visible=True)],
            [sg.Button('Siguiente', font=fuente), sg.Button('Cancelar', font=fuente)]
        ]

        self.ventana = sg.Window('Autómata Push Down', self.ventana1_layout, size=(1200, 800), font=fuente, finalize=True)

    def ejecutar(self):
        while True:
            evento, valores = self.ventana.read()

            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if evento == 'modo':
                self.modo_aceptacion = valores['modo']
                mostrar = self.modo_aceptacion == 'estado_final'
                self.ventana['estado_final'].update(visible=mostrar)
                self.ventana['lbl_final'].update(visible=mostrar)

            if evento == 'Agregar transición':
                origen = valores['origen'].strip()
                simbolo = valores['simbolo'].strip()
                tope = valores['tope'].strip()
                destino = valores['destino'].strip()
                push = valores['push'].strip()

                if all([origen, simbolo, tope, destino, push]):
                    # Si el usuario escribe 'E' en push, significa que debe hacer pop
                    if push == 'E':
                        accion = 'pop'
                    else:
                        accion = f'push({push})'
                    
                    self.transiciones_lista.append(f"{origen}, {simbolo}, {tope} -> {destino}, {accion}")
                    self.transiciones[(origen, simbolo, tope)] = (destino, accion)

                    self.ventana['lista_transiciones'].update(self.transiciones_lista)

                    # Limpiar casillas y volver al inicio
                    self.ventana['origen'].update('')
                    self.ventana['simbolo'].update('')
                    self.ventana['tope'].update('')
                    self.ventana['destino'].update('')
                    self.ventana['push'].update('')
                    self.ventana['origen'].SetFocus()
                else:
                    sg.popup('Por favor, completa todos los campos.', font=('Helvetica', 16))

            if evento == 'Siguiente':
                if not self.transiciones:
                    sg.popup('Debes agregar al menos una transición.')
                    continue

                if self.modo_aceptacion == 'estado_final' and not valores['estado_final'].strip():
                    sg.popup('Debes ingresar al menos un estado final.')
                    continue

                self.estado_final = valores['estado_final'].strip().split(',') if self.modo_aceptacion == 'estado_final' else []

                self.ventana.close()
                self.mostrar_ventana_palabras()

    def mostrar_ventana_palabras(self):
        fuente = ('Helvetica', 18)
        layout = [
            [sg.Text('Ingrese una palabra para evaluar:', font=fuente)],
            [sg.Input(key='palabra', size=(40, 1), font=fuente)],
            [sg.Button('Probar', font=fuente), sg.Button('Cancelar', font=fuente)],
            [sg.Text('', key='resultado', size=(80, 2), font=fuente)]
        ]

        ventana = sg.Window('Probar Palabras', layout, size=(800, 300), font=fuente)

        apd = AutomataPushDown(
            transiciones=self.transiciones,
            estado_inicial='q0',
            estado_final=self.estado_final,
            modo_aceptacion=self.modo_aceptacion
        )


        while True:
            evento, valores = ventana.read()
            if evento in (sg.WIN_CLOSED, 'Cancelar'):
                break

            if evento == 'Probar':
                palabra = valores['palabra']
                aceptada = apd.acepta_cadena(palabra)
                msg = f"La palabra '{palabra}' es ACEPTADA ✅" if aceptada else f"La palabra '{palabra}' es RECHAZADA ❌"
                ventana['resultado'].update(msg)
                ventana['palabra'].update('')

        ventana.close()


if __name__ == "__main__":
    gui = Interfaz()
    gui.ejecutar()
