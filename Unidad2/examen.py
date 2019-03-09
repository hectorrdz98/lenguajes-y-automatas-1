
"""
Autor: Hector Rodriguez
"""

"""

"""

import re

# Regex necesarias
RegexPatterns = {
    'No inicia con mayúscula': [
        'normal',
        r'(\w*\.\s*[a-z]\w*)'
    ],
    'Día con mayúscula': [
        'special',
        r'([Ll][Uu][Nn][Ee][Ss]|[Mm][Aa][Rr][Tt][Ee][Ss]|[Mm][Ii][EeÉé][Rr][Cc][Oo][Ll][Ee][Ss]|[Jj][Uu][Ee][Vv][Ee][Ss]|[Vv][Ii][Ee][Rr][Nn][Ee][Ss]|[Ss][AaÁá][Bb][Aa][Dd][Oo]|[Dd][Oo][Mm][Ii][Nn][Gg][Oo])',
        r'[A-Z]'
    ],
    'Mes con mayúscula': [
        'special',
        r'([Ee][Nn][Ee][Rr][Oo]|[Ff][Ee][Bb][Rr][Ee][Rr][Oo]|[Mm][Aa][Rr][Zz][Oo]|[Aa][Bb][Rr][Ii][Ll]|[Mm][Aa][Yy][Oo]|[Jj][Uu][Nn][Ii][Oo]|[Jj][Uu][Ll][Ii][Oo]|[Aa][Gg][Oo][Ss][Tt][Oo]|[Ss][Ee][Pp][Tt][Ii][Ee][Mm][Bb][Rr][Ee]|[Oo][Cc][Tt][Uu][Bb][Rr][Ee]|[Nn][Oo][Vv][Ii][Ee][Mm][Bb][Rr][Ee]|[Dd][Ii][Cc][Ii][Ee][Mm][Bb][Rr][Ee])',
        r'[A-Z]'
    ],
    'Hay un ! o ? y un punto': [
        'normal',
        r'(\w*[!?]\s*[\.]\w*)'
    ],
    'Hay dos puntos seguidos': [
        'normal',
        r'(\w*[\.]\s*[\.]\w*)'
    ],
    'No abre el signo de pregunta': [
        'complex',
        r'((?<!\¿)[\w\s\,áéíúó]*\?)',
        r'([\w\s\,áéíúó]*\?)'
    ],
    'No cierra el signo de pregunta': [
        'complex',
        r'(\¿[\w\s\,áéíúó]*(?!\?))',
        r'(\¿[\w\s\,áéíúó]*)'
    ],
}

text = ''

try:
    with open('errores.txt', encoding='utf-8') as file:
        for line in file:
            text += line      
except Exception as e:
    print('Error al abrir el archivo: {}'.format(e))

cont = 1

print('\nErrores encontrados:\n')

for RegexPattern, RegexExp in RegexPatterns.items():
    print('{}.- {}:'.format(cont, RegexPattern))
    cont2 = 1
    if RegexExp[0] == 'normal':
        foundErrors = re.findall(RegexExp[1], text)
        for foundError in foundErrors:
            print('\t{}.{}.- {}'.format(cont, cont2, foundError))
            cont2 += 1
    if RegexExp[0] == 'complex':
        foundPosibles = re.findall(RegexExp[1], text)
        foundOposites = re.findall(RegexExp[2], text)
        tempCont = 0
        for posibleError in foundPosibles:
            if posibleError == foundOposites[tempCont]:
                print('\t{}.{}.- {}'.format(cont, cont2, posibleError))
            cont2 += 1
            tempCont += 1
    if RegexExp[0] == 'special':
        foundPosibles = re.findall(RegexExp[1], text)
        for posibleError in foundPosibles:
            if re.findall(RegexExp[2], posibleError) != []:
                print('\t{}.{}.- {}'.format(cont, cont2, posibleError))
                cont2 += 1
    cont += 1
    print('')