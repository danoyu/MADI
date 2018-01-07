
import numpy as np
import outils as ot
import time as tm
import gurobipy as grb

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
    d = np.zeros((len(g), len(g[0])))
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
        t += 1
        #valeur de la politique courant
        vt = np.copy(val_etats)
        
        #evaluation de la politique courante
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                r = -g[i][j][1]
                #arrive au but
                val_etats[i][j] =  r + gamma * ot.sum_p_v(g,val_etats,i,j,p,d[i][j])
    
        #amelioration de la politique
        for i in range(len(val_etats)):
            for j in range(len(val_etats[0])):
                arg = []
                for action in liste_actions:
                    #arrive au but
                    r = -g[i][j][1]
                    arg.append(r + gamma*ot.sum_p_v(g,val_etats,i,j,p,action))
                arg = np.array(arg)
                d[i][j] = np.argmax(arg)

    end = tm.time()
    time = end - start
    return d,val_etats,t, time

def pl(g,p,gamma):
   global liste_actions
   start = tm.time()

   # Create a new model
   m = grb.Model("test")

   val_etats = []

   # Create variables
   for i in range(len(g)):
       for j in range(len(g[0])):
           n = "v["+str(i)+"]["+str(j)+"]"
           r = - g[i][j][1]
           x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
           val_etats.append(x)

   val_etats = np.array(val_etats)
   val_etats = np.reshape(val_etats,(len(g),len(g[0])))

   m.setObjective(np.sum(val_etats), grb.GRB.MINIMIZE)

   for i in range(len(g)):
       for j in range(len(g[0])):
           for action in liste_actions:
               r = -g[i][j][1]
               m.addConstr(val_etats[i][j] >= r + gamma * ot.sum_p_v(g, val_etats, i, j, p, action))

   m.optimize()

   val_etats = np.reshape(np.array([v.x for v in m.getVars()]),(len(g),len(g[0])))

   d = np.zeros((len(g), len(g[0])))
   for i in range(len(val_etats)):
       for j in range(len(val_etats[0])):
           val_par_action = np.zeros(len(liste_actions))
           for action in liste_actions:
                   val_par_action[action] = r + gamma * ot.sum_p_v(g, val_etats, i, j, p, action)
           d[i][j] = np.argmax(val_par_action)
   end = tm.time()
   time = end - start
   #nombre d'iteration
   t = m.getAttr('IterCount')
   return d, val_etats, t, time


def pl_part3_1(g, p, gamma):
    global liste_actions
    # Create a new model
    m = grb.Model("politique-mixte")

    x_sa = []

    # Create variables
    # variable objective
    z = m.addVar(name="z")

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "x[" + str(i) + "][" + str(j) + "][" + str(action) + ']'
                x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
                x_sa.append(x)

    # x_sa tableau a trois dimension, 2 pour l'etat, et 1 pour l'action
    # pour chaque etat on renvoit un vecteur en principe de zeros et de 1 avec 1 sur
    x_sa = np.array(x_sa)
    x_sa = np.reshape(x_sa, (len(g), len(g[0]), len(liste_actions)))

    m.setObjective(z, grb.GRB.MINIMIZE)
    # print((x_sa.shape))

    m.update()

    #  Contraintes

    for re in range(4):
        constr = []
        for i in range(len(g)):
            for j in range(len(g[0])):
                # on teste la ressource
                ressource = g[i][j][0]
                if ressource != 0:  # si il s'agit bien d'une ressource et pas d'un mur
                    r = [0] * 4
                    r[re] = -g[i][j][1]
                    # z < f(x)
                    constr = constr + (
                            r[0] * m.getVarByName("x[" + str(i) + "][" + str(j) + "][" + str(liste_actions[0]) + ']')
                            + r[1] * m.getVarByName("x[" + str(i) + "][" + str(j) + "][" + str(liste_actions[1]) + ']')
                            + r[2] * m.getVarByName("x[" + str(i) + "][" + str(j) + "][" + str(liste_actions[2]) + ']')
                            + r[3] * m.getVarByName("x[" + str(i) + "][" + str(j) + "][" + str(liste_actions[3]) + ']'))

        m.addConstr(z <= constr)

    for i in range(len(g)):
        for j in range(len(g[0])):  # pour chaque etat
            sum_actions = 0
            for action in liste_actions:
                sum_actions += x_sa[i][j][action]
            sum_2 = 0
            for k in range(len(g)):
                for l in range(len(g[0])):
                    somme = 0
                    for action in liste_actions:
                        cases = ot.probas_action(g, k, l, p, action)
                        # print(x_sa[k][l][action])
                        # print(len(cases))
                        # print(cases[2])
                        for en, c in enumerate(cases):
                            somme += cases[2][en] * x_sa[i][j][action]
                    sum_2 += somme

            m.addConstr(sum_actions + gamma * sum_2 == 1)

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                m.addConstr(x_sa[i][j][action] >= 0)

    m.write('debug.lp')
    m.optimize()

    # on va recuperer x_sa

    # d'apres Propriete 2
    delta_sa = np.zeros((len(g), len(g[0]), len(liste_actions)))
    # D'apres la proposition 2
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions = 0
            for action in liste_actions:
                somme_actions += x_sa[i][j][action]
            delta_sa[i][j][action] = x_sa[i][j][action] / somme_actions

    return delta_sa


