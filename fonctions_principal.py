from fltk import *
from math import *
from pathlib import Path
from time import *
from random import *
import collections
import heapq


WIDTH = 800
HEIGHT = 800

CASE_WIDTH = 18
CASE_HEIGHT = 18



class Voiture:
    def __init__(self,map):
        self.map = map
        self.trajectoire = []
        

    def vitesse(self,trajectoire):
        """renvoie le vecteur vitesse de la voiture
        param: trajectoire: lst de coordonées """
        if len(trajectoire) < 2:
            return (1,0)
        else:
            x1,y1 = trajectoire[-1]
            x2,y2 = trajectoire[-2]
            x = x1 - x2
            y = y1 - y2
            return (x,y)
   
    
    def verif_collision(self,coord):
        """verifie que le couple debut et le couple fin n'entre pas en colision (#) avec un objet renvoir True si il y a collision false sinon"""
        x,y = coord
        
        if x < 0 or x >= len(self.map[0]) or y < 0 or  y >= len(self.map) or self.map[y][x] == "#"  :
            return True
        else :
            return False
       

    def verif_collision_n2(self,coord,vect):
        """verification des collision de niveaux 2, on ne peut passer a traver les mur
        renvoie true si on passe/touche un mur et false sinon"""
        x,y = coord
        i,j = vect
        for v in range(abs(j)+1):
            for w in range(abs(i)+1):
                if self.verif_collision((x+self.sign(i)*w,y+self.sign(j)*v)) :
                    return True            
        return False
    
    def sign(self,num):
        """renvoie 1 si nombre possitif et -1 si nombre négatif (le signe du nombre)"""
        if num==0:
            return 0
        if num>0:
            return 1
        else:
            return -1
    
    def verif_max(self,a,b):
        """verifier quelle est le plus grand nombre poisif/négatif """
        maxi = self.plus_grand(a,b)
        mini = self.plus_petit(a,b)
        if mini <0:
            mini = - mini
        return self.plus_grand(maxi,mini)


    def plus_grand(self,a,b):
        """renvoie le plus grand nombre"""
        if a > b:
            return a
        else:
            return b
    
    def plus_petit(self,a,b):
        """verifie le plus petit nombre"""
        if a < b:
            return a
        else:
            return b


    def prochain_emplacement(self,coord_voiture,vitesse): 
        """calcule l'emplacement suivant de la voiture si il ne fait rien
        param:
            - coord_voiture : tuple avec coordonée de l'emplacmeent de la voiture 
            - vect: un vecteur qui represente la vitesse de la voiture"""
        x_v,y_v = coord_voiture
        x_vect,y_vect = vitesse
        x,y = x_v+x_vect,y_v+y_vect 
        return (x,y)
        
        

    def options(self,coord_voiture) :
        """return un liste des option possible pour decelerer ou accelerer"""
        lst_option = []
        temp  = [(coord_voiture[0]-1,coord_voiture[1]-1),(coord_voiture[0],coord_voiture[1]-1),(coord_voiture[0]+1,coord_voiture[1]-1),
            (coord_voiture[0]-1,  coord_voiture[1]),(coord_voiture[0],  coord_voiture[1]),(coord_voiture[0]+1,  coord_voiture[1]),
            (coord_voiture[0]-1,coord_voiture[1]+1),(coord_voiture[0],coord_voiture[1]+1),(coord_voiture[0]+1,coord_voiture[1]+1)]
        
        for x,y in temp:
            if (self.verif_collision((x,y)) == False) and ((x,y) not in self.trajectoire) :
                lst_option.append((x,y))

        return lst_option

    
    def appuie_options(self,casex,casey,lst_option):
        """en fonction de si on a apuié sur une option la prend dans la trajectoire"""
        if (casex,casey) in lst_option:
            self.trajectoire.append((casex,casey))


    def gagner(self,next_stop):
        """verifie  si la fin est sur l'arrivé (*) renvoie true si point sur un case gagante et flase sinon"""
        casex,casey = next_stop   
        
        if not (casex < 0 or casey < 0 or (casex >= len(self.map[0]) or casey >= len(self.map))) and self.map[casey][casex] == "*":
            return True
        else :
            return False
        
        
        
    def perdu(self,next_stop):
        """renvoie true si on a perdue"""
        casex,casey = next_stop
        if casex < 0 or casey < 0 or (casex >= len(self.map[0]) or casey >= len(self.map)) or self.map[casey][casex] =="#" :
            return True
        return False


class Affichage:
    def __init__(self,url)  :
        self.rayon = 5
        self.voiture_pose = False
        self.map = self.charger_fichier(url)
        self.voiture = Voiture(self.map)

        if len(self.map[0]) == len(self.map):

            self.map_width = len(self.map[0])
            self.map_height = len(self.map)

            self.case_width = WIDTH/self.map_width
            self.case_height = HEIGHT/self.map_height
        else:
            self.case_width = CASE_WIDTH
            self.case_height = CASE_HEIGHT
            


    def charger_fichier(self,url) : 
        """
        charge dans une liste un fichier texte 
        param: url d'un fichier pour le lire 
        --> return matrice
        """
        matrice = []
        mon_fichier = Path(url)
        with mon_fichier.open('r') as map: 
            contenu = map.readlines() 
            for string in contenu: 
                matrice.append(list(string[:-1]))
        

        for liste in matrice:
            for caractere in liste:
                if caractere not in [">","*", "#","."]: 
                    return None
        
        return matrice 
    
    def affichage_graphique(self,matrice): 
        """prend la matrice representant la map et l'affiche en fltk 
            affiche aussi la voiture si on l'a placé 
            param : matrice : matrice de symbole representant la map
            --> return None """
        x = 0
        y = 0
        for liste in matrice: 
            for caractère in liste: 
                if caractère == "#": 
                    rectangle(x,y,x+self.case_width,y+self.case_height,remplissage = "green")
                if caractère == ".":
                    rectangle(x,y,x+self.case_width,y+self.case_height,remplissage = "white")
                if caractère == ">": 
                    rectangle(x,y,x+self.case_width,y+self.case_height,remplissage = "RoyalBlue4") 
                    
                if caractère == "*":
                    rectangle(x,y,x+self.case_width,y+self.case_height,remplissage = "gray")
                
                rectangle(2,2,70,40)
                texte(34,19,"menu",ancrage = "center",taille = 20)

                x+= self.case_width
            x=0
            y+= self.case_height



    def option(self,lst_option): 
        """affiche les points autour de la voiture pour les différentes options possibles """
        if lst_option != []:
            for (x,y) in lst_option:
                cercle((x) * self.case_width,(y)*self.case_height,self.rayon,remplissage = "black")

    def vitesse(self,trajectoire):
        """affiche le vercteur vitesste de la voiture"""
        for i in range(len(trajectoire)-1):
            x,y = self.voiture.vitesse([trajectoire[i],trajectoire[i+1]])

            if 1 < abs(x) < 3 or 1 < abs(y) < 3 :
                color = "purple"
            if abs(x) <= 1 and abs(y) <= 1: 
                color = "blue"
            if abs(x) >= 3 or abs(y) >= 3: 
                color = "red"

            cercle(trajectoire[i][0]*self.case_width,trajectoire[i][1]*self.case_height,self.rayon,remplissage = color,tag="Voiture")
            ligne(trajectoire[i][0]*self.case_width,trajectoire[i][1]*self.case_height,
                  trajectoire[i+1][0]*self.case_width,trajectoire[i+1][1]*self.case_height,
                  couleur = color,epaisseur = 3,tag ="Voiture")
    

