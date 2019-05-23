import re
import pickle
import sys
import os

"""

Autor: Héctor Daniel Rodríguez Feregrino

Este programa toma un archivo fuente y detecta los componentes
léxicos para mostarlos y guardar la lista resultante en un archivo
.data

Para ejecutar el programa es necesario escribir:
>> python lexico.py archivoFuente.hd 

"""

# All variables

if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    sys.exit('Missing filename arg...')

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

reservedWordsPath = os.path.join(application_path, 'reservedWords.txt')
automataPath = os.path.join(application_path, 'automata.tr')

lastState = ''
actualState = 'searching'
aL = 0                                      # Actual Line
aR = 0                                      # Actual Row
initialChar = 0                             # Found thing init char
finalChar = 0                               # Found thins last char
turing = {}                                 # Main turing
actions = {}                                # Actions to do
codeLines = []                              # Code splitted into lines
bigError = False                            # Flag for big errors


# Save the reserved words in reservedWords list
reservedWords = []

with open(reservedWordsPath) as file:
    for line in file:
        words = re.split(r'\s+', line)
        for word in words:
            if word != '':
                reservedWords.append(word)


# Get turing using automata.turing file model
datas = []

with open(automataPath) as file:
    for line in file:
        if line[0] != '#' and line != '\n':
            commentIndex = line.find('#')
            if (commentIndex != -1):
                line = line[0:commentIndex]
            if (line[len(line) - 1] == '\n'):
                line = line[0:len(line) - 1]
            datas.append(line)
        else:
            continue

for data in datas:
    spD = re.split(r'\s+', data)            # Splitted Data
    if not spD[0] in turing:
        turing[spD[0]] = []
        turing[spD[0]].append(spD[1:5])
    else:
        turing[spD[0]].append(spD[1:5])


# Create special actions for some states in turing

# Este metodo checa si lo obtenido es variable o palabra reservada
# y lo almacena con su respectivo token
def isReserved():
    global actualState
    codeLine = codeLines[aL]
    thing = codeLine[initialChar:finalChar + 1]
    thing = re.split(r'\s+', thing)[0]
    # print('Estoy viendo si {} es palabra reservada'.format(thing))
    name = ''
    if thing in reservedWords:
        name = 'ReservedWord'
    else:
        name = 'Variable'
    lexic.append([
        name, thing, 
        initialChar, initialChar + len(thing),
        aL
    ])
    actualState = 'searching'

# Este método almacena el token de los componente que consisten
# en un solo caracter
def getOneChar():
    global actualState
    global bigError
    codeLine = codeLines[aL]
    thing = codeLine[initialChar:finalChar + 1]
    if actualState != 'foundBreakLine':
        thing = re.split(r'\s+', thing)[0]
    else:
        thing = '\n'
    # print('Estoy viendo si {} es palabra reservada'.format(thing))
    name = ''
    if actualState == 'foundOperator':
        if thing == '+':
            name = 'PlusOperator'
        elif thing == '-':
            name = 'MinusOperator'
        elif thing == '*':
            name = 'MultiOperator'
        elif thing == '/':
            name = 'DivOperator'
        elif thing == '^':
            name = 'PowOperator'
    if actualState == 'foundEqual':
        name = 'EqualSign'
    if actualState == 'foundComa':
        name = 'Coma'
    if actualState == 'foundDoubleQ':
        name = 'DoubleQuote'
    if actualState == 'foundSingleQ':
        name = 'SingleQuote'
    if actualState == 'foundOpPara':
        name = 'OpParenthesis'
    if actualState == 'foundCloPara':
        name = 'CloParenthesis'
    if actualState == 'foundOpBrace':
        name = 'OpBrace'
    if actualState == 'foundCloBrace':
        name = 'CloBrace'
    if actualState == 'foundLowChar':
        name = 'LowerThan'
    if actualState == 'foundGreChar':
        name = 'GreaterThan'
    if actualState == 'foundDiffChar':
        name = 'Different'
    if actualState == 'foundBreakLine':
        name = 'BreakLine'

    if name != '':
        lexic.append([
            name, thing, 
            initialChar, initialChar + len(thing),
            aL
        ])
        actualState = 'searching'
    else:
        bigError = True

