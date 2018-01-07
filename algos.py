
import numpy as np
import outils as ot
import time as tm
import grille as gr
import gurobipy as grb

# definition des actions
liste_actions = [0,1,2,3]

def iteration_de_la_valeur(g,p,gamma,epsilon):
    global liste_actions
    start = tm.time()
    
    #2 etats :  - pour t-1 
    #           - pour t 
    val_etats =  np.zeros((len(g),len(g[0])))
    vt =  np.zeros((len(g),len(g[0])))
    q = np.zeros((len(g),len(g[0]),len(liste_actions)))
    t = 0
    #critere d'arret
    while np.max(np.abs(vt - val_etats)) >= epsilon or t==0:
        t += 1
        #etat precedant
        vt = np.copy(val_etats) 
        for i in range(len(val_etats)):#TODO : plus propre de mettre nbLignes non ?
            for j in range(len(val_etats[0])): # pareil 
                for action in liste_actions:
                    r = - g[i][j][1]                     
                    q[i][j][action] = r + gamma * ot.sum_p_v(g,val_etats,i,j,p,action)
                val_etats[i][j] = max(q[i][j])
    
    #politique optimal
    d = np.zeros((len(g),len(g[0])))
    for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                d[i][j] = np.argmax(q[i][j])
    end = tm.time()
    time = end - start
    return d,val_etats,t, time 


def iteration_de_la_politique(g,p,gamma,epsilon):
    global liste_actions

    #2 etats :  - pour t-1 
    #           - pour t 
    start = tm.time()

    val_etats =  np.zeros((len(g),len(g[0])))
    d = np.zeros((len(g),len(g[0])))

    t = 0
    vt = val_etats,val_etats
    
    #critere d'arret
    while np.max(np.abs(vt - val_etats)) >= epsilon or t==0:
#     while not(np.array_equal(d_pred,d)) or t == 0:
        t += 1
        #valeur de la politique courant
        vt = np.copy(val_etats)
        
        #evaluation de la politique courante
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                r = -g[i][j][1]
                #arrivé au but
                val_etats[i][j] =  r + gamma * ot.sum_p_v(g,val_etats,i,j,p,d[i][j])
    
        #amelioration de la politique
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                arg = []
                for action in liste_actions:
                    #arrivé au but
                    r = -g[i][j][1]
                    arg.append(r + gamma*ot.sum_p_v(g,val_etats,i,j,p,action))
                arg = np.array(arg)
                d[i][j] = np.argmax(arg)
#    print(g)
 #   print(ot.from_action_to_dir(d,g))
#    #print(v)
#    print(t)
    end = tm.time()
    time = end - start
    return d,val_etats,t, time


#
#grille = gr.Grille(10,10,2,0.2,0.2,0.2,0.2,0.2,[0,1,2,3,4], 1000)
#p = 0.6
#gamma = 0.9
#epsilon = 0.00001

## Test iteration de la valeur
#d,v,t,time = iteration_de_la_valeur(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))
##print(v)
##print(t)
#

## Test iteration de la politique
#d,v,t,time = iteration_de_la_politique(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))

# Test PL
#d,v,time = pl_part2(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))

#grille.Mafenetre.mainloop() #Affichage 

# TEST PL part3
#grille = gr.Grille_avec_chiffre(10,10,2,0.2,0.2,0.2,0.2,0.2, 1000)
#p = 0.6
#gamma = 0.9
#epsilon = 0.00001

#d,v,time = pl_part3_1(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))

#d,v,time = pl_part3_1(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))
