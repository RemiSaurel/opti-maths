from mip import *

def modeleDecoupePapierRemi(width, listeBandes, prix_euro_par_metre, prix_waste):
    # creation du modele
    m = Model("papier", sense=MAXIMIZE)
    # MAX WASTE = PLUS PETITE BANDE DE LISTE BANDES
    MAX_WASTE = min(listeBandes)
    PRIX_WASTE = prix_waste

    cuts = []
    waste = []

    def findCuts(liste_bandes, width_restante, bande_actuelle):
        if MAX_WASTE > width_restante >= 0:
            cuts.append(bande_actuelle)
        elif width_restante > 0:
            for i in range(0, len(liste_bandes)):
                findCuts(liste_bandes[i:],
                         width_restante - liste_bandes[i],
                         bande_actuelle + [liste_bandes[i]])

    # find the waste for each cuts from cuts
    def findWaste(cuts):
        for cut in cuts:
            waste.append(width - sum(cut))

    findCuts(listeBandes, width, [])
    findWaste(cuts)

    print("Liste des coupes : " + str(cuts))
    print("Liste des pertes : " + str(waste))

    # create a dictionary that matches a letter to each bande of listeBandes
    dico = {}
    for i in range(0, len(listeBandes)):
        dico[chr(65 + i)] = listeBandes[i]

    print("Dico : ")
    print(dico)

    # create a dictionary that matches a letter to each price of prix_euro_par_metre
    dico_prix = {}
    for i in range(0, len(prix_euro_par_metre)):
        dico_prix[chr(65 + i)] = prix_euro_par_metre[i]

    print("Dico prix : ")
    print(dico_prix)

    # for each cut, create a variable from the letters of the bandes in the cut matching the width of the cut
    # each times it is used
    varname = []
    for i in range(0, len(cuts)):
        toAdd = ""
        for j in range(0, len(cuts[i])):
            toAdd += str(list(dico.keys())[list(dico.values()).index(cuts[i][j])])
        varname.append(toAdd)

    print("Varnames : ")
    print(varname)
    var = [m.add_var(v) for v in varname]

    # set the objective
    print(f'Waste : {sum(waste) * PRIX_WASTE}')
    # we want to maximize the profit
    total_bandes_profits = xsum(dico_prix[varname[i][j]] * var[i] for i in range(0, len(varname))
                       for j in range(0, len(varname[i])))
    print(f'Total bandes profits : {total_bandes_profits}')

    # get the total waste cost and add it to the total profit
    total_waste_cost = xsum(waste[i] * PRIX_WASTE * var[i] / 100 for i in range(0, len(varname)))
    print(f'Total waste cost : {total_waste_cost}')
    m.objective = total_bandes_profits - total_waste_cost

    #############
    # CONSTRAINTS
    #############

    # Get total produced
    # Example :
    # total_produced = 3AAA + 3AAB + ... + 4EEEE
    total_produced = 0
    for i in range(0, len(cuts)):
        total_produced += len(cuts[i]) * var[i]

    # Maximum paper size = 1000
    m += total_produced <= 1000

    # Not a single band can represent more than 50% of the total length of the paper
    # Example :
    # Letter : A
    # 3AAA + ABB + ABC + ... <= 0.5 * total_produced
    for i in range(0, len(listeBandes)):
        letter = chr(65 + i)
        m += xsum(var[j] * varname[j].count(letter) for j in range(0, len(cuts)) if letter in varname[j]) <= 0.5 * total_produced
    
    # Must produce 100 meters more of A band than C band
    # Example :
    # 3AAA + 2AAB + AEE >= (BCD + 3CCC) + 100
    total_A = 0
    total_C = 0
    for i in range(0, len(cuts)):
        total_A += var[i] * varname[i].count("A")
        total_C += var[i] * varname[i].count("C")
    # print(f'Total A : {total_A}')
    # print(f'Total C : {total_C}')
    m += total_A >= total_C + 100

    # lancement de l'optimisation
    m.optimize()

    if m.status == OptimizationStatus.OPTIMAL:
        # affichage du resultat
        for i in range(0, len(var)):
            print(varname[i] + " = " + str(var[i].x))
        print("Bénéfice total : " + str(m.objective_value))
    else:
        print("No solution")


