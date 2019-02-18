
"""
Programa Diptongos
Autor: Héctor Rodríguez

Este programa permite obtener los
diptongos existentes en un archivo
de texto. Muestra en pantalla el diptongo,
la palabra donde se encuentra y en que
linea del archivo.

Esta version en Python reconocé vocales con
tilde, y diéresis.
"""

vocales = ['a', 'e', 'i', 'o', 'u', 'á', 'é', 'í', 'ó', 'ú', 'ö', 'ü']

try:
    with open('parrafo.txt', encoding="utf-8") as file:
        lineNumber = 1
        for line in file:
            words = line.split(" ")
            for word in words:
                vocalAntes = ''
                for char in word:
                    if char in vocales:
                        if not vocalAntes == '' and not vocalAntes == char:
                            print('\nPalabra:', word)
                            print('Diptongo: {}{}'.format(vocalAntes, char))
                            print('En la linea', lineNumber)
                        vocalAntes = char
                    else:
                        vocalAntes = ''
            lineNumber += 1
except Exception as e:
    print("Error al abrir el archivo")