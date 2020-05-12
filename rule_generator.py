from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables

class RuleGen():
    """ Converti un graphe de la classe NoeudDeDecision en une liste de règles compatible avec le moteur avec variables de la série 3 """
    
    def convert(self, tree):
        print("Running depth first search on tree : ")
        self.depth_first_search(tree)

    def depth_first_search(self, tree):
        if tree.terminal():
            print(tree.p_class)
        else:
            print(tree.attribut)
            for key in tree.enfants:
                print(key,end = " : ")
                self.depth_first_search(tree.enfants[key])