from random import *

#función listaL
def estadosInicialFina(n,a,b):
    L=[]
    for i in range(n):
        num=randint(a,b)
        L.append(num)
    return L

eFinales=[]
continuar = False

def verificar_estado(estado):
    # Verifica la longitud de la cadena
    if len(estado) <= 0 or len(estado) > 3:
        return False
    
    # Verifica que cada caracter sea una letra o un dígito
    for c in estado:
        if not c.isalnum():
            return False
    return True

#-------------------------------------------------
while continuar == False :
    q0 = str(input("Ingrese el Estado Inicial: "))
    if verificar_estado(q0):
        continuar = True
    else: print("Estado inicial ingresado inválido")

nFinales = int(input("¿Cuántos estados finales tendrá el autómata?: "))

# ciclo for desde 0 hasta nFinales-1
for i in range(1,nFinales+1):
    x = str(input("Ingrese el Estado Final número {}: ".format(i)))
    if verificar_estado(x):
        eFinales.append(x)
    else: print("Estado final ingresado inválido")

# Solo para corroborar que hay estados finales en el arreglo "eFinales"
#print(", ".join(eFinales))





