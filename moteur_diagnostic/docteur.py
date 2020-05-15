from moteur_avec_variables.chainage_avant_avec_variables import ChainageAvantAvecVariables
from copy import deepcopy
from moteur_diagnostic.first_year_md import FirstYearMedSchool


class Docteur(FirstYearMedSchool):
    
    def __init__(self,attribs_et_valeurs):
        """:param regles: Générateur de règles contenant les règles générées par l'arbre
        :param attribs_et_valeurs:liste des attributs et des valeurs possibles"""
        FirstYearMedSchool.__init__(self)
        
        
        self.attribs_et_valeurs = attribs_et_valeurs
        
        #On ne peut pas changer le sexe et l'age donc on les enlève
        del self.attribs_et_valeurs['age']
        del self.attribs_et_valeurs['sex']
        #print(self.attribs_et_valeurs)
        
        self.titre = "médecin diplomé"
    
    def traitement(self,patient,k):
        """Prescrit un traitement à un patient. 
        :param patient: Exemple issue des données
        :param k: nombre d'objets maximal à changer dans le diagnositque
        :return: """
        traitement = ('1')
        
        if k not in range(1,len(self.attribs_et_valeurs)+1):
            raise ValueError('Le nombre de symptômes n est pas valide. Ce nombre doit être compris entre 1 et {}'.format(len(attribs_et_valeurs)))
        
        #Initialisation de la queue avec tous les chagements possibles de taille 1 et le changement de taille 0
        queue = [{}]+[{attrib:valeur} for attrib in self.attribs_et_valeurs for valeur in self.attribs_et_valeurs[attrib] if valeur != patient[1][attrib]]
        
        nb_changement = 1
        while len(queue) > 0:
            changement = queue.pop(0)
            new_patient = deepcopy(patient)
            new_patient[1].update(changement)
            (new_diagnostic,new_regle) = self.diagnostique(new_patient[1])
            
            #target = 0 => patient sain
            if new_diagnostic == '0':
               traitement = (new_diagnostic, new_regle, changement,patient)
               return traitement
            
            #Rajout des "enfants" de changement à la queue tant que ces enfants sont de tailles inférieurs ou égales à k
            if len(changement) < k and len(changement) > 0:
                for attrib2 in self.attribs_et_valeurs:
                    if attrib2 in changement:
                        continue
                    
                    for valeur2 in self.attribs_et_valeurs[attrib2]:
                        if valeur2 == patient[1][attrib2]:
                            continue
                        new_changement = changement.copy()
                        new_changement.update({attrib2:valeur2})
                        if new_changement not in queue:
                            queue.append(new_changement)
            
            nb_changement += 1
        
        return traitement
    
    def affiche_traitement(self,traitement):
        """Affiche un traitement 
        :param traitement: un traitement établit au format de la méthode précédente"""
        
        if traitement[0] == '1':
            print("Nous n'avons pas pu trouver de traitement...")
        
        elif traitement[0] == '0':
        
            if len(traitement[2]) == 0:
                print("Pas de traitement à afficher.")
            
            else:
                print('Et voici le traitement que je recommande:')
                changement = traitement[2]
                for attribut in changement:
                    if changement[attribut] == traitement[3][1][attribut]:
                        print('Big oof')
                        continue
                    print(attribut + ": " + traitement[3][1][attribut] + " ---> " + traitement[2][attribut])
                print('Ce traitement est basé sur la règle suivante:')
                print(traitement[1])
        
        else:
            raise ValueError("Quel étrange traitement !? Je ne sais pas quoi en faire...")
    
    def traitements_hopital(self,patients,k):
        """Etablit des traitements pour une liste de patients
        :param patients: Une liste de patients,
        :param k: Le nombre de changement maximal dans un traitement
        :return: Un dictionnaire avec keys = patient, value = traitement du patient"""
        no_patient = 1
        res = {}
        
        for patient in patients:
            res.update({no_patient:self.traitement(patient,k)})
            no_patient += 1
            
        return res
    
        
    
    def affiche_diagnostics_et_traitements_hopital(self,diagnostics,traitements):
        """Affiche les diagnostiques et les traitements pour des patients
        :param diagnostics: un dictionnaire de diagnostics au format de la méthode .diagnostique_hopital
        :param traitements: un dictionnaire de traitements au format de la méthode . traitements_hopitalS"""
        
        print("Bonjour, je suis {} et serai votre médecin aujourd'hui".format(self.titre))
        
        no_patient = 1
        
        for patient in diagnostics:
            
            print("Pour le.la patiente no {}, voici mon diagnostic et le traitement approprié:".format(no_patient))
            self.affiche_diagnostic(diagnostics[patient])
            self.affiche_traitement(traitements[patient])
            print("\n")
            
            no_patient += 1
   