import re

fileName = 'RestaConCarryPositivos.txt'

datas = []
turing = {}

with open(fileName) as file:
    for line in file:
        if line[0] != ';' and line != '\n':
            commentIndex = line.find(';')
            if (commentIndex != -1):
                line = line[0:commentIndex]
            if (line[len(line) - 1] == '\n'):
                line = line[0:len(line) - 1]
            datas.append(line)
        else:
            continue

for data in datas:
    spD = re.split(r'\s', data) # Splitted Data
    if not spD[0] in turing:
        turing[spD[0]] = []
        turing[spD[0]].append(spD[1:5])
    else:
        turing[spD[0]].append(spD[1:5])

cState = '0' # Current state 
initialInput = '1111-111='
apu = 1

auxStr = ' ' + initialInput + ' '
flag = False


import os           
os.system('color')          # Activate color mode in terminal

import color
colors = color.colors       # Create colors object

import time                 # For slowing the while function


while True:

    if apu >= len(auxStr):
        auxStr += ' '
    
    if apu < 0:
        auxStr = ' ' + auxStr
        apu = 0

    print('', end='\r')
    print('', end='\t')
    for n in range(len(auxStr)):
        
        if n == apu:
            print(colors.bg.cyan + colors.fg.black + auxStr[n] + colors.reset, end='')
        else:
            print(auxStr[n], end='')

    if "halt" in cState:
        break

    flag = False
    # print('\nVoy en el char: {} en el index: {}, estado = {}'.format(auxStr[apu], apu, cState))

    for way in turing[cState]:

        # print('Voy en way: {}'.format(way))

        if way[0] == '*':                   # Si buscamos un *

            # print('Voy a buscar un: {} estando en {}'.format(way[0], auxStr[apu]))
            
            # Cambiar el valor
            auxL = list(auxStr)
            if way[1] == '_':
                auxL[apu] = ' '
            elif way[1] == '*':
                auxL[apu] = auxL[apu]
            else:
                auxL[apu] = way[1]
            auxStr = ''.join(auxL)

            # Mover d, l, *
            if way[2] == 'r':
                apu += 1
            elif way[2] == 'l':
                apu -= 1

            # Cambiar estado
            cState = way[3]

            flag = True
            break                       # Salimos del for, no seguimos buscando en mas ways
                


        else:                               # Si buscamos cualquier otra cosa
            searchFor = ''
            if way[0] == '_':
                searchFor = ' '
            else:
                searchFor = way[0]

            # print('Voy a buscar un: {} estando en {}'.format(searchFor, auxStr[apu]))

            if auxStr[apu] == way[0] or (searchFor == ' ' and auxStr[apu] == ' '):       # Si si coincide con lo que buscamos
                
                # Cambiar el valor
                auxL = list(auxStr)
                if way[1] == '_':
                    auxL[apu] = ' '
                elif way[1] == '*':
                    auxL[apu] = auxL[apu]
                else:
                    auxL[apu] = way[1]
                # print('auxL = {}'.format(auxL))
                auxStr = ''.join(auxL)

                # Mover d, l, *
                if way[2] == 'r':
                    apu += 1
                elif way[2] == 'l':
                    apu -= 1

                # Cambiar estado
                cState = way[3]


                flag = True
                break                       # Salimos del for, no seguimos buscando en mas ways
    
    # print('\n{} --> {}'.format(initialInput, auxStr))

    if not flag:
        print('Woooops, tuve que salir del while')
        break
    
    time.sleep(0.1)        # Wait 0.25 s