class Manuel:

    def __init__(self,url,regle):
        ### donnée necessaire  

        self.debut = False
        self.lst_option = []
        self.perdu_fenetre = False
        self.man_fenetre = True
        self.gagner_fenetre = False
        self.affichage = Affichage(url)
        self.matrice = self.affichage.charger_fichier(url)
        self.voiture = Voiture(self.matrice)
        self.regle = regle

      

        if len(self.matrice[0]) == len(self.matrice):

            self.map_width = len(self.matrice[0])
            self.map_height = len(self.matrice)

            self.case_width = WIDTH/self.map_width
            self.case_height = HEIGHT/self.map_height
            self.width = WIDTH
            self.height = HEIGHT
        else:

            self.case_width = CASE_WIDTH
            self.case_height = CASE_HEIGHT

            self.width = len(self.matrice[0])*CASE_WIDTH
            self.height = len(self.matrice)*CASE_HEIGHT

        
        ### fenetre graphique 
        ferme_fenetre()
        cree_fenetre(self.width,self.height)

        self.man()


    def man(self):
        while self.man_fenetre: 
            self.afficher_objet()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == "Quitte": 
                self.man_fenetre = False

            self.gerer_evenement(ev,ty)

            if self.affichage.voiture_pose: # si on a poser la voiture et donc entrain de jouer
                #self.lst_option = self.voiture.options(self.voiture.trajectoire[-1])

                vitesse = self.voiture.vitesse(self.voiture.trajectoire) 

                next_stop = self.voiture.prochain_emplacement(self.voiture.trajectoire[-1],vitesse)
                
                if self.regle == "regle_stricte":
                    bool = self.voiture.verif_collision_n2(self.voiture.trajectoire[-1],vitesse)
                else :
                    bool = self.voiture.verif_collision(self.voiture.trajectoire[-1])

                if not bool :
                    self.lst_option = self.voiture.options(next_stop)


                    if self.voiture.gagner(next_stop) == True:
                        self.gagner_fenetre = True
                        self.man_fenetre = False
                        self.fenetre_gagner()


                    if self.voiture.perdu(next_stop) == True:
                        ev = attend_ev()
                        ty = type_ev(ev)
                        if ty == "Touche":
                            t = touche(ev)
                            if t  == ("Control_L" and  "z"): 
                                self.voiture.trajectoire.pop()

                        elif ty == "ClicGauche":
                            self.perdu_fenetre = True
                            self.fenetre_perdu()
                            self.man_fenetre = False

        
            
    def afficher_objet(self): 
        efface_tout()
        self.affichage.affichage_graphique(self.matrice)
        self.affichage.option(self.lst_option)
        if len(self.voiture.trajectoire) > 1:
            self.affichage.vitesse(self.voiture.trajectoire)
        mise_a_jour()

    def gerer_evenement(self,ev,ty):

        if ty == "ClicGauche" : 
            x = abscisse(ev)
            y = ordonnee(ev)
            casex = int(x//self.case_width)
            casey = int(y//self.case_height)
            if self.matrice[casey][casex] == ">":
                self.affichage.voiture_pose = True
                self.voiture.trajectoire.append((casex,casey))
            self.voiture.appuie_options(casex,casey,self.lst_option)

            if (2 <= x <= 70) and (2 <= y <= 40):
                    self.man_fenetre = False
                    ferme_fenetre()
                    Menu()

        if ty == "Touche":
            t = touche(ev)
            if t  == ("Control_L" and  "z"): 
                self.voiture.trajectoire.pop()

    def fenetre_perdu(self):
        """ouvre une fenetre des qu'on a perdu pour rejouer"""
        ferme_fenetre()
        cree_fenetre(WIDTH,HEIGHT)
        while self.perdu_fenetre:

            efface_tout()
            rectangle(2,2,70,40,remplissage = "skyblue")
            texte(34,19,"menu",ancrage = "center",taille = 20)
            texte(WIDTH/2,HEIGHT/2,"PERDU",ancrage = "center")
            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == "Quitte":
                self.perdu_fenetre = False

            if ty == "ClicGauche":
                x,y = (abscisse(ev),ordonnee(ev))

                if (2 <= x <= 70) and (2 <= y <= 40):
                    ferme_fenetre()
                    self.perdu_fenetre = False
                    Menu()

    def fenetre_gagner(self):
        ferme_fenetre()
        cree_fenetre(WIDTH,HEIGHT)
        while self.gagner_fenetre:

            efface_tout()
            rectangle(2,2,70,40,remplissage = "skyblue")
            texte(34,19,"menu",ancrage = "center",taille = 20)
            texte(WIDTH/2,HEIGHT/2,"Gagner",ancrage = "center")
            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == "Quitte":
                break

            if ty == "ClicGauche":
                x,y = (abscisse(ev),ordonnee(ev))

                if (2 <= x <= 70) and (2 <= y <= 40):
                    ferme_fenetre()
                    self.gagner_fenetre = False
                    Menu()

  
class Solveur: 
    def __init__(self,url,mdj,aleatoire,aff,regle) -> None:
        self.url = url #fichier de la map 
        self.mdj = mdj # solveur activé ou desactivé
        self.aleatoire = aleatoire # parcours aleatoire ou normal
        self.aff = aff # affichage fin ou complet
        self.regle = regle # regle souple ou stricte


        self.dico_visite = {"visite":[],"vitesse":[]}
        self.visite = set()
        self.trajectoire = []
        self.lst_option = []
        self.lst_chemin = []
        self.booleen = None # bool pour le solveur 
        self.depart = False
        self.chemin = [] # le chemin de fin 
        self.affichage = Affichage(self.url) 
        self.matrice = self.affichage.charger_fichier(self.url)
        self.voiture = Voiture(self.matrice)
        self.dp_al = self.depart_aleatoire()
        self.tuple = None 


        
        

    def main_solveur(self):
        """main du solveur qui gere toute les options et appelle les fonctions """

        
        if len(self.matrice[0]) == len(self.matrice):

            self.map_width = len(self.matrice[0])
            self.map_height = len(self.matrice)

            self.case_width = WIDTH/self.map_width
            self.case_height = HEIGHT/self.map_height
            self.width = WIDTH
            self.height = HEIGHT
        else:

            self.case_width = CASE_WIDTH
            self.case_height = CASE_HEIGHT

            self.width = len(self.matrice[0])*CASE_WIDTH
            self.height = len(self.matrice)*CASE_HEIGHT

        ### fenetre graphique 
        ferme_fenetre()
        cree_fenetre(self.width,self.height)

        if self.trajectoire == []:
                acc = 1
                for i in range(len(self.matrice[0])):
                    for j in range(len(self.matrice)):
                        if self.matrice[j][i] == ">" and self.depart == False and acc==self.dp_al :
                            self.depart = True
                            self.trajectoire.append((i,j))
                        if self.matrice[j][i] == ">":
                            acc+=1

        if self.mdj == "profondeur" :
            trajectoire = self.niveau1_bis(self.trajectoire,self.aleatoire)
         
           

            self.affiche_objet(self.chemin)

        elif self.mdj == "largeur":
            

            self.files = collections.deque([(self.trajectoire[0],[self.trajectoire[0]])])

            bool,trajectoire = self.niveaux2(self.files,self.aleatoire,True)
            self.affiche_objet(self.chemin)
        
        elif self.mdj == "A*":
            a_etoile = self.A_etoile(self.matrice,self.trajectoire[-1],0,self.url)
            bool,trajectoire = a_etoile.main(self.url)
            self.affiche_objet(trajectoire)

        elif self.mdj == "tirage":
            lst = self.tirage_du_meilleur(self.trajectoire)
            self.affiche_objet(lst)
            
        attend_ev()
        ferme_fenetre()
        Menu()

    
   

    def niveau1(self,visite,trajectoire,aleatoire):
        """solveur de niveaux 1 cherche juste si il y a une sortie au parcour"""
        if self.aff == "aff_complet":
            self.affiche_objet(trajectoire)

        if trajectoire == []:
            acc = 1
            for i in range(len(self.matrice[0])):
                for j in range(len(self.matrice)):
                    if self.matrice[j][i] == ">" and self.depart == False and acc==self.dp_al :
                        self.depart = True
                        trajectoire.append((i,j))
                    if self.matrice[j][i] == ">":
                        acc+=1
        if trajectoire == []:
            return (False,[])
        
        vitesse = self.voiture.vitesse(trajectoire) 
        next_stop = self.voiture.prochain_emplacement(trajectoire[-1],vitesse)
        x,y = next_stop

        if x < 0 or y < 0 or x > len(self.matrice[1])-1 or y > len(self.matrice)-1:
            trajectoire.pop()
            return(False,trajectoire)

        if self.regle == "regle_stricte":
            bol = self.voiture.verif_collision_n2(trajectoire[-1],vitesse) 
        else:
            bol = self.voiture.verif_collision(trajectoire[-1])
        
        if not bol: 
            if self.voiture.gagner(next_stop) == True or self.matrice[trajectoire[-1][1]][trajectoire[-1][0]] == "*":
                chemin = trajectoire
                if self.matrice[next_stop[1]][next_stop[0]] == "*":
                    chemin.append(next_stop)
                self.chemin = chemin
                return (True,trajectoire)

            self.lst_option=self.voiture.options(next_stop)

            c =  (trajectoire[-1])
            
            if c in visite["visite"] :
                index = visite["visite"].index(c)
            else :
                index = False
            if index == False:
                if c in visite["visite"] :
                    return (False,trajectoire)
                else: 
                    visite["visite"].append(c)
                    visite["vitesse"].append(self.voiture.vitesse(trajectoire))
            else : 
                if c in visite["visite"] or vitesse >= visite["vitesse"][index] :
                    return (False,trajectoire)
                else: 
                    visite["visite"].append(c)
                    visite["vitesse"].append(self.voiture.vitesse(trajectoire))

           
            #suffle la lst pour que les voisin ne soivent jamais dans le meme ordre
            if aleatoire ==  "aleatoire":
                self.lst_option = self.sufle_lst(self.lst_option)

            for option in self.lst_option:
                if (self.regle == "regle_stricte") :
                    if  (not self.voiture.verif_collision_n2(trajectoire[-1],(option[0]-trajectoire[-1][0],option[1]-trajectoire[-1][1]))):
                        nouvelle_trajectoire = trajectoire + [option]
                        self.tuple = self.niveau1(visite,nouvelle_trajectoire,aleatoire)
                else: 
                    nouvelle_trajectoire = trajectoire + [option]
                    self.tuple = self.niveau1(visite,nouvelle_trajectoire,aleatoire)

                
                if self.chemin != []:
                    break

            if self.tuple:
                return (self.tuple,trajectoire)
            else:
                trajectoire.pop()
                return (False,trajectoire)

        else :
            trajectoire.pop()
            return (False,trajectoire)


    def niveau1_bis(self,trajectoire,aleatoire):
        """solveur de niveaux 1 cherche juste si il y a une sortie au parcours"""
        if self.aff == "aff_complet":
            self.affiche_objet(trajectoire)

        
        vitesse = self.voiture.vitesse(trajectoire) 
        next_stop = self.voiture.prochain_emplacement(trajectoire[-1],vitesse)
        x,y = next_stop

        if x < 0 or y < 0 or x > len(self.matrice[1])-1 or y > len(self.matrice)-1:
            trajectoire.pop()
            return trajectoire

        if self.regle == "regle_stricte":
            bol = self.voiture.verif_collision_n2(trajectoire[-1],vitesse) 
        else:
            bol = self.voiture.verif_collision(trajectoire[-1])
        
        if not bol: 
            if self.voiture.gagner(next_stop) == True or self.matrice[trajectoire[-1][1]][trajectoire[-1][0]] == "*":
                if self.matrice[next_stop[1]][next_stop[0]] == "*":
                    trajectoire.append(next_stop)
                self.chemin = trajectoire
                self.lst_chemin.append(self.chemin)
                return trajectoire

            self.lst_option=self.voiture.options(next_stop)

            c = (trajectoire[-1],vitesse)


            #suffle la lst pour que les voisin ne soivent jamais dans le meme ordre
            if aleatoire ==  "aleatoire":
                self.lst_option = self.sufle_lst(self.lst_option)

            for option in self.lst_option:
                if ((option,vitesse) not in self.visite) and (c not in self.visite) and (option not in trajectoire):
                    self.visite.add((option,vitesse))
                    if (self.regle == "regle_stricte")  :
                        if  (not self.voiture.verif_collision_n2(trajectoire[-1],(option[0]-trajectoire[-1][0],option[1]-trajectoire[-1][1]))):
                            self.tuple = self.niveau1_bis(trajectoire + [option],aleatoire)
                    else: 
                        self.tuple = self.niveau1_bis(trajectoire + [option],aleatoire)

                if self.chemin != []:
                        break
        
        return trajectoire
            
  
    def sufle_lst(self,lst):
        """suffle de facon aleatoire une lst"""
        for __ in range(2*len(lst)):
            i1 = randint(0,len(lst)-1)
            i2 = randint(0,len(lst)-1)
            elm1 = lst[i1]
            elm2 = lst[i2]
            lst[i1] = elm2
            lst[i2] = elm1
        return lst

    def niveaux2(self,files,aleatoire,affichage):
        while files:
            if affichage == True:
                ev = donne_ev()
                ty = type_ev(ev)
                if ty == "Quitte":
                    return False
                
                if ty == "ClicGauche":
                    x,y = (abscisse(ev),ordonnee(ev))
                    
                    if (2 <= x <= 70) and (2 <= y <= 40):
                        ferme_fenetre()
                        Menu()

            emplacement_actuel,chemin  = files.popleft()

            if self.aff == "aff_complet":
                self.affiche_objet(chemin)

            vitesse = self.voiture.vitesse(chemin)
            next_stop = self.voiture.prochain_emplacement(emplacement_actuel,vitesse)

            if self.regle == "regle_stricte":
                bol = self.voiture.verif_collision_n2(chemin[-1],vitesse)
            else:
                bol = self.voiture.verif_collision(chemin[-1])

            if  (not bol) and (not self.voiture.perdu(next_stop) ):

                if self.voiture.gagner(next_stop) == True: 
                    files.append((next_stop,chemin+[next_stop]))
                    self.chemin = chemin
                    self.chemin.append(next_stop)
                    return (True,self.chemin)

                self.lst_option = self.voiture.options(next_stop)


                if aleatoire ==  "aleatoire":
                    self.lst_option = self.sufle_lst(self.lst_option)
                

                for option in self.lst_option:
                    if (self.regle == "regle_stricte") and ((option,vitesse) not in self.visite)  :
                        if  (self.voiture.verif_collision_n2(chemin[-1],(option[0]-chemin[-1][0],option[1]- chemin[-1][1])) == False):
                            self.visite.add((option,vitesse))
                            files.append((option,chemin + [option]))
                    elif (option,vitesse) not in self.visite:
                        self.visite.add((option,vitesse))
                        files.append((option,chemin + [option]))
                        
        return (False,[])
    
    def tirage_du_meilleur(self,lst):
        """solveur qui lance beaucoup de fois le solveur aleatoire et prend le meilleur"""
        taille_chemin  = []
        lst_diff_chemin = []
        for _ in range(500):
            trajectoire = self.niveau1_bis(lst,"aleatoire")
        for i in range(len(self.lst_chemin)):
            lst_diff_chemin.append(self.lst_chemin[i])
            taille_chemin.append(len(self.lst_chemin[i]))

        min_len = min(taille_chemin)
        print(min_len)
        for j in range(len(lst_diff_chemin)):
            if taille_chemin[j] == min_len:
                return lst_diff_chemin[j]
            
        
    
    def affiche_objet(self,trajectoire):    
        """affiche tout le solveur""" 
        efface_tout()
        self.affichage.affichage_graphique(self.matrice)
        if len(trajectoire) > 1:
            self.affichage.vitesse(trajectoire)
        mise_a_jour()
    
    def depart_aleatoire(self):
        """renvoie un nombre aléatoire en fonction du nombre de point de départ possible pour un point de départ aléatoire"""
        acc = 0
        for i in range(len(self.matrice[0])):
                for j in range(len(self.matrice)):
                    if self.matrice[j][i] == ">" :
                        acc+=1
        return randint(1,acc)
    

    ### a modifier solon la version extern
    class A_etoile():
        def __init__(self,map,start,end,url) -> None:
            self.map = map
            self.start = start
            self.end = end
            self.voiture = Voiture(map)
            
        class Node:
            def __init__(self, position, parent=None):
                self.position = position
                self.parent = parent
                self.g = 0  # Distance du début au nœud courant
                self.h = 0  # Heuristique : estimation de la distance du nœud courant à la fin
                self.f = 0  # Coût total (g + h)

            def __eq__(self, other):
                """renvoie true si la position est la meme que l'autre position et fase sinon"""
                return self.position == other.position

            def __lt__(self, other):
                """renvoie true si la f stocker et plus petit que le f tester et false sinon """
                return self.f < other.f

        def main(self,url):
            """main solveur a *
            revoie true et le chemin si il y en a un entre le depart et l'arriver 
            sinon renvoie False et []"""
            affichage = Affichage(url)
            map = affichage.charger_fichier(url)
            #a_etoile = A_etoile(map, 0, 0,url)
            acc_dep,acc_arr = self.acc_dep_arrive(map)
            start,end = self.find_start_end(map,acc_dep,acc_arr)
            chemin = self.a_etoile(map, start, end)
            if chemin == None:
                chemin=[]
                return (False,chemin)
            return(True,chemin)


        def heuristic(self,a, b):
            # Utilise la distance de Manhattan comme heuristique
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        def a_etoile(self,map, start, end):
            """main du solveur A * qui resout le chemin"""
            # Crée les nœuds de départ et de fin
            start_node = self.Node(start)
            noeud_end = self.Node(end)

            open_list = []
            closed_list = set()

            # Ajoute le nœud de départ à la liste ouverte (open_list)
            heapq.heappush(open_list, start_node)

            while open_list:
                # Récupère le nœud avec le coût le plus bas (f)
                noeud_courant = heapq.heappop(open_list)
                closed_list.add(noeud_courant.position)

                # Si nous avons atteint le nœud de fin, reconstruit le chemin
                if noeud_courant == noeud_end:
                    path = []
                    while noeud_courant:
                        path.append(noeud_courant.position)
                        noeud_courant = noeud_courant.parent
                    return path[::-1]  # Retourne le chemin à l'envers


                if len(open_list)>1:
                        vitesse = self.voiture.vitesse([noeud_courant.parent.position,noeud_courant.position])
                else:
                    vitesse = (0,0)
                next_stop = self.voiture.prochain_emplacement(noeud_courant.position,vitesse)
                options = self.voiture.options(next_stop)
                
                for option in options:
                    if len(open_list)>1:
                        vitesse = self.voiture.vitesse([noeud_courant.position,option])
                    else:
                        vitesse = (0,0)
                    if (0 <= option[0] < len(map)) and (0 <= option[1] < len(map[0])):
                        if self.voiture.verif_collision_n2(noeud_courant.position,vitesse):  
                            continue

                        voisin_node = self.Node(option, noeud_courant)

                        if voisin_node.position in closed_list:
                            continue

                        voisin_node.g = noeud_courant.g + 1
                        voisin_node.h = self.heuristic(voisin_node.position, noeud_end.position)
                        voisin_node.f = voisin_node.g + voisin_node.h

                        if self.add_to_open_list(open_list, voisin_node):
                            heapq.heappush(open_list, voisin_node)

            return None  # Retourne None si aucun chemin n'a été trouvé

        def add_to_open_list(self,open_list, voisin):
            for node in open_list:
                if voisin == node and voisin.g > node.g:
                    return False
            return True

        def find_start_end(self,map,dep_radom,arr_random):
            start = None
            end = None
            acc_dep,acc_arr=0,0
            for j in range(len(map)):
                for i in range(len(map[0])):
                    if map[j][i] == '>':
                        acc_dep+=1
                    elif map[j][i] == '*':
                        acc_arr+=1
                    if map[j][i] == '>'and dep_radom == acc_dep:
                        start = (i, j)
                    elif map[j][i] == '*' and acc_arr== arr_random:
                        end = (i, j)
                    
            return start, end
        

        def acc_dep_arrive(self,matrice):
            """compte le nombre de point de depart et d'arriver"""
            acc_dep = 0
            acc_arr = 0
            for j in range(len(matrice)):
                for i in range(len(matrice[j])):
                    if matrice[j][i]==">":
                        acc_dep+=1
                    if matrice[j][i]=="*": 
                        acc_arr+=1

            acc_dep = randint(1,acc_dep)
            acc_arr = randint(1,acc_arr)
            return acc_dep,acc_arr


class Menu: 

    def __init__(self) :
        self.width_espacement = 100
        self.height_espacement = 100
        self.largeur_rectangle = int(WIDTH/3)
        self.hauteur_rectangle = int(HEIGHT/9)
        
        self.x_margin = 40
        self.y_margin = 40

        self.available_width = WIDTH - 2 * self.x_margin
        self.available_height = HEIGHT - 2 * self.y_margin
        self.width_espacement = int((self.available_width - 2 * self.width_espacement) / 3)
        self.height_espacement = int((self.available_height - self.height_espacement) / 3)

        

        self.texte_main = ["jouer","changer_map" ,"solveur","regle/info"]
        self.texte_map = [["map_mini","map_test"],["map_random","map1"],["map3","map2"]]
        self.texte_solveur_cercle = [["profondeur","largeur"],["A*","tirage"]]
        self.texte_solveur_rectangle = [["active","desactive"],["aleatoire","normal"],
                                        ["aff_fin","aff_complet"],["regle_souple","regle_stricte"]]
        
        self.dico_rayon = {}
        self.coord_main = {}
        self.coord_map = {}
        self.coord_solveur_cercle = {}
        self.coord_solveur_rectangle = {}
        self.rayon = WIDTH/11


        self.main_fenetre = True
        self.changer_map_fenetre = False
        self.solveur_fenetre = False
        self.info_fenetre = False

        self.img = None
        cree_fenetre(WIDTH,HEIGHT)
        self.mainloop()
        #ferme_fenetre()


    def main_affichage(self): 
        """affiche les rectangle pour le choix de menu sur la fenetre """
        x,y = (int(WIDTH/2) - 150, 40)
        
        for i in range(len(self.texte_main)):
            lst_point = [(x+10,y),(x+self.largeur_rectangle-10,y),(x+self.largeur_rectangle,y+10),
                         (x+self.largeur_rectangle,y+self.hauteur_rectangle-10),(x+self.largeur_rectangle-10,y+self.hauteur_rectangle),
                         (x+10,y+self.hauteur_rectangle),(x,y+self.hauteur_rectangle-10),(x,y+10)]
            polygone(lst_point,remplissage = "#3D59AB",epaisseur = 5 )
            texte(x + (self.largeur_rectangle/2),y+(self.hauteur_rectangle/2),
                    self.texte_main[i],ancrage = "center",taille= int(WIDTH/30),couleur ="white" )
            self.coord_main[self.texte_main[i]] = (x,y)
            x = int(WIDTH/2) - 150

            y += self.height_espacement 


    def mainloop(self):
        """fenetre principal qui renvoit au différentes fonction selon ce que l'on veut """
        while self.main_fenetre:
            efface_tout()
            try :
                image(x = WIDTH/2,y = HEIGHT/2,fichier = "media/fond/main_fond.png",ancrage='center',tag = "img")
            except :
                pass
            self.main_affichage()
            self.retour_menu()
            mise_a_jour()

            ev = donne_ev()
            ty = type_ev(ev)

            if ty == "Quitte":
                self.main_fenetre = False
                
            if ty == "ClicGauche": 
                x,y = (abscisse(ev),ordonnee(ev))

                if (self.coord_main["jouer"][0] <= x <= self.coord_main["jouer"][0] + self.largeur_rectangle) and (
                    self.coord_main["jouer"][1] <= y <= self.coord_main["jouer"][1] + self.hauteur_rectangle):
                    
                    self.jouer()
                    self.main_fenetre = False
                    
                    
                if (self.coord_main["changer_map"][0] <= x <= self.coord_main["changer_map"][0] + self.largeur_rectangle) and (
                    self.coord_main["changer_map"][1] <= y <= self.coord_main["changer_map"][1] + self.hauteur_rectangle): 
                    
                    self.changer_map_fenetre = True
                    self.changer_map()
                    self.main_fenetre = False
                    

                if (self.coord_main["solveur"][0] <= x <= self.coord_main["solveur"][0] + self.largeur_rectangle) and (
                    self.coord_main["solveur"][1] <= y <= self.coord_main["solveur"][1] + self.hauteur_rectangle):
                
                    self.solveur_fenetre = True
                    self.solveur()
                    self.main_fenetre = False
                if (self.coord_main["regle/info"][0] <= x <= self.coord_main["regle/info"][0] + self.largeur_rectangle) and (
                    self.coord_main["regle/info"][1] <= y <= self.coord_main["regle/info"][1] + self.hauteur_rectangle):
                    self.info_fenetre  = True
                    self.info_regle()
                    self.main_fenetre = False

                if (2 <= x <= 70) and (2 <= y <= 40):
                    pass


    def jouer(self):
        """fonction pour lancer en fonction des parametres enrengistrés """
        lst_info = self.lire_fichier("option.txt")
        if lst_info[0].strip() == "map_random":
            random_map(40,40)
        if lst_info[1].strip() == "man":
            Manuel(f"media\maps-texte\{lst_info[0].strip()}.txt",str(lst_info[5].strip()))

        elif lst_info[1].strip() == "solveur":
            
            solveur = Solveur(f"media\maps-texte\{lst_info[0].strip()}.txt",
                    str(lst_info[2].strip()),str(lst_info[3].strip()),str(lst_info[4].strip()),
                    str(lst_info[5].strip()))
            solveur.main_solveur()
        
            


    def retour_menu(self): 
        """affichage d'un rectangle pour retourner au menu"""
        rectangle(2,2,70,40,remplissage = "skyblue")
        texte(34,19,"menu",ancrage = "center",taille = 20)
  

    def changer_map(self): 
        """gere une fenetre pour changer la map sur laquelle on veut jouer """
        ferme_fenetre()
        cree_fenetre(WIDTH,HEIGHT)
        while self.changer_map_fenetre:
            efface_tout()
            try :
                image(x = WIDTH/2,y = HEIGHT/2,fichier = "media/fond/main_fond_2.png.png",ancrage='center',tag = "img")
            except :
                pass
            
            self.affichage_map()
            self.retour_menu()
            mise_a_jour()
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == "Quitte":
                break
            if ty == "ClicGauche":
                x,y = (abscisse(ev),ordonnee(ev))
                for cle in self.coord_map:
                    if (self.coord_map[cle][0] - self.rayon <= x <= self.coord_map[cle][0] + self.rayon) and (
                        self.coord_map[cle][1] - self.rayon <= y <= self.coord_map[cle][1] + self.rayon):                        
                        self.ecrire_fichier(cle,0,"option.txt")
                        
                if (2 <= x <= 70) and (2 <= y <= 40):
                    self.changer_map_fenetre = False
                    self.mainloop()
                    

    def affichage_map(self): 
        """affiche les elements pour changer la map"""
        x,y = (WIDTH/2-180,100)
        lst_info = self.lire_fichier("option.txt")
        
        for i in range(len(self.texte_map)): 

            for j in range(len(self.texte_map[i])):
                rayon = self.taille_rayon(self.texte_map[i][j])
                self.coord_map[self.texte_map[i][j]] = (x,y)
                self.dico_rayon[self.texte_map[i][j]] = rayon

                if lst_info[0].strip() == self.texte_map[i][j]:
                    couleur = "pink"
                else:
                    couleur = "#3D59AB"

                cercle(x,y,rayon,remplissage = couleur)
                texte(x,y,self.texte_map[i][j],ancrage = "center",taille = int(WIDTH/50),couleur = "white")
                x+=self.width_espacement + 150
            x = 200
            y += self.height_espacement + 76


    def solveur(self):
        ferme_fenetre()
        cree_fenetre(WIDTH,HEIGHT)
        while self.solveur_fenetre:
            efface_tout()
            try :
                image(x = WIDTH/2,y = HEIGHT/2,fichier = "media/fond/main_fond_3.png",ancrage='center')
            except :
                pass
            
            self.affichage_solveur()
            self.retour_menu()
            mise_a_jour()
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == "Quitte":
                break
            if ty == "ClicGauche":
                x,y = (abscisse(ev),ordonnee(ev))
                for cle in self.coord_solveur_cercle: 
                    rayon = self.dico_rayon[cle]
                    if (self.coord_solveur_cercle[cle][0] - rayon <= x <= self.coord_solveur_cercle[cle][0] + rayon) and (
                        self.coord_solveur_cercle[cle][1] - rayon <= y <= self.coord_solveur_cercle[cle][1] + rayon) :
                        self.ecrire_fichier(cle,2,"option.txt")

                if (self.coord_solveur_rectangle["active"][0] <= x <= self.coord_solveur_rectangle["active"][0] + 50) and (
                    self.coord_solveur_rectangle["active"][1] <= y <= self.coord_solveur_rectangle["active"][1] + 40) :
                    self.ecrire_fichier("solveur",1,"option.txt")
                
                elif (self.coord_solveur_rectangle["desactive"][0] + 50 <= x <= self.coord_solveur_rectangle["desactive"][0] + 100) and (
                    self.coord_solveur_rectangle["desactive"][1] <= y <= self.coord_solveur_rectangle["desactive"][1] + 40) :
                    self.ecrire_fichier("man",1,"option.txt")
                
                if (self.coord_solveur_rectangle["aleatoire"][0]  <= x <= self.coord_solveur_rectangle["aleatoire"][0] + 50) and (
                    self.coord_solveur_rectangle["aleatoire"][1]  <= y <= self.coord_solveur_rectangle["aleatoire"][1] + 40) :
                    self.ecrire_fichier("aleatoire",3,"option.txt")

                elif (self.coord_solveur_rectangle["normal"][0] + 50 <= x <= self.coord_solveur_rectangle["normal"][0] + 100) and (
                    self.coord_solveur_rectangle["normal"][1]   <= y <= self.coord_solveur_rectangle["normal"][1] + 40) :
                    self.ecrire_fichier("normal",3,"option.txt")
                
                if (self.coord_solveur_rectangle["aff_fin"][0] <= x <= self.coord_solveur_rectangle["aff_fin"][0] + 50) and (
                    self.coord_solveur_rectangle["aff_fin"][1]   <= y <= self.coord_solveur_rectangle["aff_fin"][1] + 40) :
                    self.ecrire_fichier("aff_fin",4,"option.txt")

                elif (self.coord_solveur_rectangle["aff_complet"][0] + 50 <= x <= self.coord_solveur_rectangle["aff_complet"][0] + 100) and (
                    self.coord_solveur_rectangle["aff_complet"][1]  <= y <= self.coord_solveur_rectangle["aff_complet"][1] + 40) :
                    self.ecrire_fichier("aff_complet",4,"option.txt")
                
                if (self.coord_solveur_rectangle["regle_souple"][0] <= x <= self.coord_solveur_rectangle["regle_souple"][0] + 50) and (
                    self.coord_solveur_rectangle["regle_souple"][1]   <= y <= self.coord_solveur_rectangle["regle_souple"][1] + 40) :
                    self.ecrire_fichier("regle_souple",5,"option.txt")

                elif (self.coord_solveur_rectangle["regle_stricte"][0] + 50 <= x <= self.coord_solveur_rectangle["regle_stricte"][0] + 100) and (
                    self.coord_solveur_rectangle["regle_stricte"][1]  <= y <= self.coord_solveur_rectangle["regle_stricte"][1] + 40) :
                    self.ecrire_fichier("regle_stricte",5,"option.txt") 

                if (2 <= x <= 70) and (2 <= y <= 40):
                    self.mainloop()
                    self.solveur_fenetre = False
            

    def affichage_solveur(self): 
        """tout les elements a afficher sur la fenetre pour gerer le solveur """
        lst_info = self.lire_fichier("option.txt")
        try :
                image(x = WIDTH/2,y = HEIGHT/2,fichier = "media/fond/main_fond_4.png",ancrage='center')
        except :
            pass

        x,y = (WIDTH/2,110)
        for i in range(len(self.texte_solveur_cercle)):
            for j in range(len(self.texte_solveur_cercle[i])):
                rayon = self.taille_rayon(self.texte_solveur_cercle[i][j])
                self.dico_rayon[self.texte_solveur_cercle[i][j]] = rayon

                if self.texte_solveur_cercle[i][j] == lst_info[2].strip():
                    color = "pink"
                else:
                    color = "#3D59AB"

                self.coord_solveur_cercle[self.texte_solveur_cercle[i][j]] = (int(x),int(y))
                cercle(x,y,rayon,"black",remplissage = color,epaisseur = 2)
                texte(x,y,f"{self.texte_solveur_cercle[i][j]}",taille = int(WIDTH/60),ancrage = "center",couleur = "white")
                y+= self.height_espacement - 50
                x+= self.width_espacement +100
            y+= 110
            x = 100

        x1,y1 = (50,HEIGHT/2-300)
        x2,y2 = (50,HEIGHT/2-290)
        for i in range(len(self.texte_solveur_rectangle)):
                for j in range(len(self.texte_solveur_rectangle[i])):
                    if lst_info[1].strip() == "solveur" and j == 0 and i == 0:
                        rectangle(x1,y1,x1+50,y1+40,remplissage = "darkolivegreen3")
                    elif lst_info[1].strip() == "man" and j == 1 and i == 0:
                        rectangle(x1+50,y1,x1+100,y1+40,remplissage = "#6E8B3D")
                    
                    if lst_info[3].strip() == "aleatoire" and j == 0  and i == 1:
                        rectangle(x1,y1,x1+50,y1+40,remplissage = "#CD6600")
                    if lst_info[3].strip() == "normal" and j == 1 and i == 1: 
                        rectangle(x1+50,y1,x1+100,y1+40,remplissage = "#8B4500") 

                    if lst_info[4].strip() == "aff_fin" and j == 0 and i == 2:
                        rectangle(x1,y1,x1+50,y1+40,remplissage = "#79CDCD")
                    if lst_info[4].strip() == "aff_complet" and j == 1 and i == 2:
                        rectangle(x1+50,y1,x1+100,y1+40,remplissage = "#528B8B") 

                    if lst_info[5].strip() == "regle_souple" and j == 0 and i == 3:
                        rectangle(x1,y1,x1+50,y1+40,remplissage = "#808080")
                    if lst_info[5].strip() == "regle_stricte" and j == 1 and i == 3:
                        rectangle(x1+50,y1,x1+100,y1+40,remplissage = "#030303") 


                    texte(x2,y2+40,self.texte_solveur_rectangle[i][j],taille = int(WIDTH/60),ancrage = "center")
                    self.coord_solveur_rectangle[self.texte_solveur_rectangle[i][j]] = (int(x1),int(y1))
                    x2 += self.width_espacement -10
                    y2 = y1

                
                rectangle(x1,y1,x1+100,y1+40)
                x1 += self.width_espacement
                y1 += self.height_espacement - 50
                x2 = x1
                y2 = y1
                    
            

            

    def lire_fichier(self,fichier): 
        """lis le fichier recu en param et renvoie le contenu sinon None
        param : fichier : le fichier qu'on veut lire(fichier.txt) 
        --> return contenu du fichier 
        """
        try :
            with open(str(fichier),"r") as r: 
                contenu = r.readlines()
                return contenu
                                                        
        except FileNotFoundError:
            print(f"Le fichier {fichier} n'existe pas.")
            return None


    def ecrire_fichier(self,valeur,numero,fichier):
        """ecrit dans un fichier un valeur pour la stocker
        params:  valeur: la valeur a stocket
                numero : numero de la ligne ou l'on doit ecrire
                fichier : le nom du fichier ou le chemin relatif
        return None 
        """
        liste_info = self.lire_fichier("option.txt")
        liste_info[numero] = valeur +"\n"
        with open(fichier,"w") as f: 
            for string in liste_info:
                f.write(string)


    def taille_rayon(self,string):
        """modifie la taille de self.rayon en fonction de la longeur du texte a l'interieur
        param : string : texte a mettre dans le cercle """
        longueur = len(string)
        rayon = self.rayon
        # 7 car si le mot fait 7 lettre ca rentre parfaitement dans un cercle de rayon 70
        if longueur <= 7 :
            rayon = WIDTH/11

        elif longueur > 7:
            rayon = self.rayon + (longueur-7) * 10
        return rayon

    def info_regle(self):
        """ouvre une fentre qui explique les regles en lisant un fichier"""
        ferme_fenetre()
        cree_fenetre(WIDTH,HEIGHT)
        

        while self.info_fenetre:
            efface_tout()
            self.retour_menu()
            self.affichage_info()
            mise_a_jour()
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == "Quitte":
                self.info_fenetre = False
            if ty == "ClicGauche":
                x1,y1 = (abscisse(ev),ordonnee(ev))
                if (2 <= x1 <= 70) and (2 <= y1 <= 40):
                    self.main_fenetre = True
                    self.mainloop()
                    self.info_fenetre = False

            
            
    def affichage_info(self):
        """affichage pour les info_regle """
        titre = "regle du jeu"
        liste_texte = [ ["pour changer les paramètres comme activé le solveur"],
                        ["ou changer les regles veuillez vous rendre dans solveur"],
                        ["sinon le lancement ce fait depuis le boutons jouer"],
                        ["sans le solveur les regles sont simples: c'est un jeu "],
                        ["de voiture, en partant d'un point de depart (en bleu)"], 
                        ["il faut arriver a l'arrivée (en gris) la voiture va au"],
                        ["point suivant si nous changons rien, mais nous pouvons"],
                        ["modifier la vitesse de 1 case en appuyant sur les options"],
                            ["Bon courage et c'est parti !!!!!"]]
        
        x,y = (WIDTH/2,200)
        texte(WIDTH/2,50,titre,ancrage = "center")
        for i in range(len(liste_texte)):
            for j in range(len(liste_texte[i])):
                texte(x,y,liste_texte[i][j],taille = 20,ancrage = "center")
            
            y+=50


class random_map:
    def __init__(self,nb_ligne,nb_colone) -> None:
        self.nb_ligne = nb_ligne
        self.nb_colone = nb_colone
        self.set = set()
        self.dep = []
        self.matrice = []
        self.p_loin = (0,0)
        self.main()
       

    def main(self):
        """main qui genere une map aléatoire"""
        #permet de genret la map aleatoire
        while True :
            self.set = set()
            self.dep = []
            self.matrice = []
            self.p_loin = (0,0)
    
            self.creation_map_random()
            max_tuple = self.verification_arriver()

            if max_tuple[0]>=int(max(self.nb_ligne,self.nb_colone)*5/8):
                break
    

    def creation_map_random(self):
        """cree un map totalement random"""
        self.trajectoire = self.point_depart(self.nb_ligne,self.nb_colone)
        self.matrice = self.cree_p_dep(self.trajectoire,self.nb_ligne,self.nb_colone)
        self.voiture = Voiture(self.trajectoire)
        self.affichage = Affichage("media\maps-texte\map_random.txt")
        for i in range(max(self.nb_ligne,self.nb_colone)+int(max(self.nb_ligne,self.nb_colone)/2)):
            acc = 0
            while acc==0:
                if self.trajectoire == []:
                    self.trajectoire = self.point_depart(self.nb_ligne,self.nb_colone)
                    self.matrice = self.cree_p_dep(self.trajectoire,self.nb_ligne,self.nb_colone)
                try :
                    info_direction = self.direction_chemin_random(self.nb_ligne,self.nb_colone,self.trajectoire)
                    acc+=1
                except :
                    self.trajectoire.pop()
            self.trajectoire = self.ajout_longueur(self.trajectoire,info_direction,self.nb_ligne,self.nb_colone)
            self.matrice = self.ajout_chemin(self.trajectoire,self.matrice,self.nb_ligne,self.nb_colone)
        self.ecrire_fichier("media\maps-texte\map_random.txt",self.matrice)
        self.trajectoire = self.gen_lst_matrice()
        self.trajectoire = self.ajout_epaisseur(self.trajectoire,self.nb_ligne,self.nb_colone)
        self.matrice = self.ajout_chemin(self.trajectoire,self.matrice,self.nb_ligne,self.nb_colone)
        self.chemin = self.gen_lst_matrice()
        self.p_loin = self.point_eloigner()
        self.matrice = self.zone_arriver(self.matrice,self.nb_ligne,self.nb_colone)
        self.ecrire_fichier("media\maps-texte\map_random.txt",self.matrice)


    def verification_arriver(self):
        """verifie la zone d'arriver pour qu'elle soit avec le plus grand chemin depuis le point de depart"""
        solveur = Solveur("media\maps-texte\map_random.txt","profondeur","normal","aff_fin","regle_stricte")
        stockage = []
        for elm in self.dep:
            try :
                self.chemin.remove(elm)
            except:
                pass

        for elem in self.chemin:
            files = self.files()
            i,j=elem
            self.matrice[j][i]="*"
            self.ecrire_fichier("media\maps-texte\map_random.txt",self.matrice)
            bool,trajectoire = solveur.niveaux2(files,"normal",False)
            stockage.append((len(trajectoire),elem))
            self.matrice[j][i]="."
            self.matrice = self.ajout_chemin(self.trajectoire,self.matrice,self.nb_ligne,self.nb_colone)
        #calcule le max parmis le 1er elment de chaque tuple de la lst
        max_tuple = max(stockage, key=lambda x: x[0])
        self.p_loin = max_tuple[1]
        self.matrice = self.zone_arriver(self.matrice,self.nb_ligne,self.nb_colone)
        self.ecrire_fichier("media\maps-texte\map_random.txt",self.matrice)
        return max_tuple
     

    def files(self):
        """cree un files"""
        trajectoire = []
        for i in range(len(self.matrice[0])):
            for j in range(len(self.matrice)):
                if self.matrice[j][i] == ">"  :
                    trajectoire.append((i,j))
                
        files = collections.deque([(trajectoire[0],[trajectoire[0]])])   
        return files    


    def point_eloigner(self):
        """calcule le point le plus loin du point de depart"""
        lst = self.gen_lst_matrice()
        a,b = self.dep[-1]

        max_d = 0
        for i in range(len(lst)):
                tuple = lst[i]
                distance = sqrt((tuple[0] - a)**2 + (tuple[1] - b)**2)
                if distance > max_d:
                    max_d = distance
                    max_tuple = tuple
        return max_tuple

       
    def zone_arriver(self,matrice,x,y):
        """place la zone d'ariver dans la matrice"""
        i,j = self.p_loin
        matrice[j][i] = "*"
        if 1< i-1 < x-1:
            matrice[j][i-1] = "*"
        if 1< i+1 < x-1:
            matrice[j][i+1] = "*"
        if 1< j-1 < y-1:
            matrice[j-1][i] = "*"
        if 1< j+1 < y-1:
            matrice[j+1][i] = "*"
        if 1< j-1 < y-1 and 1< i-1 < x-1:
            matrice[j-1][i-1] = "*"
        if 1< j+1 < y-1 and 1< i-1 < x-1:
            matrice[j+1][i-1] = "*"
        if 1< j-1 < y-1 and 1< i+1 < x-1:
            matrice[j-1][i+1] = "*"
        if 1< j+1 < y-1 and 1< i+1 < x-1:
            matrice[j+1][i+1] = "*"
        return matrice


    def gen_lst_matrice(self):
        """genere un lst de couple en fonction de la map"""
        lst = []
        for j in range(len(self.matrice)-1): 
            for i in range(len(self.matrice[j])-1):
                if self.matrice[j][i]  in [">","*","."]:
                    lst.append((i,j))
        return lst


    def ajout_epaisseur(self,lst,x,y):
        """ajoute de l'epaisseur au chemin de la lst"""
        lst_tmp = []
        for elm in lst:
            i,j=elm
            if 1< i-1 < x-2:
                lst_tmp.append((i-1,j))
            if 1< i+1 < x-2:
                lst_tmp.append((i+1,j))
            if 1< j-1 < y-2:
                lst_tmp.append((i,j-1))
            if 1< j-1 < y-2:
                lst_tmp.append((i,j+1))
        for elm in lst_tmp:
            lst.append(elm)
        return lst


    def ajout_chemin(self,trajectoire,matrice,x,y):
        """ajoute le chemin a la matrice"""
        for elm in trajectoire:
                i,j = elm
                matrice[j][i]="."
        matrice = self.modif_p_dep(matrice,x,y)

        return matrice


    def modif_p_dep(self,matrice,x,y):
        """permet d'afficher le poirnt de depart dans la matrice"""
        i,j = self.dep[-1]
        matrice[j][i] = ">"
        if 1< i-1 < x-1:
            matrice[j][i-1] = ">"
        if 1< i+1 < x-1:
            matrice[j][i+1] = ">"
        if 1< j-1 < y-1:
            matrice[j-1][i] = ">"
        if 1< j+1 < y-1:
            matrice[j+1][i] = ">"
        if 1< j-1 < y-1 and 1< i-1 < x-1:
            matrice[j-1][i-1] = ">"
        if 1< j+1 < y-1 and 1< i-1 < x-1:
            matrice[j+1][i-1] = ">"
        if 1< j-1 < y-1 and 1< i+1 < x-1:
            matrice[j-1][i+1] = ">"
        if 1< j+1 < y-1 and 1< i+1 < x-1:
            matrice[j+1][i+1] = ">"
        return matrice


    def direction_chemin_random(self,x,y,trajectoire):
        """cree une longeur et une direction aleatoire"""
        direction = choice(["H","B","D","G"])
        if direction == "B" :
            longeur = int((randint(trajectoire[-1][1],y-2)*random())/2)
        if direction == "D" :
            longeur = int((randint(trajectoire[-1][0],x-2)*random())/2)
        if direction == "G" :
            longeur = -int((randint(trajectoire[-1][0],x-2)*random())/2)
        if direction == "H" :
            longeur = -int((randint(trajectoire[-1][1],y-2)*random())/2)
        tmp_x = trajectoire[-1][0]+longeur
        tmp_y= trajectoire[-1][1]+longeur

        if direction == "B" and tmp_y > y-2:
            self.direction_chemin_random(x,y,trajectoire)
        elif direction == "H" and tmp_y < 1 :
            self.direction_chemin_random(x,y,trajectoire)
        elif direction == "D" and tmp_x > x-2 :
            self.direction_chemin_random(x,y,trajectoire)
        elif direction == "G" and tmp_x < 1:
            self.direction_chemin_random(x,y,trajectoire)

        if tmp_x < 1 or tmp_y< 1 or tmp_x > x-2 or tmp_y> y-2 :
            self.direction_chemin_random(x,y,trajectoire)
        
        if -1<=longeur<=1 :
            self.direction_chemin_random(x,y,trajectoire)
        return (direction,longeur)


    def ajout_longueur(self,trajectoire,info_direction,x,y):
        """ajoute les direction dans la lst du chemin"""
        direction,longeur = info_direction
        i,j= trajectoire[-1]
        tmp_x = trajectoire[-1][0]+longeur
        tmp_y= trajectoire[-1][1]+longeur

        if tmp_x < 1 or tmp_y< 1 or tmp_x > x-2 or tmp_y> y-2:
             try:
                 self.direction_chemin_random(x,y,trajectoire)
             except :
                 trajectoire.pop()

        if direction == "H" or direction == "B" :
            for v in range(1,abs(longeur)+1):
                if 1<j+v*self.voiture.sign(longeur) < y-2 and (i,j+v*self.voiture.sign(longeur)) not in self.set:
                    trajectoire.append((i,j+v*self.voiture.sign(longeur)))
                    self.set.add((i,j+v*self.voiture.sign(longeur)))
        if direction == "G" or direction == "D" :
            for v in range(1,abs(longeur)+1):
                if 1<i+v*self.voiture.sign(longeur)<x-2 and (i+v*self.voiture.sign(longeur),j) not in self.set:
                    trajectoire.append((i+v*self.voiture.sign(longeur),j))
                    self.set.add(((i+v*self.voiture.sign(longeur),j)))
        return trajectoire


    def point_depart(self,x,y):
        """point de depart aléatoire"""
        coin_h = choice(["H","B"])
        coin_d = choice(["D","G","M"])
        
        if coin_h == "H" and coin_d == "G":
            i = randint(int(x*9/10),x-2)
            j = randint(1,int(y/10))
        elif coin_h == "B" and coin_d == "D":
            i = randint(int(x*9/10),x-2)
            j = randint(int(y*9/10),y-2)
        elif coin_h == "H" and coin_d == "D":
            i = randint(int(x*9/10),x-2)
            j = randint(1,int(y/10))
        elif coin_h == "B" and coin_d == "G":
            i = randint(1,int(x/10))
            j = randint(int(x*9/10),y-2)
        elif coin_h == "B" and coin_d == "M":
            i = randint(int(x/2),int(x/2)+3)
            j = randint(int(x*9/10),y-2)
        elif coin_h == "H" and coin_d == "M":
            i = randint(int(x/2),int(x/2)+3)
            j = randint(1,int(y/10))
        
        return [(i,j)]


    def cree_p_dep(self,trajectoire,x,y):
        """cree les point de depart dans la lst de lst"""

        lst = []   
        for j in range(y):
            tmp_lst = []
            for i in range(x):
                if i==trajectoire[0][0] and j==trajectoire[0][1] :
                    tmp_lst.append(">")
                    self.dep.append((trajectoire[0][0],trajectoire[0][1]))               
                else : 
                    tmp_lst.append("#")
            lst.append(tmp_lst)
        
        return lst


    def ecrire_fichier(self,url,matrice) : 
        """
        ecrie dans une liste un fichier texte 
        param: url d'un fichier pour le lire 
            matrice : lst de lst
        --> return NONE
        """
        fichier = open(url, "w")
        fichier.truncate()
        fichier.close()
        fichier = open(url, "a")
        for j in range(len(matrice)):
            for i in range(len(matrice[j])+1):
                if i == len(matrice[j]):
                   fichier.write("\n")
                else :
                    fichier.write(matrice[j][i])
        fichier.close()


