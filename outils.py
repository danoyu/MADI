#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import random
# cases dispo prenant en compte les limite 
# pas les murs !!!

# 0 : droite
# 1 : gauche
# 2 : bas
# 3 :haut


# fonction qui considère les trois cases possiblement atteignable lors d'une action
# et qui leur associe 1 si elles sont dans la grille, 0 sinon
# TODO : utiliser is in grid pour simplifier la fonction
def cases_dispo(g,i,j,action):
    cases = np.zeros((3,3))
    #si on va a droite  
    if action == 0 :
        cases = [[i-1, j+1,0], [i,j+1,0], [i+1,j+1,0]]
        if j!=(len(g[0])-1):
            cases[1][2]=1
            if i != 0:
                cases[0][2]=1
            if i != (len(g)-1):
                cases[2][2]=1
    #gauche           
    if action == 1 :
        cases = [[i-1, j-1,0], [i,j-1,0], [i+1,j-1,0]]
        if j!=0:
            cases[1][2]=1
            if i != 0:
                cases[0][2]=1
            if i != (len(g)-1):
                cases[2][2]=1   
    #bas
    if action == 2 :
        cases = [[i+1, j-1,0], [i+1,j,0], [i+1,j+1,0]]
        if i!=(len(g)-1):
            cases[1][2]=1
            if j != 0:
                cases[0][2]=1
            if j != (len(g[0])-1):
                cases[2][2]=1
    #haut
    if action == 3 :
        cases = [[i-1, j-1,0], [i-1,j,0], [i-1,j+1,0]]
        if i!=0:
            cases[1][2]=1
            if j != 0:
                cases[0][2]=1
            if j != (len(g[0])-1):
                cases[2][2]=1           
    return cases

# Fonction qui teste si un point i j est dans la grille g
def is_in_grid(g, i, j):
    if 0<=i and i < len(g) and 0<=j and j < len(g[0]) :
        return True
    else : 
        return False


# Fonction qui renvoie pour une action donnée une matrice indiquand pour chaque case
        # accessible après une action action depuis ij la probabilité d'y arriver effectivement
def probas_action(g,i,j,p,action):
    # on recupère le vecteurs des cases visées : 0 si la case est hors de la grill
    # 1 sinon
    cases = cases_dispo(g,i,j,action)
      
    ## on est dans le cas grille_avec_chiffre
    if (len(g.shape)== 3) :   
        for i,case in enumerate(cases):# pour chaque case
            # si elle est accessible mais que c'est un mur
            if case[2]==1 and g[case[0]][case[1]][0] == 0 :
                case[2] = 0 # on la rend inaccessible
                
    ## on est dans le cas grille simple
    else :
        for i,case in enumerate(cases): # pour chacune case
            # si elle est accessible mais que c'est un mur
            if is_in_grid(g, case[0], case[1]) and g[case[0]][case[1]] == 0 :
                case[2] = 0 # on la rend inaccessible
                
    #si la case du milieu (celle visee est un mur) : toutes les probas sont mises à 0
    if cases[1][2] == 0:
        cases[0][2] = 0
        cases[1][2] = 0
        cases[2][2] = 0
    else :
        if cases[0][2] == 0:
            if cases[2][2] == 0:
                # les cases voisines sont des murs
                cases[1][2] = 1
            # la derniere case est accessible
            else:
                cases[1][2] = (1+p)/2
                cases[2][2] = (1-p)/2
        #premiere case n'est pas un mur
        else:
            if cases[2][2] == 0:
                cases[0][2] = (1-p)/2
                cases[1][2] = (1+p)/2
            # toutes les cases sont accessibles
            else:
                cases[0][2] = (1-p)/2
                cases[1][2] = p
                cases[2][2] = (1-p)/2   
    return cases


# Fonction qui tire une case arrivée selon la case de depart, l'action, l'état et la probabilité
def deplacement_probabiliste(g,i,j,p,action):
    # on récupère les probabilités de chaque case
    cases = probas_action(g,i,j,p,action)
    z = random.uniform(0,1)
    new_i =0
    new_j =0
    if z<cases[0][2] :
        new_i = cases[0][0]
        new_j = cases[0][1]
    elif z<cases[0][2]+cases[1][2]:
        new_i = cases[1][0]
        new_j = cases[1][1]
    else :
        new_i = cases[2][0]
        new_j = cases[2][1]
    return(new_i,new_j)


