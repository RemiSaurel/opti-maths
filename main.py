from opti import *


def printModulo(numero):
    '''
    Affiche les modulos de 3 à 7 d'un numéro étudiant
    :param numero: numéro étudiant
    :return: None
    '''
    # Il nous fallait les modulos de 3 à 7, à changer si besoin
    for i in range(3, 8):
        print("Modulo " + str(i) + " : " + str(numero % i))


if __name__ == '__main__':
    # METTRE LES NUMEROS ETUDIANTS ICI

    # NUM_REMI = 12345678
    # NUM_ADAM = 87654321

    # FONCTION POUR AFFICHER VOS MODULOS FACILEMENT
    # printModulo(NUM_REMI)
    # printModulo(NUM_ADAM)

    # MODULO 3 à 7 POUR RÉMI :
    # ...............
    # MODULO 3 à 7 POUR ADAM :
    # ...............

    # REMI
    print("REMI : ")
    modeleDecoupePapierRemi(255, [85, 80, 75, 70, 60], [15, 14, 13, 16, 14], 3)

    print("=====================================")

    # ADAM
    print("ADAM")
    modeleDecoupePapierAdam(283, [110, 92, 80, 74, 70, 65], [15, 12, 10, 9, 7, 3], 2)
