from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        # Nous devons extraire les domaines de valeur des 
        # attributs, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
            
        arbre = self.construit_arbre_recur(donnees, attributs)
        
        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        if not donnees:
            #Pas de donnees
            return None
        elif len(list(set([item[0] for item in donnees]))) == 1: # c'est un peu de la branlette comme syntaxe mais si toutes les donnees sont dans la même classe ça rends true
            #Noeud terminal
            return NoeudDeDecision(None, donnees)
        else:
            #Noeud intermediaire
            entropie = [(a,self.h_C_A(donnees,a,attributs[a])) for a in attributs] # a nouveau c peut-être pas très clair, mais ca fait une liste de tuples "(attribut,entropie)" après je m'en sers pour trouver le min de l'entropie
            at_clef = list(filter(lambda t: t[1] == min(entropie)[1], entropie))[0][0] # extrait la catégorie qui a l'entropie la plus faible de la liste des entropies
            partition = self.partitionne(donnees, at_clef, attributs[at_clef])
            attributs_sans_at_clef = {key:val for key, val in attributs.items() if key != at_clef} 
            enfants = {}

            for key in partition : 
                if partition[key] != []:
                    enfants[key] = self.construit_arbre_recur(partition[key], attributs_sans_at_clef)
            return NoeudDeDecision(at_clef, donnees, enfants)

    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        partition = dict()
        for v in valeurs:
            dt = list(filter(lambda item : item[1][attribut] == v,donnees))
            partition[v] = dt
        return partition


    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """

        acc = 0
        for d in donnees:
            if d[1][attribut] == valeur: acc = acc + 1

        return acc/len(donnees)

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """

        acc_a = 0
        acc_c = 0
        for d in donnees:
            if d[1][attribut] == valeur:
                acc_a = acc_a + 1
                if d[0] == classe:
                    acc_c = acc_c + 1
        if acc_a != 0:
            return acc_c/acc_a
        else:
            return 0

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        
        classes = list(set([item[0] for item in donnees]))
        acc = 0
        for c in classes:
            p_c = self.p_ci_aj(donnees,attribut,valeur,c)
            if p_c != 0 :
                acc = acc - (p_c + log(p_c,2))
            else :
                acc = 0

        return acc

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """

        acc = 0
        for v in valeurs :
            acc = acc + self.p_aj(donnees,attribut,v) * self.h_C_aj(donnees,attribut,v)

        return acc