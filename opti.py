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
    m.objective = xsum(prix_euro_par_metre[i] * var[i] for i in range(0, len(prix_euro_par_metre))) - sum(waste) * PRIX_WASTE

    #############
    # CONSTRAINTS
    #############

    # get total produced
    total_produced = 0
    for i in range(0, len(cuts)):
        total_produced += len(cuts[i]) * var[i]

    # maximum paper size = 1000
    m += total_produced <= 1000

    # Not a single band can represent more than 50% of the total length of the paper
    for i in range(0, len(listeBandes)):
        letter = chr(65 + i)
        # For A, it will be:
        # 3AAA + 2AAB + 2AAC + 2AAD + 2AAE + ABB + ABC + ABD + ABE + ACC + ACD + ACE + ADD + ADE + AEE
        m += xsum(var[j] * varname[j].count(letter) for j in range(0, len(cuts)) if letter in varname[j]) <= 0.5 * total_produced
    
    # Must produce 100 meters more of A band than C band
    # Example :
    # 3AAA + 2AAB + AEE >= (BCD + 3CCC) + 100
    m += xsum(var[j] * varname[j].count('A') for j in range(0, len(cuts)) if 'A' in varname[j]) >= xsum(var[j] * varname[j].count('C') for j in range(0, len(cuts)) if 'C' in varname[j]) + 100

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
    m.objective = xsum(prix_euro_par_metre[i] * var[i] for i in range(0, len(prix_euro_par_metre))) - sum(
        waste) * PRIX_WASTE

    #############
    # CONSTRAINTS
    #############
    # get total produced
    total_produced = 0
    for i in range(0, len(cuts)):
        total_produced += len(cuts[i]) * var[i]

    # maximum paper size = 1000
    m += total_produced <= 1000

    # Not a single band can represent more than 50% of the total length of the paper
    for i in range(0, len(listeBandes)):
        letter = chr(65 + i)
        # For A, it will be:
        # 3AAA + 2AAB + 2AAC + 2AAD + 2AAE + ABB + ABC + ABD + ABE + ACC + ACD + ACE + ADD + ADE + AEE
        m += xsum(var[j] * varname[j].count(letter) for j in range(0, len(cuts)) if
                  letter in varname[j]) <= 0.5 * total_produced

    # Total of band A + band C must be less than 750
    # Example :
    # 3AAA + 4AACC + AEE + 0BDE + 2CC + 3CCC <= 750
    total_A = xsum(var[j] * varname[j].count("A") for j in range(0, len(cuts)))
    total_C = xsum(var[j] * varname[j].count("C") for j in range(0, len(cuts)))
    print(f'Total A + C : {total_A + total_C}')
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