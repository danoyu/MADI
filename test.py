# -*- coding: utf-8 -*-



from gurobipy import *
# script mdp4.py
from Tkinter import *
import numpy as np
import outils


def initialize():
    global PosX, PosY, cost
    # position initiale du robot
    PosX = 20 + 10
    PosY = 20 + 10
    for k in range(5):
        cost[k] = 0
    # cout et affichage
    Canevas.coords(Pion, PosX - 10, PosY - 10, PosX + 10, PosY + 10)
    wg.config(text=str(cost[1]))
    wb.config(text=str(cost[2]))
    wr.config(text=str(cost[3]))
    wn.config(text=str(cost[4]))
    ws.config(text='     total = ' + str(cost[0]))


# deplace le robot selon la touche
def deplacement(touche, li, cj):
    haut(touche, li, cj)
    bas(touche, li, cj)
    droite(touche, li, cj)
    gauche(touche, li, cj)

    # on dessine le pion a sa nouvelle position
    Canevas.coords(Pion, PosX - 10, PosY - 10, PosX + 10, PosY + 10)
    cost[0] = 0
    for k in range(4):
        cost[0] += cost[k + 1] * weight[k + 1]
    wg.config(text=str(cost[1]))
    wb.config(text=str(cost[2]))
    wr.config(text=str(cost[3]))
    wn.config(text=str(cost[4]))
    ws.config(text='     total = ' + str(cost[0]))


def haut(touche, li, cj):
    global PosX, PosY, cost, g
    # deplacement vers le haut
    if touche == 'a' and li > 0 and g[li - 1, cj, 0] > 0:
        PosY -= 20
        cost[g[li - 1, cj, 0]] += g[li - 1, cj, 1]
    else:
        print('deplacement imposiible')


def bas(touche, li, cj):
    global PosX, PosY, cost, g
    # deplacement vers le bas
    if touche == 'q' and li < nblignes - 1 and g[li + 1, cj, 0] > 0:
        PosY += 20
        cost[g[li + 1, cj, 0]] += g[li + 1, cj, 1]
    else:
        print('deplacement imposiible')


def droite(touche, li, cj):
    global PosX, PosY, cost, g
    # deplacement vers la droite
    if touche == 'm' and cj < nbcolonnes - 1 and g[li, cj + 1, 0] > 0:
        PosX += 20
        cost[g[li, cj + 1, 0]] += g[li, cj + 1, 1]
    else:
        print('deplacement imposiible')


def gauche(touche, li, cj):
    global PosX, PosY, cost, g
    # deplacement vers la gauche
    if touche == 'l' and cj > 0 and g[li, cj - 1, 0] > 0:
        PosX -= 20
        cost[g[li, cj - 1, 0]] += g[li, cj - 1, 1]
    else:
        print('deplacement imposiible')


# pblanc correspond à la proba d'avoir des murs
def colordraw(g, nblignes, nbcolonnes, pblanc, pverte, pbleue, prouge, pnoire):
    pblanc = pblanc
    pverte = pverte
    pbleue = pbleue
    prouge = prouge
    pnoire = pnoire
    # remplit la grille avec une couleur c selon les probas
    for i in range(nblignes):
        for j in range(nbcolonnes):
            y = 20 * i + 20
            x = 20 * j + 20
            z = np.random.uniform(0, 1)
            if z < pblanc:
                c = 0
            else:
                if z < pblanc + pverte:
                    c = 1
                else:
                    if z < pblanc + pverte + pbleue:
                        c = 2
                    else:
                        if z < pblanc + pverte + pbleue + prouge:
                            c = 3
                        else:
                            c = 4
            if c > 0:
                g[i, j] = c
                Canevas.create_oval(10 + x - 3, 10 + y - 3, 10 + x + 3, 10 + y + 3, width=1, outline=color[c],
                                    fill=color[c])
            else:
                Canevas.create_rectangle(x, y, x + 20, y + 20, fill=myblack)


def Clavier(event):
    global PosX, PosY, cost, g
    touche = event.keysym
    # position du robot
    cj = (PosX - 30) / (20 * zoom)
    li = (PosY - 30) / (20 * zoom)
    li = int(li)
    cj = int(cj)

    deplacement(touche, li, cj)
    # résolution automatique


def deterministe(strategie):
    global PosX, PosY, cost, g
    for a in strategie:
        cj = int((PosX - 30) / (20 * zoom))
        li = int((PosY - 30) / (20 * zoom))
        deplacement(a, li, cj)


# strategie mixte lors de l'appuie sur le touche "espace"
def mixte():
    global PosX, PosY, cost, g
    cj = int((PosX - 30) / (20 * zoom))
    li = int((PosY - 30) / (20 * zoom))
    if np.random.uniform(0, 1) < 0.4:
        touche = 'm'
    else:
        if np.random.uniform(0, 1) < 0.8:
            touche = 'q'
        else:
            if np.random.uniform(0, 1) < 0.9:
                touche = 'a'
            else:
                touche = 'l'
    deplacement(touche, li, cj)


# deplce le robot avec espace selon si mixte est cohée ou pas
def deplacement_deterministe_mixte(event):
    touche = event.keysym
    if touche == 'space':
        print(check)
        if check:
            mixte()
        else:
            deterministe(['q'])


Mafenetre = Tk()
Mafenetre.title('MDP')

# taille de la grille
nblignes = 5
nbcolonnes = 8

# Creation d'un widget Canvas (pour la grille)
Largeur = 20 * nbcolonnes + 40
Hauteur = 20 * nblignes + 40

# valeurs de la grille
g = np.zeros((nblignes, nbcolonnes), dtype=np.int)
cost = np.zeros(5, dtype=np.int)
weight = np.zeros(5, dtype=np.int)
weight[1] = 1
weight[2] = 1
weight[3] = 1
weight[4] = 1

