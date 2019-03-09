import re

polinomio = 'x*2-x+1=0'

estadoActual = 'q0'

automata = {
    'q0': [
        [r'[\d\-]', 'q1'],
        [r'x', 'q3']
    ],
    'q1': [
        [r'\d', 'q1'],
        [r'x', 'q3']
    ],
    'q2': [
        [r'[\+\-]', 'q5'],
        [r'=', 'q9']
    ],
    'q3': [
        [r'[\+\-]', 'q11'],
        [r'=', 'q9'],
        [r'\*', 'q4']
    ],
    'q4': [
        [r'2', 'q2']
    ],
    'q5': [
        [r'\d', 'q6'],
        [r'x', 'q7']
    ],
    'q6': [
        [r'\d', 'q6'],
        [r'x', 'q7'],
        [r'=', 'q9']
    ],
    'q7': [
        [r'[\+\-]', 'q11'],
        [r'=', 'q9']
    ],
    'q9': [
        [r'0', 'q10']
    ],
    'q10': [
        #Exito
    ],
    'q11': [
        [r'\d', 'q12']
    ],
    'q12': [
        [r'\d', 'q12'],
        [r'=', 'q9']
    ]
}



for char in polinomio:
    flag = False
    #print('Vamos en {}, estado: {}'.format(char, estadoActual))
    for test in automata[estadoActual]:
        #print(test)
        if re.findall(test[0], char) != []:
            flag = True
            #print('Nos cambiamos al estado {}'.format(test[1]))
            estadoActual = test[1]
            break
    if not flag:
        #print('No pasa')
        break

if estadoActual == 'q10':
    print('Llegamos al final correctamente')
else:
    print('No se llegó al final')