def modeleDecoupePapierAdam(width, listeBandes, prix_euro_par_metre, prix_waste):
    # creation du modele
    m = Model("papier", sense=MAXIMIZE)
    # MAX WASTE = PLUS PETITE BANDE DE LISTE BANDES
    MAX_WASTE = min(listeBandes)
    PRIX_WASTE = prix_waste

    cuts = []
    waste = []

    def findCuts(liste_bandes, width_restante, bande_actuelle):
        if MAX_WASTE > width_restante >= 0:
            cuts.append(bande_actuelle)
        elif width_restante > 0:
            for i in range(0, len(liste_bandes)):
                findCuts(liste_bandes[i:],
                         width_restante - liste_bandes[i],
                         bande_actuelle + [liste_bandes[i]])

    # find the waste for each cuts from cuts
    def findWaste(cuts):
        for cut in cuts:
            waste.append(width - sum(cut))

    findCuts(listeBandes, width, [])
    findWaste(cuts)

    print("Liste des coupes : " + str(cuts))
    print("Liste des pertes : " + str(waste))

    # create a dictionary that matches a letter to each bande of listeBandes
    dico = {}
    for i in range(0, len(listeBandes)):
        dico[chr(65 + i)] = listeBandes[i]

    print(dico)

    # create a dictionary that matches a letter to each price of prix_euro_par_metre
    dico_prix = {}
    for i in range(0, len(prix_euro_par_metre)):
        dico_prix[chr(65 + i)] = prix_euro_par_metre[i]

    print("Dico prix : ")
    print(dico_prix)

    # for each cut, create a variable from the letters of the bandes in the cut matching the width of the cut
    # each times it is used
    varname = []
    for i in range(0, len(cuts)):
        toAdd = ""
        for j in range(0, len(cuts[i])):
            toAdd += str(list(dico.keys())[list(dico.values()).index(cuts[i][j])])
        varname.append(toAdd)

    print(varname)
    var = [m.add_var(v) for v in varname]

    # set the objective
    print(f'Waste : {sum(waste) * PRIX_WASTE}')
    # we want to maximize the profit
    total_bandes_profits = xsum(dico_prix[varname[i][j]] * var[i] for i in range(0, len(varname))
                       for j in range(0, len(varname[i])))
    print(f'Total bandes profits : {total_bandes_profits}')

    # get the total waste cost and add it to the total profit
    total_waste_cost = xsum(waste[i] * PRIX_WASTE * var[i] / 100 for i in range(0, len(varname)))
    print(f'Total waste cost : {total_waste_cost}')
    m.objective = total_bandes_profits - total_waste_cost

    #############
    # CONSTRAINTS
    #############

    # Get total produced
    # Example :
    # total_produced = 3AAA + 3AAB + ... + 4EEEE
    total_produced = 0
    for i in range(0, len(cuts)):
        total_produced += len(cuts[i]) * var[i]

    # Maximum paper size = 1000
    m += total_produced <= 1000

    # Not a single band can represent more than 50% of the total length of the paper
    # Example :
    # Letter : A
    # 3AAA + ABB + ABC + ... <= 0.5 * total_produced
    for i in range(0, len(listeBandes)):
        letter = chr(65 + i)
        m += xsum(var[j] * varname[j].count(letter) for j in range(0, len(cuts)) if letter in varname[j]) <= 0.5 * total_produced

    # Total of band A + band C must be less than 750
    # Example :
    # 3AAA + 4AACC + AEE + 0BDE + 2CC + 3CCC <= 750
    total_A = 0
    total_C = 0
    for i in range(0, len(cuts)):
        total_A += var[i] * varname[i].count("A")
        total_C += var[i] * varname[i].count("C")
    # print(f'Total A + C : {total_A + total_C}')
    m += total_A + total_C <= 750

    # lancement de l'optimisation
    m.optimize()

    if m.status == OptimizationStatus.OPTIMAL:
        # affichage du resultat
        for i in range(0, len(var)):
            print(varname[i] + " = " + str(var[i].x))
        print("Bénéfice total : " + str(m.objective_value))
    else:
        print("No solution")