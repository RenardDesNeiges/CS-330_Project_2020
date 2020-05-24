from copy import deepcopy

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables
from moteur_sans_variables.connaissance import BaseConnaissances
from moteur_avec_variables.filtre import Filtre
from moteur_avec_variables.unificateur import Unificateur
from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables

class FirstYearMedSchool():
    """ Converti un graphe de la classe NoeudDeDecision en une liste de 
        règles compatible avec le moteur avec variables de la série 3, 
        et gère la déduction à partir de ces règles """
    def __init__(self):
        self.rules = []
        self.titre = "en première année de médecine"

    def apprend(self, node):
        """ Converti un graphe de la classe NoeudDeDecision en une liste de
        règles compatible avec le moteur avec variables de la série 3 """

        print("Running depth first search on tree ... ")
        cond = []
        self.depth_first_search(node,cond)
        print("Rules generated")
        return self.rules

    def convert_case_to_facts(self, case,name):
        """ Convertit un cas en faits utilisables par le moteur d'inférence """
        facts = []
        for attribute in case:
            fact = (str(attribute), name, str(case[attribute]))
            facts.append(fact)
        return facts

    def depth_first_search(self, node,cond):
        """ Parcourt en DFS l'arbre pour générer les règles """
        
        if node.terminal():
            cond_copy = deepcopy(cond)
            conclusion = ('target', '?x', node.classe())
            self.rules.append(RegleAvecVariables(cond_copy,conclusion))
        else:
            for key in node.enfants:
                cond_copy = deepcopy(cond)

                #del rule_copy[-1]
                cond_copy.append((str(node.attribut),
                                            '?x',
                                            str(key),))
                self.depth_first_search(node.enfants[key], cond_copy)

    def diagnostique(self, case, verbose = False):
        """ Classifie un cas en fonction des règles données au départ """
        #print("Classifying : ")
        facts = self.convert_case_to_facts(case, 'subject')

        bc = BaseConnaissances(
            lambda regle: regle)


        bc.ajoute_faits(facts)
        bc.ajoute_regles(self.rules)

        moteur = ChainageAvantAvecVariables(connaissances=bc, methode=Filtre())
        faits = moteur.chaine()

        if(verbose): moteur.affiche_trace()
        
        res = list(filter(lambda x: x[0] == 'target', faits))
        
        if len(res) == 0:
            return ('2',moteur.trace[0])

        return (res[0][2],moteur.trace[0])
    
    def repr_diagnostic(self,diagnostic):
        """Affiche un diagnostics établit par la méthode précédente"""
        res = ""
        annonce = ""
        
        if diagnostic[0] == '2':
            return "Le diagnostic n'a pas abouti..."
        
        else:
            if diagnostic[0] == '1':
                annonce = 'Je diagnostique une maladie cardiaque chez ce.tte patient.e.'
            elif diagnostic[0] == '0':
                annonce = "Je ne diagnostique aucune maladie cardiaque chez ce.tte patient.e"
            else:
                raise ValueError("Le diagnostic n'a pas abouti...")
        
            res += (annonce + "\n")
        
            res += "Ce diagnostic est basé sur les faits suivants:\n"
        
            faits_diagnostic = ""
            for cond in diagnostic[1].conditions:
                faits_diagnostic += cond[0] + " = " + cond[2] + ", "
            faits_diagnostic = faits_diagnostic[:len(faits_diagnostic)-2]
        
            res += (faits_diagnostic + "\n")
            
            return res
    
    def diagnostique_hopital(self,patients):
        """"Crée un diagnostique pour chaque patient
        :param patients: une liste de patients
        :return: un dictionnaire key = patient, value = diagnostic associé"""
        no_patient = 1
        res = {}
        
        for patient in patients:
            res.update({no_patient:self.diagnostique(patient[1])})
            no_patient += 1
       
        return res
    
    def repr_diagnostics_hopital(self,diagnostics):
        """Affiche la liste de diagnostic retrounée par la méthode précédents
        :param: Un dictionnaire de diagnostics établi par diagnostique_hopital"""
        res = ""
        for no_patient in diagnostics:
            res += "Pour le.la patiente no {}, voici mon diagnostic:".format(no_patient)
            res += self.repr_diagnostic(diagnostics[no_patient])
            res += "\n"
        
        return res