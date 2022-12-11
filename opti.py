from mip import *

def modeleDecoupePapier(largeur, listeBandes, prix_euro_par_metre):
    # creation du modele
    m = Model("papier", sense=MAXIMIZE)
    # MAX WASTE = PLUS PETITE BANDE DE LISTE BANDES
    MAX_WASTE = min(listeBandes)
    PRIX_WASTE = 3

    cuts = []
    waste = []

    def findCuts(liste_bandes, largeur_restante, bande_actuelle):
        if MAX_WASTE > largeur_restante >= 0:
            cuts.append(bande_actuelle)
        elif largeur_restante > 0:
            for i in range(0, len(liste_bandes)):
                findCuts(liste_bandes[i:],
                         largeur_restante - liste_bandes[i],
                         bande_actuelle + [liste_bandes[i]])

    # find the waste for each cuts from cuts
    def findWaste(cuts):
        for cut in cuts:
            waste.append(largeur - sum(cut))

    findCuts(listeBandes, largeur, [])
    findWaste(cuts)

    print("Liste des coupes : " + str(cuts))
    print("Liste des pertes : " + str(waste))

    # create a dictionary that matches a letter to each bande of listeBandes
    dico = {}
    for i in range(0, len(listeBandes)):
        dico[chr(65 + i)] = listeBandes[i]

    print(dico)

    # for each cut, create a variable from the letters of the bandes in the cut matching the largeur of the cut
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
    m.objective = xsum(prix_euro_par_metre[i] * var[i] for i in range(0, len(prix_euro_par_metre))) - sum(waste) * PRIX_WASTE

    # add the constraints
    # maximum paper size = 1000
    m += xsum(var[i] for i in range(0, len(cuts))) <= 1000

    # todo
    # not a single band can represent more than 50% of the total length of the paper

    # Must produce 100 meters more of A band than C band
    m += xsum(var[j] for j in range(0, len(cuts)) if "A" in varname[j]) - xsum(var[j] for j in range(0, len(cuts)) if "C" in varname[j]) >= 100
    # lancement de l'optimisation
    m.optimize()

    if m.status == OptimizationStatus.OPTIMAL:
        # affichage du resultat
        for i in range(0, len(var)):
            print(varname[i] + " = " + str(var[i].x))
        print("Bénéfice total : " + str(m.objective_value))
    else:
        print("No solution")
