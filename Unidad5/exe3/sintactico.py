import pickle
import re

fileName = 'program1.hd'                       # Code file

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

# print('{}{}Normal turing model{}'.format(
#     textColors['bold'], textColors['blue'], textColors['reset']
# ))
# print(turing)


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

turingReservedCheck = {}

with open('reservedCheck.tr') as file:
    for line in file:
        if line != '' and line != '\n':
            comment = re.split('#', line)
            if comment[0] != '':
                thing = comment[0]
                thing = re.split(r'\s+', thing)
                if thing[0] in turingReservedCheck:
                    turingReservedCheck[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])
                else:
                    turingReservedCheck[thing[0]] = []
                    turingReservedCheck[thing[0]].append([
                        thing[1], thing[2], thing[3], thing[4]
                    ])

# print()
# print('{}{}Reserved CHECK turing model{}'.format(
#     textColors['bold'], textColors['blue'], textColors['reset']
# ))
# print(turingReservedCheck)
# print()
# print('{}{}---------------------------------------------------------{}'.format(
#     textColors['bold'], textColors['blue'], textColors['reset']
# ))
# print()


# Exit states from reserved.tr

exitReserved = [
    'funcParamsInit',
    'errorFNClose',
    'errorFInvCall',
    'errorFInvCall2',
    'functionNoParams',
    'reservedNotStr',
    'errorStrOp',
    'errorInvOp'
]

# Errors

errors = {
    'errorSQ': 'You forgot to close a single quote',
    'errorDQ': 'You forgot to close a double quote',
    'errorStrOp': 'Invalid operation with string',
    'errorFNClose': 'You forgot to close the parameter declaration',
    'errorInvOp': 'Invalid usage of operator',
    'errorInvVarDec': 'Invalid variable declaration',
    'errorInvVarDecUn': 'Unknown thing assign to variable',
    'errorInvOp': 'Unknown operator',
    'errorFInvCall': 'Invalid function call, missing ( params )',
    'errorFInvCall2': 'Invalid function call, no params requiered',
    'errorFInvCall3': 'Invalid function call',
}

# Success states from syntax.tr

successStates = [
    'reading'
]

# Functions

functions = [
    'print',
    'readLn'
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
            # print('Added {} instruction'.format(typeIns))
            # print('{} -> {}'.format(typeIns, actualInstructionParts))
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
programmerError = True              # Error generated by this program

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
                        # print('Add instruction')
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

            # Check if state is error state
            if actState in errors:
                # Load codes lines for debugging line in error
                codeLines = []
                with open(fileName, encoding='utf-8') as file:
                    for line in file:
                        codeLines.append(line)

                print('\n{}{}{} in line {}{}{} :  {}{}{}'.format(
                    textColors['bold'], textColors['red'], errors[actState], 
                    textColors['orange'], lexic[currentL][4] + 1, textColors['red'],
                    textColors['orange'], codeLines[lexic[currentL][4]], 
                    textColors['reset']
                ))
                programmerError = False
                goodLexic = False
                break

            # We found a reserved word, change to reserved states
            if actState == 'gettingReserved':
                actState = 'init'
                typeState = 'reserved'
            elif actState == 'gettingReservedNotStr':
                actState = 'notStr'
                typeState = 'reservedCheck'
            else:    
                print('\n{}{}The state is not in turing{}'.format(
                    textColors['bold'], textColors['red'], textColors['reset']
                ))
                goodLexic = False
                break

    # If we are in reserved states
    elif typeState == 'reserved' or typeState == 'reservedCheck':
        turingReservedToCheck = turingReserved
        if typeState == 'reservedCheck':
            turingReservedToCheck = turingReservedCheck

        if actState in turingReservedToCheck:
            flag = False
            for path in turingReservedToCheck[actState]:
                if re.search(re.compile(path[0]), lexic[currentL][1]) != None:
                    # print('Got with {}!'.format(path))
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
                print('\n{}{}You have syntax errors:{}'.format(
                    textColors['bold'], textColors['red'], textColors['reset']
                ))
                if typeState == 'reserved':
                    print('\n{}{}Not a valid reserved path for {} in {}{}'.format(
                        textColors['bold'], textColors['red'], 
                        lexic[currentL], actState,
                        textColors['reset']
                    ))
                else:
                    print('\n{}{}Not a valid CHECK reserved path for {} in {}{}'.format(
                        textColors['bold'], textColors['red'], 
                        lexic[currentL], actState,
                        textColors['reset']
                    ))
                goodLexic = False
                break
        else:
            if typeState == 'reserved':
                print('\n{}{}The reserved state is not in turing{}'.format(
                    textColors['bold'], textColors['red'], textColors['reset']
                ))
            else:
                print('\n{}{}The reserved CHECK state is not in turing{}'.format(
                    textColors['bold'], textColors['red'], textColors['reset']
                ))
            goodLexic = False
            break



if goodLexic and actState in successStates:
    
    # Show instructions

    print('\n{}{}Intrucciones: {}\n'.format(
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
    
    print('\n{}{}Nice! No syntax errors{}'.format(
        textColors['bold'], textColors['green'], textColors['reset']
    ))

else:
    if programmerError:
        print('{}{}Oh no... My bad...{}'.format(
            textColors['bold'], textColors['red'], textColors['reset']
        ))

