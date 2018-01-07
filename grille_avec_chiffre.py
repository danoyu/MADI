#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Tkinter as tk
import numpy as np
import random

class Grille_chiffre():
    def __init__(self,nbLignes,nbCol,zoom,pblanc,pverte,pbleue,prouge,pnoire,reward):
        self.nbLignes = nbLignes
        self.nbCol = nbCol
        self.zoom = zoom
        self.pblanc = pblanc
        self.pverte = pverte
        self.pbleue = pbleue
        self.prouge = prouge
        self.pnoire = pnoire
        
        self.reward = reward
        
        self.g = np.zeros((nbLignes,nbCol,2), dtype=np.int)
        self.cost = [0]*6
        self.weight= np.ones(6, dtype=np.int)
        self.weight[0]=0
        
        
#         self.PosX = PosX
#         self.PosY = PosY
        
        #fenetre graphique 
        self.Mafenetre = tk.Tk()
        
        #creation de l'interface graphique
        self.Canvas = self.init_canvas()
        
        #coloration de la grille 
        self.colordraw()
        
        #creation du Pion
        self.init_Pion()
        
        self.Canevas.focus_set()
        self.Canevas.bind('<Key>',self.Clavier)
        self.Canevas.pack(padx =6, pady =6)
        
        #ajout des boutons
        self.init_boutton()
        self.check = tk.IntVar()
        self.c = tk.Checkbutton(self.Mafenetre, text="Mixte", variable=self.check).pack()
        self.init_cost()
        
    #creation d'un grille vide
    def init_canvas(self):
        self.Mafenetre.title('MDP')
        mywhite="#FFFFFF"
        Largeur = self.zoom*20*self.nbCol+40
        Hauteur = self.zoom*20*self.nbLignes+40
        self.Canevas = tk.Canvas(self.Mafenetre, width = Largeur, height =Hauteur, bg =mywhite)
        for i in range(self.nbLignes+1):
            ni=self.zoom*20*i+20
            self.Canevas.create_line(20, ni, Largeur-20,ni)
        for j in range(self.nbCol+1):
            nj=self.zoom*20*j+20
            self.Canevas.create_line(nj, 20, nj, Hauteur-20)
    
    #coloration grille 
    def colordraw(self):
        mygreen="#1AD22C"
        myblue="#0B79F7"
        #mygrey="#E8E8EB"
        myblack="#5E5E64"
        mywhite="#FFFFFF"
        myred="#F70B42"
        
        mytarget="magenta"
        
        mywalls="#5E5E64"
        #need_init = True
        color=[mywhite,mygreen,myblue,myred,myblack,mytarget]
        for i in range(self.nbLignes):
            for j in range(self.nbCol):
                y =self.zoom*20*i+20
                x =self.zoom*20*j+20
                # pas de mur sur la premiere case et ses alentours 
                # idem pour l'objectif
                if (i==0 and j==0) or (i==0 and j==1) or (i==1  and j==0) or (i==len(self.g)-2 and j==len(self.g[0])-1) or (i==len(self.g)-1 and j==len(self.g[0])-2):
