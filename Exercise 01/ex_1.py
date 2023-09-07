import random
from os import system

def adivina(intentos):
    system("clear")

    # RANGO
    min_num = 0
    max_num = 100

    num_aleatorio  = random.randint(min_num, max_num)
    
    for i in range(intentos):
        num = int(input("Ingrese un número entre {} y {}: ".format(min_num, max_num)))
    
        if num == num_aleatorio:
            print("\nFelicitaciones. Ha adivinado el número!")
            print("Se utilizaron " + str(i+1) + " intentos.")
            print("El número es: " + str(num_aleatorio) + "\n")
            break

        intentos -= 1

        if intentos == 0:
            print("\nSe han acabado los intentos!\n")
       
adivina(10)
