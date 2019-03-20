import re
import math

# Variables 

polinomio = input()
estadoActual = 'q0'   # Estado actual
notAssigCoef = 'b'    # Variables temporal para el coeficiente actual
coefs = {             # Coeficientes
    'a': '',
    'b': '',
    'c': ''
}            

# Funciones necesarias

def add2Coef(thing): # Nos permite agregar mas caracteres al coef
    if thing != '+':
        coefs[notAssigCoef] += thing

def setCoefs(): # Vuelve los coefs enteros
    for name,coef in coefs.items():
        if coef == '':
            coefs[name] = 0
        elif coef == '-':
            coefs[name] = -1
        else:
            coefs[name] = int(coef)

def changeCoef(thing): # Cambia el coeficiente actual que está siendo encontrado
    global notAssigCoef

    if estadoActual == 'q3':
        notAssigCoef = 'c'
        if thing != '+':
            coefs[notAssigCoef] += thing
    if estadoActual == 'q2':
        notAssigCoef = 'b'
        if thing != '+':
            coefs[notAssigCoef] += thing
    if estadoActual == 'q7':
        notAssigCoef = 'c'
        if thing != '+':
            coefs[notAssigCoef] += thing

    if estadoActual == 'q4':
        coefs['a'] = coefs[notAssigCoef]
        coefs[notAssigCoef] = ''
        notAssigCoef = 'a'
    if estadoActual == 'q6':
        coefs['c'] = coefs[notAssigCoef]
        coefs[notAssigCoef] = ''
        notAssigCoef = 'c'
    
def itExist(thing): # Coloca un 1 a las x solas
    global notAssigCoef
    if coefs[notAssigCoef] == '':
        coefs[notAssigCoef] = '1'

def getXs(): # Encuentra las Xs del polinomio
    a = coefs['a']
    b = coefs['b']
    c = coefs['c']

    print()

    if a != 0: # El polinomio tiene 2 raices
        d = (b*b) - (4*a*c)
        complexRoot = False

        if d < 0:
            complexRoot = True
            d = math.fabs(d)

        if complexRoot: 
            print('x1 = {} + {}i'.format(
                (-1*b/2*a), (math.sqrt(d)/(2*a))
            ))
            print('x2 = {} - {}i'.format(
                (-1*b/2*a), (math.sqrt(d)/(2*a))
            ))
        else:
            print('x1 = {}'.format(
                (-1*b/2*a) + (math.sqrt(d)/(2*a))
            ))
            print('x2 = {}'.format(
                (-1*b/2*a) - (math.sqrt(d)/(2*a))
            ))
    else: # El polinomio tiene una raiz
        print('x = {}'.format(
            (-1*c) / b
        ))

automata = { # El autómata como matriz
    'q0': [
        [r'[\d\-]', 'q1', [add2Coef]],
        [r'x', 'q3']
    ],
    'q1': [
        [r'\d', 'q1',[add2Coef]],
        [r'x', 'q3']
    ],
    'q2': [
        [r'[\+\-]', 'q5', [changeCoef]],
        [r'=', 'q9']
    ],
    'q3': [
        [r'[\+\-]', 'q11', [itExist, changeCoef]],
        [r'=', 'q9', [itExist]],
        [r'\^', 'q4']
    ],
    'q4': [
        [r'2', 'q2', [changeCoef, itExist]]
    ],
    'q5': [
        [r'\d', 'q6', [add2Coef]],
        [r'x', 'q7']
    ],
    'q6': [
        [r'\d', 'q6', [add2Coef]],
        [r'x', 'q7'],
        [r'=', 'q9', [changeCoef]]
    ],
    'q7': [
        [r'[\+\-]', 'q11', [itExist, changeCoef]],
        [r'=', 'q9', [itExist]]
    ],
    'q9': [
        [r'0', 'q10']
    ],
    'q10': [
        # Exito
    ],
    'q11': [
        [r'\d', 'q12', [add2Coef]]
    ],
    'q12': [
        [r'\d', 'q12', [add2Coef]],
        [r'=', 'q9']
    ]
}

# Código

isValid = True

for char in polinomio:
    flag = False
    for test in automata[estadoActual]:
        findThing = re.findall(test[0], char)
        if findThing != []:
            flag = True
            if len(test) > 2:
                for function in test[2]:
                    function(findThing[0])
            estadoActual = test[1]
            break
    if not flag:
        isValid = False
        break

if estadoActual == 'q10' and isValid: # Si llegó al final exitoso
    setCoefs()
    print('El polinomio es: {}'.format(polinomio))
    print('Coefs = a:{}, b:{}, c:{}'.format(coefs['a'], coefs['b'], coefs['c']))
    getXs()

else: # Si no llegó a estado de éxito
    print('{} no es un polinomio válido'.format(polinomio))