#                     print(i,j)
                    c = np.random.random_integers(3)
                elif (i==len(self.g)-1 and j==len(self.g[0])-1):
                    # on est à la case cible
                    c=5       
                else :
                    z= random.uniform(0,1)
                    if z < self.pblanc:
                        c=0
                    else:
                        if z < self.pblanc+ self.pverte:
                            c=1
                        else:
                            if z < self.pblanc+ self.pverte + self.pbleue:
                                c=2
                            else:
                                if z< self.pblanc+ self.pverte + self.pbleue +self.prouge:
                                    c=3
                                else:
                                    c=4 

                if c>0:
                    self.g[i,j,0]=c
                    if (i==len(self.g)-1 and j==len(self.g[0])-1):
                        # on est à la case cible
                        # on met le reward à 1000
                        self.g[i,j,1]= - self.reward
                    else :
                        self.g[i,j,1]=np.random.random_integers(9)  
                    self.Canevas.create_text(x+self.zoom*(10),y+self.zoom*(10), text=str(self.g[i,j,1]),fill=color[self.g[i,j,0]],font = "Verdana "+str(int(6*self.zoom))+" bold")
                else:
                    self.Canevas.create_rectangle(x, y, x+self.zoom*20, y+self.zoom*20, fill=mywalls)
        
    #creation du Pion
    def init_Pion(self):
        myyellow="#F9FB70"
        self.PosX = 20+10*self.zoom
        self.PosY = 20+10*self.zoom
        self.Pion = self.Canevas.create_oval(self.PosX-9*self.zoom,self.PosY-9*self.zoom,self.PosX+9*self.zoom,self.PosY+9*self.zoom,width=2,outline='black',fill=myyellow)
        
    #Bouton quitter et restart
    def init_boutton(self):
        #Creation d'un widget Button (bouton Quitter)
        tk.Button(self.Mafenetre, text ='Quitter', command = self.Mafenetre.destroy).pack(side=tk.LEFT,padx=5,pady=5)
        tk.Button(self.Mafenetre, text ='Restart', command = self.restart).pack(side=tk.LEFT, padx=5,pady=5)
        
    #bouton restart 
    def restart(self):
        self.cost = [0]*6
        self.PosX = 20+10*self.zoom
        self.PosY = 20+10*self.zoom
        self.Canevas.coords(self.Pion,self.PosX - 9*self.zoom, self.PosY -9*self.zoom, self.PosX +9*self.zoom, self.PosY +9*self.zoom )
        self.wg.config(text=str(self.cost[1]))
        self.wb.config(text=str(self.cost[2]))
        self.wr.config(text=str(self.cost[3]))
        self.wn.config(text=str(self.cost[4]))
        self.wm.config(text=str(self.cost[5]))
        self.ws.config(text='     total = '+str(self.cost[0]))
        
        
    #deplace le robot selon la touche
    def deplacement(self,touche,li,cj):
        if touche == 'a':
            self.haut(li,cj)
        else :
            if touche == 'q' :
                self.bas(li,cj)
            else :
                if touche == 'l' :
                    self.gauche(li,cj)
                else :
                    if touche == 'm' :
                        self.droite(li,cj)
                    else:
                        print('touche invalide')

        # on dessine le pion a sa nouvelle position
        self.Canevas.coords(self.Pion,self.PosX - 9*self.zoom, self.PosY -9*self.zoom, self.PosX +9*self.zoom, self.PosY +9*self.zoom )
        self.cost[0]=0    
        for k in range(5):
            self.cost[0]+=self.cost[k+1]*self.weight[k+1]        
        self.wg.config(text=str(self.cost[1]))
        self.wb.config(text=str(self.cost[2]))
        self.wr.config(text=str(self.cost[3]))
        self.wn.config(text=str(self.cost[4]))
        self.wm.config(text=str(self.cost[5]))
        self.ws.config(text='     total = '+str(self.cost[0]))


    def haut(self,li,cj):
        # deplacement vers le haut
        if li>0 and self.g[li-1,cj,0]>0:
            self.PosY -= 20*self.zoom
            self.cost[self.g[li-1,cj,0]]+= self.g[li-1,cj,1]  
        else:
            print('deplacement imposiible')

    def bas(self,li,cj):
           # deplacement vers le bas
        if li<self.nbLignes-1 and self.g[li+1,cj,0]>0:
            self.PosY += 20*self.zoom
            self.cost[self.g[li+1,cj,0]]+=self.g[li+1,cj,1]
        else:
            print('deplacement imposiible')
        
    def droite(self,li,cj):
        # deplacement vers la droite
        if cj< self.nbCol-1 and self.g[li,cj+1,0]>0:
            self.PosX += 20*self.zoom
            self.cost[self.g[li,cj+1,0]]+=self.g[li,cj+1,1] 
        else:
            print('deplacement imposiible')
        
    def gauche(self,li,cj):
        # deplacement vers la gauche
        if cj >0 and self.g[li,cj-1,0]>0:
            self.PosX -= 20*self.zoom
            self.cost[self.g[li,cj-1,0]]+=self.g[li,cj-1,1] 
        else:
            print('deplacement imposiible')
            
    #deplacement selon une sategie deterministe lors de l'appuie sur la touche "espace"
    def deterministe(self,strategie):
        for a in strategie:
            cj=int((self.PosX-30)/(20*self.zoom))
            li=int((self.PosY-30)/(20*self.zoom))
            self.deplacement(a,li,cj)

    #strategie mixte lors de l'appuie sur le touche "espace avec "mixte" coché dans GUI
    def mixte(self):
        cj=int((self.PosX-30)/(20*self.zoom))
        li=int((self.PosY-30)/(20*self.zoom))
        p = random.uniform(0,1)
        if p < 0.4:
                touche = 'm'
        else:
                if  p <0.6: 
                    touche ='q'
                else:
                    if  p < 0.8: 
                        touche ='a'
                    else:
                        touche = 'l'
        self.deplacement(touche,li,cj)
        
    #Deplace le robot : 
    # si appuie sur espace :
        # - si mixte est coche alors joue la strategie mixte 
        # - sinon joue la stratégie deterministe
    # sinon :  a : haut ; q : bas ; l : droite ; m : gauche
    def Clavier(self, event):
        touche = event.keysym
        #position du robot
        cj=(self.PosX-30)/(20*self.zoom)
        li=(self.PosY-30)/(20*self.zoom)
        li = int(li)
        cj = int(cj)
        if touche == 'space':
            if self.check.get():
                self.mixte()
            else:
                self.deterministe(['q'])
        else:
            self.deplacement(touche,li,cj)
    
    #init des costs a 0 et affichage dans GUI
    def init_cost(self): 
        mygreen="#1AD22C"
        myblue="#0B79F7"
        #mygrey="#E8E8EB"
        myblack="#5E5E64"
        #mywhite="#FFFFFF"
        myred="#F70B42"
        mytarget="magenta"
        self.w = tk.Label(self.Mafenetre, text='     Costs: ', fg=myblack,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.w.pack(side=tk.LEFT,padx=5,pady=5) 
        self.wg = tk.Label(self.Mafenetre, text=str(self.cost[1]),fg=mygreen,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.wg.pack(side=tk.LEFT,padx=5,pady=5) 
        self.wb = tk.Label(self.Mafenetre, text=str(self.cost[2]),fg=myblue,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.wb.pack(side=tk.LEFT,padx=5,pady=5) 
        self.wr = tk.Label(self.Mafenetre, text=str(self.cost[3]),fg=myred,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.wr.pack(side=tk.LEFT,padx=5,pady=5) 
        self.wn = tk.Label(self.Mafenetre, text=str(self.cost[4]),fg=myblack,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.wn.pack(side=tk.LEFT,padx=5,pady=5) 
        self.wm = tk.Label(self.Mafenetre, text=str(self.cost[5]),fg=mytarget,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.wm.pack(side=tk.LEFT,padx=5,pady=5)                
        self.ws = tk.Label(self.Mafenetre, text='     total = '+str(self.cost[0]),fg=myblack,font = "Verdana "+str(int(5*self.zoom))+" bold")
        self.ws.pack(side=tk.LEFT,padx=5,pady=5) 
    

#decommenter pour afficher
#pblanc=0.1
#pverte=0.3
#pbleue=0.25
#prouge=0.2
#pnoire=0.15
#g = Grille_chiffre(10,10,3,pblanc,pverte,pbleue,prouge,pnoire,1000)
#g.Mafenetre.mainloop()
