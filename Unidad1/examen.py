
"""
Autor: Hector Rodriguez
"""

"""
Este codigo lee el archivo ips.txt (debe estar al mismo nivel de carpeta que este archivo) 
y muestra en pantalla las direcciones ip validas segun el siguiente formato:
    aaa.aaa.aaa.aaa
donde a es un digito del 0 al 9 y aaa debe ser menor que 255 y mayor a 0
"""

try:
    with open('ips.txt', encoding='utf-8') as file:
        for line in file:
            words = line.split(' ')
            for word in words:
                if len(word) == 0:
                    continue
                if word[len(word) - 1] == '\n':
                    word = word[0:len(word) - 1]
                parts = word.split('.')
                if len(parts) == 4:
                    flag = False
                    for part in parts:
                        try:
                            if int(part) < 0 or int(part) > 255:
                                flag = True
                        except:
                            flag = True
                    if not flag:
                        print('{}.{}.{}.{}'.format(parts[0], parts[1], parts[2], parts[3]))
                            
except Exception as e:
    print('Error al abrir el archivo: {}'.format(e))