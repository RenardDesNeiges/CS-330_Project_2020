from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables
from .rule_generator import RuleGen

class Diagnostique:
    
    def __init__(self,rgen,donnees):
        #:param regles: La liste des règles générées par RuleGen.depth_first_search
        self.rgen = rgen
        self.donnees = donnees
        
        """Construction d'un dictionnaire avec 
        key = attribut passible de chagements dans le diagnositque et 
        value = liste des valeurs possibles"""
        attribs_et_valeurs = {}
        for donnee in self.donnnees:
                for attrib in donnee[1]:
                    #On évite l'age et le sexe
                    if attrib == 'sexe' or attrib == 'age':
                        continue
                    
                    if attrib not in attribs_et_valeurs:
                        attribs_et_valeurs[attrib] = [donnee[1][attrib]]
                    else:
                        attribs_et_valeurs[attrib].append(donnee[1][attrib])
        
        self.attribs_et_valeurs = attribs_et_valeurs
    
    def diagnositque_patient(self,patient,k):
        """Diagnostique un patient.
        :param patient: Exemple issue des données
        :param k: nombre d'objets maximal à changer dans le diagnositque
        :return: un dictionnaire de changements à apporter aux patients pour qu'il soit sain, keys = attributes to change and values = value you should """
        
        #Cas patient non malade. On suppose que target = 0 => patient sain
        if patient[0] == 0:
            return {}
        
        if k not in range(1,12):
            raise ValueError('Le nombre de symptômes n est pas valide. Ce nombre doit être compris entre 1 et 11')
        
        #Initialisation de la queue avec tous les chagements possibles de taille 1
        queue = [{attrib:valeur} for attrib in patient[1] for valeur in attribs_et_valeurs[attrib] if valeur != patient[1][attrib]] 
        
        while len(queue) > 0:
            changement = queue.pop(0)
            new_patient = patient.deepcopy()
            new_patient[1].update(changement)
            target = self.rgen.classifie(newpatient)
            
            #target = 0 => patient sain
            if target == 0:
               return changement
            
            #Rajout des "enfants" de changement à la queue tant que ces enfants sont de tailles inférieurs ou égales à k
            if len(changement) < k:
                for attrib2 in attribs_et_valeurs:
                    if attrib2 in changement:
                        continue
                    
                    for valeur2 in attribs_et_valeurs[attrib2]:
                        new_changement = changement.copy()
                        new_changement.update({attrib2:valeur2})
                        queue.append(new_changement)
        
        return {}