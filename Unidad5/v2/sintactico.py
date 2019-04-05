import pickle
import re

# Load data from lexico

file = open('lexicAnalisis.data', 'rb')
lexic = pickle.load(file)

# Colors for terminal

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


# Normal states turing model

turing = {}

with open('syntax.tr') as file:
    for line in file:
        if line != '' and line != '\n':
            comment = re.split('#', line)
            if comment[0] != '':
                thing = comment[0]
                thing = re.split(r'\s+', thing)
                if thing[0] in turing:
                    turing[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])
                else:
                    turing[thing[0]] = []
                    turing[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])

print('{}{}Normal turing model{}'.format(
    textColors['bold'], textColors['blue'], textColors['reset']
))
print(turing)


# Reserved states turing

turingReserved = {}

with open('reserved.tr') as file:
    for line in file:
        if line != '' and line != '\n':
            comment = re.split('#', line)
            if comment[0] != '':
                thing = comment[0]
                thing = re.split(r'\s+', thing)
                if thing[0] in turingReserved:
                    turingReserved[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])
                else:
                    turingReserved[thing[0]] = []
                    turingReserved[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])

print()
print('{}{}Reserved turing model{}'.format(
    textColors['bold'], textColors['blue'], textColors['reset']
))
print(turingReserved)
print()
print('{}{}---------------------------------------------------------{}'.format(
    textColors['bold'], textColors['blue'], textColors['reset']
))
print()


# Exit states from reserved.tr

exitReserved = [
    'funcParamsInit'
]

# Success states from syntax.tr

successStates = [
    'reading'
]

# Functions

functions = [
    'print'
]


# Instructions

def typesOfIns(instruction):
    returnThing = ''
    if instruction[0] == 'Variable':
        returnThing = 'variableDeclaration'
    if instruction[0] == 'ReservedWord':
        if instruction[1] in functions:
            returnThing = 'function'
    return returnThing


instructions = []

def addInstruction():
    if actualInstructionParts != []:
        typeIns = typesOfIns(actualInstructionParts[0])
        if typeIns != '':
            instructions.append([
                typeIns, actualInstructionParts
            ])
            print('Added {} instruction'.format(typeIns))
            print('{} -> {}'.format(typeIns, actualInstructionParts))
        else:
            print('Not added {} instruction'.format(typeIns))


currentL = 0                # Current lexic index that is on analisis
actState = 'reading'        # Current state

# We can have two different types of states:
#
#   1.- Normal: Meaning that we are comparing types of lexic we found. 
#       Here we use syntax.tr (turing)
#
#   2.- Reserved: Meaning that we are comparing content of reserved
#       words. Example: 
#           Type of lexic: ReservedWord
#           Content of lexic: print
#       Here we use reserved.tr (turingReserved)

typeState = 'normal'
goodLexic = True

actualInstructionParts = []

while True:

    # Check if we reach the limits of lexic data
    if currentL >= len(lexic):
        break
    if currentL < 0:
        print('{}{}Woooops! Negative lexic index? Whaaaaaaat?{}'.format(
            textColors['bold'], textColors['red'], textColors['reset']
        ))
        goodLexic = False
        break



    print('actState: {}'.format(actState))
    print('currentLexic: {}'.format(lexic[currentL]))

    # If we are in normal states
    if typeState == 'normal':
        if actState in turing:
            flag = False
            for path in turing[actState]:
                if path[0] == lexic[currentL][0]  or path[0] == '*':
                    print('Got with {}'.format(path))

                    # Add instruction
                    if lexic[currentL][0] == 'BreakLine' and path[3] == 'reading':
                        print('Add instruction')
                        addInstruction()
                        actualInstructionParts = []

                    if lexic[currentL][0] != 'BreakLine':
                        actualInstructionParts.append(lexic[currentL])

                    if path[2] == 'r':
                        currentL += 1
                    if path[2] == 'l':
                        currentL -= 1

                    actState = path[3]
                    flag = True
                    break
            if not flag:
                print('\n{}{}Not a valid path for {} in {}{}'.format(
                    textColors['bold'], textColors['red'], 
                    lexic[currentL], actState,
                    textColors['reset']
                ))
                goodLexic = False
                break
        else:
            # We found a reserved word, change to reserved states
            if actState == 'gettingReserved':
                actState = 'init'
                typeState = 'reserved'
            else:    
                print('\n{}{}The state is not in turing{}'.format(
                    textColors['bold'], textColors['red'], textColors['reset']
                ))
                goodLexic = False
                break

    # If we are in reserved states
    elif typeState == 'reserved':
        if actState in turingReserved:
            flag = False
            for path in turingReserved[actState]:
                if path[0] == lexic[currentL][1] or path[0] == '*':
                    print('Got with {}!'.format(path))

                    if path[2] == 'r':
                        currentL += 1
                    if path[2] == 'l':
                        currentL -= 1
                    actState = path[3]
                    flag = True

                    # Check if exit reserved
                    if actState in exitReserved:
                        typeState = 'normal'

                    break
            if not flag:
                print('\n{}{}Not a valid reserved path for {} in {}{}'.format(
                    textColors['bold'], textColors['red'], 
                    lexic[currentL], actState,
                    textColors['reset']
                ))
                goodLexic = False
                break
        else:
            print('\n{}{}The reserved state is not in turing{}'.format(
                textColors['bold'], textColors['red'], textColors['reset']
            ))
            goodLexic = False
            break
    
    print()




print('\n\n{}{}Intrucciones: {}\n'.format(
    textColors['bold'], textColors['blue'], textColors['reset']
))

for instruction in instructions:
    print('{}{}{}{}: '.format(
        textColors['bold'], textColors['yellow'], 
        instruction[0],
        textColors['reset']
    ))
    
    for ins in instruction[1]:
        print('\t{}: {}'.format(ins[0], ins[1]))

print()
print()

if goodLexic and actState in successStates:
    print('{}{}Nice! No syntax errors{}'.format(
        textColors['bold'], textColors['green'], textColors['reset']
    ))

else:
    print('{}{}Nop... You have syntax errors{}'.format(
        textColors['bold'], textColors['red'], textColors['reset']
    ))

