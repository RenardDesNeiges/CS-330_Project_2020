from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables
from rule_generator import RuleGen
from copy import deepcopy


class Diagnostique:
    
    def __init__(self,rgen,attribs_et_valeurs):
        """:param regles: Générateur de règles contenant les règles générées par l'arbre
        :param attribs_et_valeurs:liste des attributs et des valeurs possibles"""
        self.rgen = rgen
        
        """Construction d'un dictionnaire avec 
        key = attribut passible de chagements dans le diagnositque et 
        value = liste des valeurs possibles"""
        self.attribs_et_valeurs = attribs_et_valeurs
        
        #On ne peut pas changer le sexe et l'age donc on les enlève
        del self.attribs_et_valeurs['age']
        del self.attribs_et_valeurs['sex']
        #print(self.attribs_et_valeurs)
    
    def diagnostique_patient(self,patient,k):
        """Diagnostique un patient.
        :param patient: Exemple issue des données
        :param k: nombre d'objets maximal à changer dans le diagnositque
        :return: si le patient est sein, {'target':0}, si aucun traitement n'a été trouvé {'target':1},
        si un traitement est trouvé {'target':1, attributs à changer pour le traitement: valeurs pour que le patient soit sain}.
        La trace est aussi retrounée"""
        
        #Cas patient non malade. On suppose que 'target' = 0 => patient sain
        if patient[0] == '0':
            return ('0',{},[])
        
        if k not in range(1,len(self.attribs_et_valeurs)+1):
            raise ValueError('Le nombre de symptômes n est pas valide. Ce nombre doit être compris entre 1 et {}'.format(len(attribs_et_valeurs)))
        
        #Initialisation de la queue avec tous les chagements possibles de taille 1
        queue = [{attrib:valeur} for attrib in self.attribs_et_valeurs for valeur in self.attribs_et_valeurs[attrib] if(valeur != patient[1][attrib])] 
        
        while len(queue) > 0:
            changement = queue.pop(0)
            #print(changement)
            new_patient = deepcopy(patient)
            new_patient[1].update(changement)
            (target,trace) = self.rgen.classifie(new_patient[1])
            
            #target = 0 => patient sain
            if target == '0':
               return (target,changement,trace)
            
            #Rajout des "enfants" de changement à la queue tant que ces enfants sont de tailles inférieurs ou égales à k
            if len(changement) < k:
                for attrib2 in self.attribs_et_valeurs:
                    if attrib2 in changement:
                        continue
                    
                    for valeur2 in self.attribs_et_valeurs[attrib2]:
                        new_changement = changement.copy()
                        new_changement.update({attrib2:valeur2})
                        queue.append(new_changement)
        
        return ('1',{},[])