
GUI : 
Pour l'interface graphique si python3 modifier Tkinter par tkinter (sans majuscules)

On a deux sortes de grille :
	- sans chiffre (grille.py)
	- avec chiffres (grille_avec_chiffre.py)
	
Pour les lancer aller dans le fichier correspondant et décommenter les lignes commentées
Dans la grille basique on a trois bouttons, chacun executant un algorithme et affiche le résultat dans la zone de texte

Les déplacements peuvent se faire manuellement aux clavier à l'aide des touches a,q,l et m, ou bien de façon automatique avec la touche espace. Le comportement du pion ne sera pas le même avec l'utilisation d'espace selon que la case mixte soit cochée ou non. Dans un premier cas, on aura un déplacement déterministe vers le bas, dans le second on aura un déplacement mixte.

ALGO : 
Dans le fichier algos.py on a tout nos algorithmes, pour les tester il faut d'abord initialiser une grille et ensuite appelé la fonction voulue (exemple dans le fichier source)

etude_impact.py : 
Ce module recense les éléments de code permettant de répondre aux questions de la partie 2 :  étudier l'impact des paramètres, afficher les dataframes et tracer les courbes correspondants, changer les fonctions de couts et visualiser rapidement leur impact sur les politiques. 

p3.py :
Ce module a un role similaire au module précédent, mais pour la partie 3. Y sont codés des fonctions d'exploration et de comparaison des résultats.

outils.py :
Ce module comprend les fonctions techniques permettant le bon fonctionnement du reste des modules : le calcul des probabilités de déplacements, le calcul des couts dans les cas des déplacements probabilisés, et d'autres fonctions utilitaires du même type.


