import re

# Variables 

polinomio = input()

print('El polinomio es: {}'.format(polinomio))

estadoActual = 'q0'
notAssigCoef = 'b'    
coefs = {             
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
    if coefs[notAssigCoef] == '':
        coefs[notAssigCoef] = '1'

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

# Codigo

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
        break

if estadoActual == 'q10':
    setCoefs()
    print('Coefs = a:{}, b:{}, c:{}'.format(coefs['a'], coefs['b'], coefs['c']))
    print('Llegamos al final correctamente')

else:
    print('No se llegó al final')