# Este método almacena todos aquellos tokens de longitud
# mayor a 1. Ej: variables, enteros, flotantes y los errores
def putContent():
    global actualState
    global bigError
    codeLine = codeLines[aL]
    thing = codeLine[initialChar:finalChar + 1]
    thing = re.split(r'\s+', thing)[0]
    # print('Estoy viendo si {} es palabra reservada'.format(thing))
    name = ''

    # print('Entre aquí en {} y {}'.format(actualState, thing))

    if actualState == 'foundVar':
        name = 'Variable'
    if actualState == 'foundInteger':
        name = 'Integer'
    if actualState == 'foundFloat':
        name = 'Float'
    if actualState == 'foundNothing':
        name = 'NotValid'

    if name != '':
        lexic.append([
            name, thing, 
            initialChar, initialChar + len(thing),
            aL
        ])
        actualState = 'searching'
    else:
        bigError = True

# Este método almacena los strings de comilla simple y comilla doble
def getString():
    global actualState
    global bigError
    codeLine = codeLines[aL]
    thing = codeLine[initialChar:finalChar + 1]
    
    # print('Estoy viendo si {} es string'.format(thing))
    
    name = ''

    # print('Entre aquí en {} y {}'.format(actualState, thing))

    if actualState == 'foundStringSQ':
        name = 'StringSQ'
    if actualState == 'foundStringDQ':
        name = 'StringDQ'

    if name != '':
        lexic.append([
            name, thing, 
            initialChar, initialChar + len(thing),
            aL
        ])
        actualState = 'searching'
    else:
        bigError = True

# Este método salta de linea
def jumpLine():
    global aL
    global aR
    global actualState
    aL += 1
    aR = 0
    actualState = 'searching'


# Con este JSON vemos a que método ir dependiendo del estado
# en el turing
actions = {
    'foundResVar':      [isReserved],

    'foundVar':         [putContent],
    'foundInteger':     [putContent],
    'foundFloat':       [putContent],
    'foundNothing':     [putContent],

    'foundOperator':    [getOneChar],
    'foundComa':        [getOneChar],
    'foundEqual':       [getOneChar],
    'foundDoubleQ':     [getOneChar],
    'foundSingleQ':     [getOneChar],
    'foundOpPara':      [getOneChar],
    'foundCloPara':     [getOneChar],
    'foundOpBrace':     [getOneChar],
    'foundCloBrace':    [getOneChar],
    'foundLowChar':     [getOneChar],
    'foundGreChar':     [getOneChar],
    'foundDiffChar':    [getOneChar],

    'foundStringSQ':    [getString],
    'foundStringDQ':    [getString],

    'foundBreakLine':   [getOneChar],

    'foundComment':     [jumpLine]
}






# Open code file and save in code variable

code = ''
with open(fileName, encoding='utf-8') as file:
    for line in file:
        code += line


# Save in codeLines list all the lines in the code
# codeLines = [ line + ' ' for line in re.split(r'\n', code) ]
codeLines = [ line + '\n' for line in re.split(r'\n', code) ]
codeLinesCopy = codeLines


# Lexic results table

lexic = []





# Actual code :P

activeActualChar = False
posibleGoodLexic = False

