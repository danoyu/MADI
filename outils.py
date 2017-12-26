# -*- coding: utf-8 -*-


import numpy as np
# cases dispo prenant en compte les limite 
# pas les murs !!!

# 0 : droite
# 1 : gauche
# 2 : bas
# 3 :haut
def cases_dispo(g,i,j,action):
    cases = []
    #si on va a droite        
    if action == 0 :
        if j!=(len(g[0])-1):
            j += 1
            cases.append([i,j])
            if i != 0:
                cases.append([i-1,j])
            if i != (len(g)-1):
                cases.append([i+1,j])
    #gauche           
    if action == 1 :
        if j!=0:
            j -= 1
            cases.append([i,j])
            if i != 0:
                cases.append([i-1,j])
            if i != (len(g)-1):
                cases.append([i+1,j])
                
    #bas
    if action == 2 :
        if i!=(len(g)-1):
            i += 1
            cases.append([i,j])
            if j != 0:
                cases.append([i,j-1])
            if j != (len(g[0])-1):
                cases.append([i,j+1])
    #haut
    if action == 3 :
        if i!=0:
            i -= 1
            cases.append([i,j])
            if j != 0:
                cases.append([i,j-1])
            if j != (len(g[0])-1):
                cases.append([i,j+1])

    return cases

#cases_dispo(g,9,0,2)


#Calcul des probas d'aller en x et a droite et a gauche de x 
#prend en compte l'incertain
def probas_action(g,i,j,p,action):
    probas = [0]*3
    cases = cases_dispo(g,i,j,action)
    for i,c in enumerate(cases):
        if g[c[0]][c[1]] != 0 :
            probas[i] = 1
          
    #terme du milieu est un mur
    if probas[1] == 0:
        return cases,np.zeros(len(probas))
    else :
        if probas[0] == 0:
            if probas[2] == 0:
                # les cases voisines sont des murs
                probas[1] = 1
            # la derniere case est accessible
            else:
                probas[1] = (1+p)/2
                probas[2] = (1-p)/2
        #premiere case n'est pas un mur
        else:
            if probas[2] == 0:
                probas[0] = (1-p)/2
                probas[1] = (1+p)/2
            # toutes les cases sont accessibles
            else:
                probas[0] = (1-p)/2
                probas[1] = p
                probas[2] = (1-p)/2   
#     print(cases,probas)
    return cases,probas

# probas_action(g,0,0,0.25,1)

#prend en compte l'incertain
def sum_p_v(g,val_etats,i,j,p,action):
    somme = 0
    cases, probas = probas_action(g,i,j,p,action)
    for i,c in enumerate(cases): 
        somme += probas[i] * val_etats[c[0]][c[1]]
    return somme


# val_etats =  np.random.rand(10,15)
# sum_p_v(g,val_etats,0,0,0.25,1

#renvoi reward apres l'action
# None si action hors limite
def reward_action(g,i,j,action,rewards):
    if action == 0:
        try :
            return rewards[g[i][j+1]]
        except:
            return None
    if action == 1:
        try :
            return  rewards[g[i][j-1]]
        except:
            return None
    if action == 2:
        try :
            return  rewards[g[i+1][j]]
        except:
            return None
    if action == 3:
        try :
            return  rewards[g[i-1][j]]
        except:
            return None
        