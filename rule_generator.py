from copy import deepcopy

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables
from moteur_sans_variables.connaissance import BaseConnaissances
from moteur_avec_variables.filtre import Filtre
from moteur_avec_variables.unificateur import Unificateur
from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables

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
        return self.rules

    def copy(self,rule):
        out = []
        for fact in rule:
            out.append(fact.copy())
        return out

    def depth_first_search(self, node,rule):
        """ Parcourt l'arbre pour générer les règles """
        #print(rule)
        #print(self.rules)
        
        if node.terminal():
            rule_copy = deepcopy(rule)
            rule_copy[1] = ('target', '?x', node.classe())
            self.rules.append(rule_copy)
        else:
            for key in node.enfants:
                rule_copy = deepcopy(rule)
                #del rule_copy[-1]
                rule_copy[0].append((str(node.attribut),
                                            '?x',
                                            str(key),))
                self.depth_first_search(node.enfants[key], rule_copy)
    
    def display_rules(self):
        print("Rules deduced :")
        for rule in self.rules:
            print("    If : ",end= "")
            for fact in rule[0]:
                print(fact,end=" & ")
            print("\n    Then => " + str(rule[1]))

    def classifie(self, case):
        """ Classifie un cas en fonction des règles données au départ """
        #print("Classifying : ")
        facts = self.convert_case_to_facts(case, 'x')

        bc = BaseConnaissances(
            lambda descr: RegleAvecVariables(descr[0], descr[1]))


        bc.ajoute_faits(facts)
        bc.ajoute_regles(self.rules)

        
        moteur = ChainageAvantAvecVariables(connaissances=bc, methode=Unificateur())
        moteur.chaine()

        moteur.affiche_trace()

    def convert_case_to_facts(self, case,name):
        """ Convertit un cas en faits utilisables par le moteur d'inférence """
        facts = []
        for attribute in case:
            fact = (str(attribute), name, str(case[attribute]))
            facts.append(fact)
        return facts
