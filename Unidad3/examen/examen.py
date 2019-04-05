import re

"""
Autor: Héctor Daniel Rodríguez Feregrino

Este programa valida una peticion HTTP en el archivo
indicado en la variable fileName

"""

fileName = 'prueba1.txt'

HTTP = ''
with open(fileName) as file:
    for line in file:
        HTTP += line

automata = { # El autómata como matriz
    'q0': [
        [r'^HTTP/', 'q30']
    ],
    'q30': [
        [r'^[0-9]', 'q1']
    ],
    'q1': [
        [r'^[0-9]', 'q1'],
        [r'^\.', 'q2'],
        [r'^ ', 'q3']
    ],
    'q2': [
        [r'^[0-9]', 'q1']
    ],
    'q3': [
        [r'^[0-9]', 'q28']
    ],
    'q28': [
        [r'^[0-9]', 'q28'],
        [r'^ ', 'q29']
    ],
    'q29': [
        [r'^[A-Z]', 'q4']
    ],
    'q4': [
        [r'^[A-Z]', 'q4'],
        [r'^\n', 'q5']
    ],
    'q5': [
        [r'^Date: ', 'q6']
    ],
    'q6': [
        [r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), [0-3][0-9] (Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9][0-9][0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9] GMT', 'q7']
    ],
    'q7': [
        [r'^\n', 'q8']
    ],
    'q8': [
        [r'^Server: ', 'q9']
    ],
    'q9': [
        [r'^[A-Z|a-z]', 'q31']
    ],
    'q31': [
        [r'^[A-Z|a-z]', 'q31'],
        [r'^\n', 'q10']
    ],
    'q10': [
        [r'^Last-Modified: ', 'q11']
    ],
    'q11': [
        [r'^(True|False), ', 'q11.5']
    ],
    'q11.5': [
        [r'^[0-3][0-9] (Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [0-9][0-9][0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9] GMT', 'q12']
    ],
    'q12': [
        [r'^\n', 'q13']
    ],
    'q13': [
        [r'^ETag: ', 'q14']
    ],
    'q14': [
        [r'^"', 'q15']
    ],
    'q15': [
        [r'^[0-9|a-z]', 'q16']
    ],
    'q16': [
        [r'^[0-9|a-z]', 'q16'],
        [r'^\-', 'q32'],
        [r'^"', 'q18']
    ],
    'q32': [
        [r'^[0-9|a-z]', 'q16']
    ],
    'q18': [
        [r'^\n', 'q19']
    ],
    'q19': [
        [r'^Accept-Ranges: ', 'q20']
    ],
    'q20': [
        [r'^[a-z]', 'q33']
    ],
    'q33': [
        [r'^[a-z]', 'q33'],
        [r'^\n', 'q21']
    ],
    'q21': [
        [r'^Content-Length: ', 'q22']
    ],
    'q22': [
        [r'^[0-9]', 'q34']
    ],
    'q34': [
        [r'^[0-9]', 'q34'],
        [r'^\n', 'q23']
    ],
    'q23': [
        [r'^Content-Type: ', 'q24']
    ],
    'q24': [
        [r'^[a-z]', 'q25']
    ],
    'q25': [
        # Exito
        [r'^[a-z]', 'q25'],
        [r'^\/', 'q26']
    ],
    'q26': [
        [r'^[a-z]', 'q25']
    ],
}

# Código

actState = 'q0'
auxStr = HTTP
correctStr = ''

while True:
    if actState in automata:
        flag = False
        for path in automata[actState]:
            foundThings = re.split(path[0], auxStr)
            if len(foundThings) > 1:
                correctStr += (re.search(path[0], auxStr)).group()
                foundThings = foundThings[len(foundThings)-1]
                flag = True
                actState = path[1]
                auxStr = ''.join(foundThings)
                break
        if not flag:
            if actState != 'q25':
                print('No se encontró un path viable')
            break
    else:
        print('El estado no está en el autómata')
        break



textColors = {
    'reset': '\033[0m',
    'green': '\033[32m',
    'red': '\033[31m',
    'blue': '\033[34m',
    'bold': '\033[01m',
}

import os           
os.system('color')          # Activate color mode in terminal

if actState == 'q25':
    print('\n{}{}¡Es valida la petición!{}\n'.format(textColors['green'], textColors['bold'],
        textColors['reset']))
else:
    print('\n{}{}No es valida la petición...{}\n'.format(textColors['red'], textColors['bold'],
        textColors['reset']))

print('{}{}{}{}'.format(textColors['green'], textColors['bold'],
    correctStr, textColors['reset']), end='')

print('{}{}{}{}'.format(textColors['red'], textColors['bold'],
    auxStr, textColors['reset']))