def pl_part3_2(g, p, gamma):
    global liste_actions
    # Create a new model
    m = grb.Model("politique-mixte")

    x_sa = []
    d_sa = []

    # Create variables
    # variable objective
    z = m.addVar(name="z")

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "x[" + str(i) + "][" + str(j) + "][" + str(action) + ']'
                x = m.addVar(vtype=grb.GRB.CONTINUOUS, name=n)
                x_sa.append(x)

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                n = "d[" + str(i) + "][" + str(j) + "][" + str(action) + ']'
                d = m.addVar(vtype=grb.GRB.BINARY, name=n)
                d_sa.append(d)

                # x_sa tableau a trois dimension, 2 pour l'etat, et 1 pour l'action
    # pour chaque etat on renvoit un vecteur en principe de zeros et de 1 avec 1 sur
    x_sa = np.array(x_sa)
    x_sa = np.reshape(x_sa, (len(g), len(g[0]), len(liste_actions)))

    d_sa = np.array(d_sa)
    d_sa = np.reshape(d_sa, (len(g), len(g[0]), len(liste_actions)))

    m.setObjective(z, grb.GRB.MINIMIZE)
    print((x_sa.shape))

    # Create constraints
    # autre methode :
    # dans chaque case, on teste la ressource et on l'ajoute au bon cout
    # -> permet de ne parcourir qu'une seule fois la grille au lieu de 4
    f_x = np.zeros(5)
    for i in range(len(g)):
        for j in range(len(g[0])):
            # on teste la ressource
            ressource = g[i][j][0]
            if ressource != 0:  # si il s'agit bien d'une ressource et pas d'un mur
                somme_actions = 0
                for action in liste_actions:
                    somme_actions += x_sa[i][j][action]
                r = -g[i][j][1]
                terme_etat = -r * somme_actions
                f_x[ressource] += terme_etat

                # Contraintes

    for ressource in range(4) + 1:
        m.addConstr(z <= f_x[ressource])

    for i in range(len(g)):
        for j in range(len(g[0])):  # pour chaque etat
            sum_actions = 0
            for action in liste_actions:
                sum_actions += x_sa[i][j][action]
            sum_2 = 0
            for k in range(len(g)):
                for l in range(len(g[0])):
                    somme = 0
                    for action in liste_actions:
                        cases = ot.probas_action(g, k, l, p, action)
                        for i, c in enumerate(cases):
                            somme += cases[2] * x_sa[k][l]
                    sum_2 += somme

            m.addConstr(sum_actions + gamma * sum_2 == 1)

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                m.addConstr(x_sa[i][j] >= 0)

    # Ajout des contraintes des politiques pures
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions = 0
            for action in liste_actions:
                somme_actions += d_sa[i][j][action]
            m.addConstr(somme_actions <= 1)

    for i in range(len(g)):
        for j in range(len(g[0])):
            for action in liste_actions:
                m.addConstr((1 - gamma) * x_sa[i][j][action] - d_sa[i][j][action] <= 0)

    m.optimize()

    # d'apres Propriete 2
    delta_sa = np.zeros(len(g), len(g[0]), 4)
    # D'apres la proposition 2
    for i in range(len(g)):
        for j in range(len(g[0])):
            somme_actions = 0
            for action in liste_actions:
                somme_actions += x_sa[i][j][action]
            delta_sa[i][j][action] = x_sa[i][j][action] / somme_actions

    return delta_sa



#grille = gr.Grille(10,10,2,0.2,0.2,0.2,0.2,0.2,[0,1,2,3,4], 1000)
#p = 0.6
#gamma = 0.9
#epsilon = 0.00001

# Test iteration de la valeur
#d,v,t,time = iteration_de_la_valeur(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))
#print(v)
#print(t)


# Test iteration de la politique
#d,v,t,time = iteration_de_la_politique(grille.g,p,gamma,epsilon)
#print(ot.from_action_to_dir(d,grille.g))

# Test PL
#d,v,time = pl_part2(grille.g, p, gamma, epsilon)
#print(ot.from_action_to_dir(d,g))

#grille.Mafenetre.mainloop() #Affichage 


# Test PL Multi Objectif (Partie 3)
# delta_sa = pl_part3_1(grille.g, liste_actions, p, gamma, epsilon)
# print(delta_sa)

# delta_sa = pl_part3_1(grille.g, liste_actions, p, gamma, epsilon)
# print(delta_sa)