
"""
Autor: Hector Rodriguez
"""

"""
Este codigo lee el archivo doc.txt (debe estar al mismo nivel de carpeta que este archivo) 
y muestra en consola para cada linea del documento que tipo de elemento o a que categoría pertenece.
Estas son mis condiciones:
 1.- Entero: Números de 0-9
 2.- Flotante: Números de 0-9 seguido de un . y más números de 0-9
 3.- Variable: Conjunto de letras de la A-Z mayúsculas y minúsculas, _ y dígitos de 0-9 que no debe iniciar con 0-9
 4.- String: Cadena de carateres que inicia y cierra con "
 5.- Aritmética: Expresión con entero, flotante o variable seguida de un * + - / ^ y luego otro entero, flotante o variable
    no pueden haber dos * + - / ^ juntos o terminar la expresión con * + - / ^
 6.- Relacional: Expresión con entero, flotante o variable seguida de un < > y un posible = o un != o == y luego otro entero, flotante o variable
    no pueden haber dos < > y un posible = o un != o == juntos o terminar la expresión con < > y un posible = o un != o ==
"""

import re

# Regex necesarias
RegexPatterns = {
    'entero': r'^[\-|\+]?\d+$',
    'flotante': r'^[\-|\+]?\d+\.\d+$',
    'variable': r'^[a-zA-Z_]\w{0,29}$',
    'string': r'^\"[^\"]*\"$',
    'aritmetica': r'^(\d+|\d+\.\d+|[a-zA-Z_]\w{0,29})([\*\/\+\-\^](\d+|\d+\.\d+|[a-zA-Z_]\w{0,29}))+$',
    'relacional': r'^(\d+|\d+\.\d+|[a-zA-Z_]\w{0,29})(([\<\>]\=?|[\!\=]=)(\d+|\d+\.\d+|[a-zA-Z_]\w{0,29}))+$'
}

try:
    with open('doc.txt', encoding='utf-8') as file:
        for line in file:
            flag = False
            for regexName, regex in RegexPatterns.items():
                foundRegex = re.findall(regex, line)
                if line != '\n':
                    if foundRegex != []:
                        flag = True
                        print('{}: es {}'.format(line[0:len(line)-1], regexName))
                        break
            if not flag and line != '\n':
                print('{}: no lo conozco'.format(line[0:len(line)-1]))
                            
except Exception as e:
    print('Error al abrir el archivo: {}'.format(e))