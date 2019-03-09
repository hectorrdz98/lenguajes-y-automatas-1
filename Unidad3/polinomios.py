import re
import math

# Variables 

examples = [
    'x=0',
    '-x=0',
    '2x=0',
    '-2x=0',
    '12x+5=0',
    '-6x-31=0',
    'x^2=0',
    '-x^2=0',
    '3x^2=0',
    '-6x^2=0',
    '-21x^2=0',
    'x^2+15=0',
    '-x^2-12=0',
    '-2x^2-5=0',
    '-x^2+2x=0',
    'x^2+25x=0',
    'x^2+2x+5=0',
    'x^2+x+1=0',
    'x^2+x=0',
    'x+1=0',
    'x^2-x+5=0',
    'x^2+x+5=0',
    'x+5=0',
    'x=0'
]

for polinomio in examples:
#for n in range(1):
#    polinomio = examples[19]

    estadoActual = 'q0'
    notAssigCoef = 'b'    # Variables temporal para el coeficiente actual
    coefs = {             # Coeficientes
        'a': '',
        'b': '',
        'c': ''
    }            


    # Funciones necesarias

    def add2Coef(thing):
        if thing != '+':
            coefs[notAssigCoef] += thing

    def setCoefs():
        for name,coef in coefs.items():
            if coef == '':
                coefs[name] = 0
            elif coef == '-':
                coefs[name] = -1
            else:
                coefs[name] = int(coef)

    def changeCoef(thing):
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
        
    
    def itExist(thing):
        global notAssigCoef
        #print('Entré con {}:{}'.format(notAssigCoef, coefs[notAssigCoef]))
        if coefs[notAssigCoef] == '':
            #print('Entremos al itExists con {} y {}\n'.format(notAssigCoef, coefs[notAssigCoef]))
            coefs[notAssigCoef] = '1'
    
    def getXs():
        a = coefs['a']
        b = coefs['b']
        c = coefs['c']

        print()

        if a != 0:
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
        else:
            print('x = {}'.format(
                (-1*c) / b
            ))

    automata = {
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

    for char in polinomio:
        flag = False
        #print('Vamos en {}, estado: {}, coefA: {}'.format(char, estadoActual, notAssigCoef))
        for test in automata[estadoActual]:
            #print(test)
            findThing = re.findall(test[0], char)
            if findThing != []:
                flag = True
                #print('Nos cambiamos al estado {}\n'.format(test[1]))
                if len(test) > 2:
                    for function in test[2]:
                        function(findThing[0])
                estadoActual = test[1]
                break
        if not flag:
            #print('No pasa')
            break

    if estadoActual == 'q10':
        setCoefs()
        print('El polinomio es: {}'.format(polinomio))
        print('Coefs = a:{}, b:{}, c:{}'.format(coefs['a'], coefs['b'], coefs['c']))
        getXs()
        #print('\nLlegamos al final correctamente')

    else:
        print('No es un polinomio válido')

    print()
    print()