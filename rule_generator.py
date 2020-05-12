from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables

class RuleGen():
    """ Converti un graphe de la classe NoeudDeDecision en une liste de 
        règles compatible avec le moteur avec variables de la série 3, 
        et gère la déduction à partir de ces règles """
    def __init__(self):
        self.rules = []

    def convert(self, node):
        """ Converti un graphe de la classe NoeudDeDecision en une liste de
        règles compatible avec le moteur avec variables de la série 3 """

        print("Running depth first search on tree ... ")
        rule = [[],None]
        self.depth_first_search(node,rule)
        print("Rules generated")
        return self.depth_first_search

    def depth_first_search(self, node,rule):
        """ Parcourt l'arbre pour générer les règles """
        
        if node.terminal():
            rule_copy = rule.copy()
            rule_copy[1] = (node.classe(),'?x')
            self.rules.append(rule_copy)

        else:
            for key in node.enfants:
                rule_copy = rule.copy()
                rule_copy[0].append((str(node.attribut),
                                            '?x',
                                            key,))
                self.depth_first_search(node.enfants[key], rule_copy)

    def classifie(self, case):
        """ Classifie un cas en fonction des règles données au départ """
        #print("Classifying : ")
        facts = self.convert_case_to_facts(case, 'x')



    def convert_case_to_facts(self, case,name):
        """ Convertit un cas en faits utilisables par le moteur d'inférence """
        facts = []
        for attribute in case:
            fact = (str(attribute), name, str(case[attribute]))
            facts.append(fact)
        return facts
