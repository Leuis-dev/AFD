import PySimpleGUI as sg
from AFD import AutomataFinitoDeterminista

class Interfaz:
    def __init__(self):
        #Creamos las ventanas con sus cajas de texto
        self.ventana1 = [
            [sg.Text(f"Ingrese las transiciones de la forma:\n'origen, símbolo -> destino'\nPonga una transición por línea"), sg.Multiline(key='transiciones', size=(30, 5))],
            [sg.Text('Estado inicial:'), sg.InputText(key='estado_inicial')],
            [sg.Text('Estados finales (de la forma q0,q1,q2): '), sg.InputText(key='estados_finales')],
            [sg.Button('Crear autómata')]
        ]
        self.ventana2 = [
            [sg.Text('Autómata creado con éxito!')],
            [sg.Text('Ingrese la palabra que desee probar:'), sg.InputText(key='palabra')],
            [sg.Button('Probar'), sg.Button('Cancelar')],
            [sg.Text('', key='resultado')]
        ]
    #Función para desglosar las transiciones ingresadas y dejarlas en un diccionario
    def parsear_transiciones(self, texto_transiciones):
        transiciones = {}
        lineas = texto_transiciones.strip().split('\n')

        #Se iteran las líneas
        for linea in lineas:
            #Se divide el string "origen, símbolo -> destino" en "->", y luego en ","
            partes = linea.strip().split('->')
            origen, resto = partes[0].strip().split(',')
            simbolo = resto.strip()
            destino = partes[1].strip()
            #Se añade al diccionario 
            transiciones[(origen.strip(), simbolo)] = destino.strip()
        return transiciones

    #Ejecutamos la gui
    def ejecutar(self):
        
        #Definimos la ventana inicial
        ventana = sg.Window('Autómata finito determinista', self.ventana1)

        while True:
            evento, valores = ventana.read()

            if evento == sg.WIN_CLOSED or evento == 'Cancelar':
                break
            
            #Al presionar crear autómata, definimos las variables ingresadas y cambiamos a la ventana2
            if evento == 'Crear autómata':
                transiciones = self.parsear_transiciones(valores['transiciones'])
                estado_inicial = valores['estado_inicial']
                estados_finales = valores['estados_finales'].split(',')
                #Si algún elemento del autómata no fue ingresado
                if transiciones == "" or estado_inicial == "" or estados_finales == "":
                    sg.popup('Error, debes ingresar todas las variables del autómata.')

                #En caso contrario, seguir a la siguiente ventana
                else:
                    ventana.close()
                    ventana = sg.Window('Autómata finito determinista', self.ventana2)

            #Al presionar probar en la ventana2, 
            elif evento == 'Probar':
                #Se crea una instancia de afd
                afd = AutomataFinitoDeterminista(transiciones, estado_inicial, estados_finales)
                palabra = valores['palabra']
                
                #Se verifica el método acepta_cadena() con la palabra y se imprime el resultado
                if afd.acepta_cadena(palabra):
                    ventana.find_element('resultado').update(f"La palabra '{palabra}' es aceptada por el autómata")
                else:
                    ventana.find_element('resultado').update(f"La palabra '{palabra}' no es aceptada por el autómata")
                ventana.find_element('palabra').update('')

if __name__ == "__main__":
    gui = Interfaz()
    gui.ejecutar()