while True:

    if codeLines[aL] == '\n':
        aL += 1

    # Validate pointer
    pointerFlag = True
    while pointerFlag:
        pointerFlag = False
        if aR < 0:                              # If we reach row limit left
    #        print('aR({}) < 0'.format(aR))
            aL -= 1
            aR = len(codeLines[aL]) - 1
            pointerFlag = True
            activeActualChar = False
        if aR >= len(codeLines[aL]):            # If we reach row limit right
    #        print('aR({}) >= {}'.format(aR, len(codeLines[aL])))
            aL += 1
            aR = 0
            pointerFlag = True
            activeActualChar = False
        if aL < 0:                              # If point line is < 0
            # print('The point line is lower than 0...')
            pointerFlag = True
            break
        if aL >= len(codeLines):                # If point line if greater than codeLines
            # print('The point line exceded code lines...')
            aL = aL - 1
            actualState = 'foundBreakLine'
            for action in actions[actualState]:
                action()
            posibleGoodLexic = True
            pointerFlag = True
            break

    #    print('aL: {} - aR: {}'.format(aL, aR))
    
    if pointerFlag:
        break

    codeLine = codeLines[aL]            # Code line we are evaluating

    # print('Linea: {}'.format([codeLine]))
    # print('Estado: {}'.format(actualState))
    # print('Caracter: {}'.format(codeLine[aR]))
    
    if actualState in turing:
        flag = False

        for way in turing[actualState]:
            foundMatch = re.findall(re.compile(way[0]), codeLine[aR])
            # print(foundMatch)
            if foundMatch != []:
                # print('Encontre: {} con {}'.format(foundMatch, way[0]))
                lastState = actualState     # Change last state
                actualState = way[3]        # Change actual state
                flag = True                 # Set flag
                # Check if data started
                if actualState != 'searching' and not activeActualChar:
                    # print('Empiezo a contar chars desde {}'.format(
                    #     aR
                    # ))
                    initialChar = aR
                    activeActualChar = True
                # Change char
                if way[1] == '_':
                    codeLine[aR] = ' '
                elif way[1] != '*':
                    codeLine[aR] = way[1]
                # Move pointer
                if way[2] == 'r':
                    aR += 1
                elif way[2] == 'l':
                    aR -= 1
                break

        if not flag:
            print('No se encontró una way viable...')
            break
                
    else:
        finalChar = aR - 1
        if actualState in actions:
            for action in actions[actualState]:
                action()
            activeActualChar = False
        else:
            print('No hay action para {}'.format(actualState))
            break
    
    if bigError:
        print('Ocurrió algo grave :(')
        break

    # print()


correctLexic = True


# Mostrar lexico encontrado

textColors = {
    'reset': '\033[0m',
    'green': '\033[32m',
    'red': '\033[31m',
    'yellow': '\033[93m',
    'cyan': '\033[36m',
    'orange': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'pink': '\033[95m',
    'bold': '\033[01m',
    'underline': '\033[04m',
}

import os           
os.system('color')          # Activate color mode in terminal

print()
print()
print(textColors['bold'] + textColors['underline'] + textColors['green'] +
    'Lexico encontrado:\n' + textColors['reset'])
for lexicThing in lexic:
    if lexicThing[0] != 'NotValid':
        print('{}{}{}:\t{}{}{}\nLine: {}, Chars({}, {})\n'.format(
            textColors['orange'], lexicThing[0], textColors['reset'],
            textColors['cyan'], lexicThing[1], textColors['reset'],
            lexicThing[4], lexicThing[2], lexicThing[3]
        ))
    else:
        print('{}{}{}:\t{}{}{}\nLine: {}, Chars({}, {})\n'.format(
            textColors['red'], lexicThing[0], textColors['reset'],
            textColors['yellow'] + textColors['underline'], lexicThing[1], textColors['reset'],
            lexicThing[4], lexicThing[2], lexicThing[3]
        ))
        correctLexic = False


print()

if posibleGoodLexic and correctLexic:

    print(textColors['bold'] + textColors['green'] + 
        '¡Excelente! No hay errores de léxico' + textColors['reset'])

else:
    print(textColors['bold'] + textColors['red'] + 
        '¡Oh no...! Tienes errores de léxico' + textColors['reset'])


# Save content into file

file = open('lexicAnalisis.data', 'wb')
pickle.dump(lexic, file)
file.close()


# Print all code: print('\n'.join(codeLines))