# def des couleurs
myred = "#D20B18"
mygreen = "#25A531"
myblue = "#0B79F7"
mygrey = "#E8E8EB"
myyellow = "#F9FB70"
myblack = "#2D2B2B"
mywalls = "#5E5E64"
mywhite = "#FFFFFF"
color = [mygrey, mygreen, myblue, myred, myblack]

# ecriture du quadrillage et coloration

PosX = 20
PosY = 30

Canevas = Canvas(Mafenetre, width=Largeur, height=Hauteur, bg=mywhite)
for i in range(nblignes + 2):
    ni = 20 * i
    Canevas.create_line(20, ni, Largeur - 20, ni)
for j in range(nbcolonnes + 2):
    nj = 20 * j
    Canevas.create_line(nj, 20, nj, Hauteur - 20)
colordraw(g, nblignes, nbcolonnes, 0.2, 0.2, 0.2, 0.2, 0.2)
Pion = Canevas.create_oval(PosX - 10, PosY - 10, PosX + 10, PosY + 10, width=2, outline='black', fill=myyellow)

Canevas.focus_set()
Canevas.bind('<Key>', Clavier)
Canevas.bind('<Key>', deplacement)

Canevas.pack(padx=5, pady=5)

# Creation d'un widget Button (bouton Quitter)
Button(Mafenetre, text='Restart', command=initialize).pack(side=LEFT, padx=5, pady=5)
Button(Mafenetre, text='Quit', command=Mafenetre.destroy).pack(side=LEFT, padx=5, pady=5)

check = IntVar()
#print(check)
c = Checkbutton(Mafenetre, text="Mixte", variable=check)
c.pack()
zoom = 1
w = Label(Mafenetre, text='     Costs: ', fg=myblack, font="Verdana " + str(int(5 * zoom)) + " bold")
w.pack(side=LEFT, padx=5, pady=5)
wg = Label(Mafenetre, text=str(cost[1]), fg=mygreen, font="Verdana " + str(int(5 * zoom)) + " bold")
wg.pack(side=LEFT, padx=5, pady=5)
wb = Label(Mafenetre, text=str(cost[2]), fg=myblue, font="Verdana " + str(int(5 * zoom)) + " bold")
wb.pack(side=LEFT, padx=5, pady=5)
wr = Label(Mafenetre, text=str(cost[3]), fg=myred, font="Verdana " + str(int(5 * zoom)) + " bold")
wr.pack(side=LEFT, padx=5, pady=5)
wn = Label(Mafenetre, text=str(cost[4]), fg=myblack, font="Verdana " + str(int(5 * zoom)) + " bold")
wn.pack(side=LEFT, padx=5, pady=5)
ws = Label(Mafenetre, text='     total = ' + str(cost[0]), fg=myblack, font="Verdana " + str(int(5 * zoom)) + " bold")
ws.pack(side=LEFT, padx=5, pady=5)
Pion = Canevas.create_oval(PosX - 10, PosY - 10, PosX + 10, PosY + 10, width=2, outline='black', fill=myyellow)


#finir le pl dans l'ajout des contraites qui ne marche pas
# revoir si la formulation est bonne

def pl(g,nbLignes,nbCol,liste_actions,rewards,p,gamma,epsilon):

    # Create a new model
    m = Model("test")


    val_etats = []


    # Create variables
    for i in range(nbLignes):
        for j in range(nbCol):
            n = "v["+str(i)+"]["+str(j)+"]"
            r = rewards[g[i][j]]
            if i == len(g) - 1 and j == len(g[0]) - 1:
                r = rewards[-1]
            x = m.addVar(vtype=GRB.CONTINUOUS, name=n)
            val_etats.append(x)

    # Set objective
    # print(val_etats[0])
    # print(m.getVars())
    # for v in m.getVars():
    #     print('la')
    #     print('%s %g' % (v.varName, v.x))
    # print(y)

    val_etats = np.array(val_etats)
    val_etats = np.reshape(val_etats,(nbLignes,nbCol))

    m.setObjective(np.sum(val_etats), GRB.MINIMIZE)
    print((val_etats.shape))
    for i in range(nbLignes):
        for j in range(nbCol):
            for action in liste_actions:
                r = outils.reward_action(g, i, j, action, rewards)
                if r:
                    if i == len(g) - 1 and j == len(g[0]) - 1:
                            r = rewards[-1]
                    m.addConstr(val_etats[i][j] >= r + gamma * outils.sum_p_v(g, val_etats, i, j, p, action))

    m.optimize()

    # for v in m.getVars():
    #     print('%s %g' % (v.varName, v.x))
    val_etats = np.reshape(np.array([v.x for v in m.getVars()]),(nbLignes,nbCol))
    # print(val_etats)
    # print(val_etats.shape)

    # for v in m.getConstrs():
    #     print('%s' % (v.getAttr("slack")))

    # print('Obj: %g' % m.objVal)

    # Affiche le pl dans un fichier
    # m.write('debug.lp')

    d = np.zeros((nbLignes, nbCol))
    for i in range(len(val_etats)):
        for j in range(len(val_etats[0])):
            val_par_action = np.zeros(len(liste_actions))
            for action in liste_actions:
                    val_par_action[action] = r + gamma * outils.sum_p_v(g, val_etats, i, j, p, action)
            d[i][j] = np.argmax(val_par_action)
    return d, val_etats


rewards = [-5, -1, -2, -3, -4, 1000]
liste_actions = [0, 1, 2, 3]
p = 0.6
gamma = 0.9
epsilon = 0.00001
d,v = pl(g, len(g), len(g[0]), liste_actions, rewards, p, gamma, epsilon)
print(d,v)
print(g)

initialize()

Mafenetre.mainloop()
