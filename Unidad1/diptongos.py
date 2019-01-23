
vocales = ['a', 'e', 'i', 'o', 'u']

with open('parrafo.txt', encoding="utf-8") as file:
    lineNumber = 1
    for line in file:
        words = line.split(" ")
        for word in words:
            if word[len(word) - 1] == '\n':
                word = word[0:len(word) - 2]
            vocalAntes = ''
            for char in word:
                if char in vocales:
                    if not vocalAntes == '' and not vocalAntes == char:
                        print()
                        print('Palabra:', word)
                        print('Diptongo: {}{}'.format(vocalAntes, char))
                        print('En la linea', lineNumber)
                    vocalAntes = char
                else:
                    vocalAntes = ''
        lineNumber += 1