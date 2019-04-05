import automata
import math

"""
Autor: Héctor Daniel Rodríguez Feregrino

Este programa utiliza una Lista de Adyacencia para reconocer y encontrar las raices
de un polinomio de grado 1 o 2.

Consideraciones: El formato para la entrada es: Ax^2+Bx+C=0 ó Bx+C=0, en ese orden específico,
donde A, B y C son constantes enteras positivas o negativas. En caso de tener Bx+C=0 el programa
regresará la raiz única y si se tiene Ax^2+Bx+C=0 regresará el conjunto de raices, sean enteras
o conplejas.

"""


automata1 = automata.Automata()

areaStates = {
    'q0': [
        [ r'[\d\-]', 'q1', ['add2Coef'] ],
        [ r'x', 'q3', [] ]
    ],
    'q1': [
        [ r'\d', 'q1', ['add2Coef'] ],
        [ r'x', 'q3', [] ]
    ],
    'q2': [
        [ r'[\+\-]', 'q5', ['changeCoef'] ],
        [ r'=', 'q9', [] ]
    ],
    'q3': [
        [ r'[\+\-]', 'q11', ['itExist', 'changeCoef'] ],
        [ r'=', 'q9', ['itExist'] ],
        [ r'\^', 'q4', [] ]
    ],
    'q4': [
        [ r'2', 'q2', ['changeCoef', 'itExist'] ]
    ],
    'q5': [
        [ r'\d', 'q6', ['add2Coef'] ],
        [ r'x', 'q7', [] ]
    ],
    'q6': [
        [ r'\d', 'q6', ['add2Coef'] ],
        [ r'x', 'q7', [] ],
        [ r'=', 'q9', ['changeCoef'] ]
    ],
    'q7': [
        [ r'[\+\-]', 'q11', ['itExist', 'changeCoef'] ],
        [ r'=', 'q9', ['itExist'] ]
    ],
    'q9': [
        [ r'0', 'q10', [] ]
    ],
    'q10': [
        # Exito
    ],
    'q11': [
        [ r'\d', 'q12', ['add2Coef'] ]
    ],
    'q12': [
        [ r'\d', 'q12', ['add2Coef'] ],
        [ r'=', 'q9', [] ]
    ]
}

automata1.autoFill(areaStates)
automata1.getState('q10').isSuccessfull = True

# -- Inician funciones que usará el automata.py --

def add2Coef(self, estadoActual, thing): # Nos permite agregar mas caracteres al coef
    if 'coefs' in self.vars and 'notAssigCoef' in self.vars:
        if thing != '+':
            self.vars['coefs'][self.vars['notAssigCoef']] += thing

def changeCoef(self, estadoActual, thing): # Cambia el coeficiente actual que está siendo encontrado
    if 'coefs' in self.vars and 'notAssigCoef' in self.vars:
        if estadoActual == 'q3':
            self.vars['notAssigCoef'] = 'c'
            if thing != '+':
                self.vars['coefs'][self.vars['notAssigCoef']] += thing
        if estadoActual == 'q2':
            self.vars['notAssigCoef'] = 'b'
            if thing != '+':
                self.vars['coefs'][self.vars['notAssigCoef']] += thing
        if estadoActual == 'q7':
            self.vars['notAssigCoef'] = 'c'
            if thing != '+':
                self.vars['coefs'][self.vars['notAssigCoef']] += thing

        if estadoActual == 'q4':
            self.vars['coefs']['a'] = self.vars['coefs'][self.vars['notAssigCoef']]
            self.vars['coefs'][self.vars['notAssigCoef']] = ''
            self.vars['notAssigCoef'] = 'a'
        if estadoActual == 'q6':
            self.vars['coefs']['c'] = self.vars['coefs'][self.vars['notAssigCoef']]
            self.vars['coefs'][self.vars['notAssigCoef']] = ''
            self.vars['notAssigCoef'] = 'c'
    
def itExist(self, estadoActual, thing): # Coloca un 1 a las x solas
    if 'coefs' in self.vars and 'notAssigCoef' in self.vars:
        if self.vars['coefs'][self.vars['notAssigCoef']] == '':
            self.vars['coefs'][self.vars['notAssigCoef']] = '1'

# -- Terminan funciones que usará el automata.py --


def setCoefs(): # Vuelve los coefs enteros
    for name,coef in coefs.items():
        if coef == '':
            coefs[name] = 0
        elif coef == '-':
            coefs[name] = -1
        else:
            coefs[name] = int(coef)

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


automata1.addVar('notAssigCoef', 'b')   # Variables temporal para el coeficiente actual
automata1.addVar('coefs', {             # Coeficientes
    'a': '',
    'b': '',
    'c': ''
})

automata1.addFunction(add2Coef)
automata1.addFunction(changeCoef)
automata1.addFunction(itExist)

polinomio = input()

if automata1.run(polinomio): # Corremos el autómata
    coefs = automata1.vars['coefs']
    setCoefs()
    print('El polinomio es: {}'.format(polinomio))
    print('Coefs = a:{}, b:{}, c:{}'.format(coefs['a'], coefs['b'], coefs['c']))
    getXs()

else:
    print('{} no es un polinomio válido'.format(polinomio))