# Fonction qui a partir d'une sortie delta des PL de la partie trois et d'une 
    # position dans la grille retourne une action tiree aleatoire 
def get_randomized_action(delta,i,j):
    # on récupère les probabilités d'action sur la case
    pb_action = delta[i][j]
    # on tire une action :
    z = random.uniform(0,1)
    if z<pb_action[0]:
        action = 0
    elif z < pb_action[0]+pb_action[1]:
        action = 1
    elif z < pb_action[0]+pb_action[1]+ pb_action[2]:
        action = 2
    else :
        action = 3
    return(action)


# Méthode qui prend en entrée une matrice de politique et qui en ressort
# un affichage simplifié de cette politique
def from_action_to_dir(matrix, g):
    result = np.zeros((len(matrix), len(matrix[0])), dtype=str)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (len(g.shape)== 3 and g[i][j][0] == 0) or (len(g.shape)== 2 and g[i][j] == 0):   # on est dans le cas de la grille avec chiffres
                # selon la grille
                result[i][j]='x'
            else :
                if matrix[i][j]==0:
                    result[i][j]= ">"
                elif matrix[i][j]==1:
                    result[i][j]= "<"
                elif matrix[i][j]==2:
                    result[i][j]= "v"    
                else :
                    result[i][j]= "^"
    return result

#prend en compte l'incertain
def sum_p_v(g,val_etats,i,j,p,action):
    somme = 0
    cases = probas_action(g,i,j,p,action)
    for i,c in enumerate(cases): 
        if c[2] != 0: # on teste si la case est accessible (permet de ne pas
            # avoir de problème avec les cases exterieurs)
            somme += c[2] * val_etats[c[0]][c[1]]
    return somme

def mean_experienced_cost(d,g,p,nbr_experience):
    mean_cost =[0]*5
    for i in range(nbr_experience):
        ## pour chacune des nbr_experiences
        i = 0
        j = 0
        cost = [0]*5
        while not (i == len(g)-1 and j == len(g[0])-1)  :
            # tant qu'on est pas à la dernière case et que la destination appartient à la grille
            direction = d[i][j]
            i,j = deplacement_probabiliste(g,i,j,p,direction)
            #print(str(i)+" "+str(j))
            if not is_in_grid(g,i,j): # si la destination n'est pas dans la grille
                break
            if (i == len(g)-1 and j == len(g[0])-1)  :
                break
            cost[g[i][j][0]]+=g[i][j][1]
        #cout total    
        cost[0]=cost[1]+cost[2]+cost[3]+cost[4]
        #print(cost)
        mean_cost = [sum(x) for x in zip(cost, mean_cost)]
        #print(mean_cost)
    mean_cost = [x/nbr_experience for x in cost] 
    return mean_cost
     
def mean_experienced_cost_p3(d,g,p,nbr_experience):
    mean_cost =[0]*5
    for i in range(nbr_experience):
        ## pour chacune des nbr_experiences
        i = 0
        j = 0
        cost = [0]*5
        while not (i == len(g)-1 and j == len(g[0])-1)  :
            # tant qu'on est pas à la dernière case et que la destination appartient à la grille
            direction = get_randomized_action(d,i,j)
            i,j = deplacement_probabiliste(g,i,j,p,direction)
            #print(str(i)+" "+str(j))
            if not is_in_grid(g,i,j): # si la destination n'est pas dans la grille
                break
            if (i == len(g)-1 and j == len(g[0])-1)  :
                break
            cost[g[i][j][0]]+=g[i][j][1]
        #cout total    
        cost[0]=cost[1]+cost[2]+cost[3]+cost[4]
        #print(cost)
        mean_cost = [sum(x) for x in zip(cost, mean_cost)]
        #print(mean_cost)
    mean_cost = [x/nbr_experience for x in cost] 
    return mean_cost
     


