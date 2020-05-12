from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables

class RuleGen():
    """ Converti un graphe de la classe NoeudDeDecision en une liste de 
        règles compatible avec le moteur avec variables de la série 3 """
    def __init__(self):
        self.rules = []

    def convert(self, node):
        print("Running depth first search on tree : ")
        rule = [[],None]
        self.depth_first_search(node,rule)
        print(self.rules)

    def depth_first_search(self, node,rule):
        rule_copy = rule.copy()
        if node.terminal():
            rule_copy[1] = (node.classe(),'?x')
            self.rules.append(rule_copy)
            #print("Terminal node : " + str(node.classe()))
        else:
            rule_copy[0].append(
                (str(node.attribut), 
                '?x', 
                 str(node.donnees[node.attribut])))

            for key in node.enfants:
                self.depth_first_search(node.enfants[key], rule_copy)
