#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 20:23:21 2018

Module pour l'étude de l'impact des différents paramètres des trois algorithmes
sur les performances de résolution. (Question b, c, et d)

@author: Manon
"""
import pandas as pd
import numpy as np
import p2
from matplotlib import pyplot as plt
import grille

# Definition des valeurs par defaut
default_tests = 1
default_nbLignes = 10
default_nbCol = 10
default_p = 1
default_gamma = 0.9
default_epsilon = 0.00001

# Fonction qui étudie l'impact de la taille de l'instance sur les performances des algorithmes. 
# Renvoie un dataframe de données ainsi que le tracé des courbes du nbre d'iteration et du temps d'execution en fonction de la taille
def impact_size(sizes,
                nbr_tests = default_tests,
                p = default_p,
                gamma = default_gamma,
                epsilon = default_epsilon):
    df = pd.DataFrame(columns = ["dimensions", "taille", "iter_val", "iter_pol", "time_val", "time_pol"])
    for i, taille in enumerate(sizes) : 
        print(taille)
        somme1_it = 0
        somme1_t = 0
        somme2_it =0 
        somme2_t =0
        for k in range(nbr_tests):
            g = grille.Grille(taille[0],taille[1],2,0.2,0.2,0.2,0.2,0.2).g
            #print(g)
            #print("run "+str(k+1)+" out of "+str(nbr_tests))
            # iteration de la valeur
            d,v,t, time = p2.iteration_de_la_valeur(g,p,gamma,epsilon)
            somme1_it += t
            somme1_t += time
            # iteration de la politique
            d,v,t, time = p2.iteration_de_la_politique(g,p,gamma,epsilon)
            somme2_it += t
            somme2_t += time
            # ajouter le pl
            line = pd.Series({'dimensions' : taille,
                              'taille' : taille[0]*taille[1],
                              'iter_val' : somme1_it/nbr_tests,
                              'iter_pol': somme2_it/nbr_tests,
                              'time_val': somme1_t/nbr_tests,
                              'time_pol': somme2_t/nbr_tests})
        df = df.append(line, ignore_index=True)
        
    # Affichage des résultats    
    print(df)
    
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.scatter(df.taille, df.iter_val, label = "Iteration de la valeur")
    plt.scatter(df.taille, df.iter_pol, label = "Iteration de la politique")
    #plt.xlabel("Taille de l'instance")
    plt.ylabel("Nombre d'itérations")
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc = 0, borderaxespad = 0.)  
    
    plt.subplot(212, sharex = ax1)
    plt.scatter(df.taille, df.time_val, label = "Iteration de la valeur")
    plt.scatter(df.taille, df.time_pol, label = "Iteration de la valeur")
    plt.xlabel("Taille de l'instance")
    plt.ylabel("Durée d'execution")
        
    plt.show()
    

# Fonction qui étudie l'impact de gamma sur les performances des algorithmes. 
# Renvoie un dataframe de données ainsi que le tracé des courbes du nbre d'iteration et du temps d'execution en fonction de gamma
def impact_gamma(interval_gamma,
                 nbr_tests = default_tests,
                 nbLignes = default_nbLignes,
                 nbCol = default_nbCol,
                 p = default_p,
                 epsilon = default_epsilon):
    df = pd.DataFrame(columns = ["gamma", "iter_val", "iter_pol", "time_val", "time_pol"])
    for gamma in np.arange(0, 1, 0.1):
        print("gamma = "+ str(gamma))
        somme1_it = 0
        somme1_t = 0
        somme2_it =0 
        somme2_t =0
        for k in range(nbr_tests):
            g= np.zeros((nbLignes,nbCol), dtype=np.int)
            p2.colordraw(g,nbLignes,nbCol,0.2,0.2,0.2,0.2,0.2)
            #print(g)
            #print("run "+str(k+1)+" out of "+str(nbr_tests))
            d,v,t, time = p2.iteration_de_la_valeur(g,p,gamma,epsilon)
            somme1_it += t
            somme1_t += time
            d,v,t, time = p2.iteration_de_la_politique(g,p,gamma,epsilon)
            somme2_it += t
            somme2_t += time
            line = pd.Series({'gamma' : gamma,
                              'iter_val' : somme1_it/nbr_tests,
                              'iter_pol': somme2_it/nbr_tests,
                              'time_val': somme1_t/nbr_tests,
                              'time_pol': somme2_t/nbr_tests})
        df = df.append(line, ignore_index=True)
    
    print(df)
    
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.scatter(df.gamma, df.iter_val, label = "Iteration de la valeur")
    plt.scatter(df.gamma, df.iter_pol, label = "Iteration de la politique")
    #plt.xlabel("Taille de l'instance")
    plt.ylabel("Nombre d'itérations")
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc = 0, borderaxespad = 0.)  
    
    plt.subplot(212, sharex = ax1)
    plt.scatter(df.gamma, df.time_val, label = "Iteration de la valeur")
    plt.scatter(df.gamma, df.time_pol, label = "Iteration de la valeur")
    plt.xlabel("Valeur de Gamma")
    plt.ylabel("Durée d'execution")
        
    plt.show()




# Fonction qui étudie l'impact de p sur les performances des algorithmes. 
# Renvoie un dataframe de données ainsi que le tracé des courbes du nbre d'iteration et du temps d'execution en fonction de p
def impact_p(interval_p,
             nbr_tests = default_tests,
             nbLignes = default_nbLignes,
             nbCol = default_nbCol,
             gamma = default_gamma,
             epsilon = default_epsilon):
    df = pd.DataFrame(columns = ["p", "iter_val", "iter_pol", "time_val", "time_pol"])
    for p in interval_p:
        print("p = "+ str(p))
        somme1_it = 0
        somme1_t = 0
        somme2_it =0 
        somme2_t =0
        for k in range(nbr_tests):
            g= np.zeros((nbLignes,nbCol), dtype=np.int)
            p2.colordraw(g,nbLignes,nbCol,0.2,0.2,0.2,0.2,0.2)
            #print(g)
            #print("run "+str(k+1)+" out of "+str(nbr_tests))
            d,v,t, time = p2.iteration_de_la_valeur(g,p,gamma,epsilon)
            somme1_it += t
            somme1_t += time
            d,v,t, time = p2.iteration_de_la_politique(g,p,gamma,epsilon)
            somme2_it += t
            somme2_t += time
            line = pd.Series({'p' : p,
                              'iter_val' : somme1_it/nbr_tests,
                              'iter_pol': somme2_it/nbr_tests,
                              'time_val': somme1_t/nbr_tests,
                              'time_pol': somme2_t/nbr_tests})
        df = df.append(line, ignore_index=True)
    
    print(df)
    
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.scatter(df.p, df.iter_val, label = "Iteration de la valeur")
    plt.scatter(df.p, df.iter_pol, label = "Iteration de la politique")
    plt.ylabel("Nombre d'itérations")
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc = 0, borderaxespad = 0.)  
    
    plt.subplot(212, sharex = ax1)
    plt.scatter(df.p, df.time_val, label = "Iteration de la valeur")
    plt.scatter(df.p, df.time_pol, label = "Iteration de la valeur")
    plt.xlabel("Valeur de p")
    plt.ylabel("Durée d'execution")
        
    plt.show()
#
#sizes = [[5,5],
#         [5,10],
#         [10,10],
#         [10,15],
#         [15,15],
#         [15,20],
#         [20,20]]
#impact_size(sizes)
#
## Etude de l'impact de gamma
#
#interval_gammas = np.arange(0, 1, 0.1)
#impact_gamma(interval_gammas)
#
## Etude de l'impact de p
#
#interval_p = np.arange(0, 1, 0.1)
#impact_p(interval_p)
#
#
#

### Question 2 : On remplace le cout c(x) par la fonction c^q(x) ou q>1.
### Etudier à partir d'exemples comment varie la solution du problème lorque q augmente et commenter ce que vous avez observés.

variation_q = range(1,10)
def impact_q(variation_q,
             nbLignes = default_nbLignes,
             nbCol = default_nbCol,
             p = default_p,
             gamma = default_gamma,
             epsilon = default_epsilon):
    couts = [0,1,2,3,4]
    for q in variation_q:
        print(q)
        new_couts = [x**q for x in couts]
        g = grille.Grille(nbLignes,nbCol,2,0.2,0.2,0.2,0.2,0.2,new_couts).g
        p2.iteration_de_la_valeur(g,p,gamma,epsilon)

#impact_q(variation_q)


### Question 3 : On décide maintenant qu'une trajectoire est meilleure qu'une 
### autre si elle traverse moins de cases noires, ou en cas d'égalité moins de cases
### rouges, ...


## TODO : mettre une recompense plus élevée !
        # sinon pas interessant d'aller jusqu'au bout de la grille
def resolution_nbr_cases(nbLignes = default_nbLignes,
                         nbCol = default_nbCol,
                         p = default_p,
                         gamma = default_gamma,
                         epsilon = default_epsilon):
    size = nbLignes * nbCol
    couts = [0, 1, size ** 1, size ** 2, size ** 3]
    g = grille.Grille(nbLignes,nbCol,2,0.2,0.2,0.2,0.2,0.2,couts).g
    p2.iteration_de_la_valeur(g,p,gamma,epsilon)

resolution_nbr_cases()