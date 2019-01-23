#Alumno: Héctor

#Lo hice en Python3.6


frase = input("Ingrese la frase: ")
vocales = ['a', 'e', 'i', 'o', 'u']
vocalesEncontradas = {}

print()

if len(frase) > 200:
	print("Esa frase es mayor a 200 carácteres")

elif len(frase) == 0:
	print("Favor de ingresar una frase")

else:
	for caracter in frase:
		if caracter in vocales:
			if caracter in vocalesEncontradas:
				vocalesEncontradas[caracter] = vocalesEncontradas[caracter] + 1
			else: 
				vocalesEncontradas[caracter] = 1

for vocal in vocalesEncontradas:
	print(vocal, "aparecio", vocalesEncontradas[vocal], "veces")