# -*- coding: utf-8 -*-


import outils as ot
import grille_avec_chiffre as gr
import algos
import pandas as pd
from matplotlib import pyplot as plt


default_tests = 1
default_nbLignes = 10
default_nbCol = 10
default_p = 1
default_gamma = 0.9
default_epsilon = 0.00001

## ----- Question d)1 -----

##Tester la resolution pratique du probleme de recherche d'une trajectoire equilibrée
## sur des grilles différentes tailles avec l'approche proposee en b).
## On donnera ici encore les temps moyens de resolution.


# Fonction qui étudie l'impact de la taille de l'instance sur les performances des algorithmes. 
# Renvoie un dataframe de données ainsi que le tracé des courbes du nbre d'iteration et du temps d'execution en fonction de la taille
def impact_size(sizes,
                nbr_tests = default_tests,
                p = default_p,
                gamma = default_gamma,
                epsilon = default_epsilon):
    df = pd.DataFrame(columns = ["dimensions",
                                 "taille",
                                 "iter_val",
                                 "iter_pol",
                                 "iter_pl",
                                 "time_val",
                                 "time_pol",
                                 "time_pl",
                                 ])
    for i, taille in enumerate(sizes) : 
        print(taille)
        somme1_it = 0
        somme1_t = 0
        somme2_it =0 
        somme2_t =0
        for k in range(nbr_tests):
            g = gr.Grille_chiffre(taille[0],taille[1],2,0.2,0.2,0.2,0.2,0.2,1000).g
            #print(g)
            #print("run "+str(k+1)+" out of "+str(nbr_tests))
            # politiques mixtes
            d,v,t, time = algos.pl_part3_1(g,p,gamma,epsilon)
            somme1_it += t
            somme1_t += time
            # politiques pures
            d,v,t, time = algos.pl_part3_2(g,p,gamma,epsilon)
            somme2_it += t
            somme2_t += time
            line = pd.Series({'dimensions' : taille,
                              'taille' : taille[0]*taille[1],
                              'iter_pl1' : somme1_it/nbr_tests,
                              'iter_pl2': somme2_it/nbr_tests,
                              'time_pl1': somme1_t/nbr_tests,
                              'time_pl2': somme2_t/nbr_tests,
                              })
        df = df.append(line, ignore_index=True)
        
    # Affichage des résultats    
    print(df)
  
    plt.figure(1)
    ax1 = plt.subplot(211)
    plt.scatter(df.taille, df.iter_pl1, label = "Politiques mixtes")
    plt.scatter(df.taille, df.iter_pl2, label = "Politiques pures")    
    #plt.xlabel("Taille de l'instance")
    plt.ylabel("Nombre d'itérations")
    plt.setp(ax1.get_xticklabels(), visible=False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc = 0, borderaxespad = 0.)  
    
    plt.subplot(212, sharex = ax1)
    plt.scatter(df.taille, df.time_pl1, label = "Politiques mixtes")
    plt.scatter(df.taille, df.time_pl2, label = "Politiques pures")
    plt.xlabel("Taille de l'instance")
    plt.ylabel("Durée d'execution")
    
    plt.show()
    

# sizes = [[5,5],
#          [5,10],
#          [10,10],
#          [10,15],
#          [15,15],
#          [15,20],
#          [20,20]]
#
# impact_size(sizes)



## ----- Question d)2 -----


## Comparer les valeurs de politiques mixtes optimales à des valeurs de politiques
## pure obtimales que l'on obtient

# comment comparer ??
# politique mixte -> probabilité
# comparer celle qui a la plus grande proba à la politique pure s


## ----- Question d)3 -----

# Simuler les politiques obtenues pour observer leurs performances en pratiques
  
# Fonction qui pour une grille donnée va calculer les politiques mixtes et pures optimales
# et les simuler un nbr nbr_tests de fois pour evaluer leurs couts respectifs.
def simul_politiques(g,
                     nbr_tests = default_tests,
                     p = default_p,
                     gamma = default_gamma
                     ):
    # on calcul les deux politiques optimales
    d_mixte,v,t,time = algos.pl_part3_1(g,p,gamma)
    d_pur,v,t,time = algos.pl_part3_2(g,p,gamma)
    # on calcul le cout moyen pour chacune des ces politiques, en pratique
    mean_mixte_cost = ot.mean_experienced_cost_p3(d_mixte,g,p,nbr_tests)
    mean_pur_cost = ot.mean_experienced_cost_p3(d_pur,g,p,nbr_tests)
    return(mean_mixte_cost,mean_pur_cost)
  
    
# créer une grille
# g = gr.Grille_chiffre(default_nbLignes,default_nbCol,2,0.2,0.2,0.2,0.2,0.2,1000).g
# mean_mixte_cost,mean_pur_cost = simul_politiques(g,
#                                                  nbr_tests = default_tests,
#                                                  p = default_p,
#                                                  gamma = default_gamma
#                                                  )
#  print(mean_mixte_cost)
# print(mean_pur_cost)




## ===== Question d) =====

# Pour une instance donnée comparer le vecteur cout que vous obternez pour une politique optimale
# calculee avec l'approche multi-obj a celui de l'approche proposée en a.
# Simulez 10 ou 20 fois ces deux politiques et observez les couts moyens obtenus

def compare_methods(g,
                    nbr_tests = default_tests,
                    p = default_p,
                    gamma = default_gamma):
    d_multi_obj,v,t,time = algos.pl_part3_1(g,p,gamma)
    d_pdm,v,t,time = algos.iteration_de_la_valeur(g,p,gamma)
    # on calcul le cout moyen pour chacune des ces politiques, en pratique
    mean_multi_obj = ot.mean_experienced_cost_p3(d_multi_obj,g,p,nbr_tests)
    mean_pdm = ot.mean_experienced_cost_p3(d_pdm,g,p,nbr_tests) 
    return(mean_multi_obj,mean_pdm)        
 
# g = gr.Grille_chiffre(default_nbLignes,default_nbCol,2,0.2,0.2,0.2,0.2,0.2,1000).g
# mean_mixte_cost,mean_pur_cost = simul_politiques(g,
#                                                  nbr_tests = default_tests,
#                                                  p = default_p,
#                                                  gamma = default_gamma
#                                                  )
# print(mean_mixte_cost)
# print(mean_pur_cost)
