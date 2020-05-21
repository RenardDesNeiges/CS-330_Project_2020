import csv
import sys

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_id3.arbre import Arbre

from moteur_id3.noeud_de_decision_continu import NoeudDeDecision_continu
from moteur_id3.id3_continu import ID3_continu

from bin_test import BinTestEnv
from continuous_test import ContinuousTestEnv
from random_forest import RandomForest
from moteur_diagnostic.first_year_md import FirstYearMedSchool 

from moteur_diagnostic.docteur import Docteur

import matplotlib.pyplot as plt

class ResultValues():

    def __init__(self):

        # Do computations here
        
        #parsing the data from the csv file
        print("Parsing pre-binned training data...")
        train_bin_csv = self.parseCSV("train_bin.csv")
        train_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_bin_csv] #Gem bcp les oneliners :)
        """
        print("Task 1")
        
        print("Generating ID3 tree from " + str(len(train_bin)) + " samples...", end = "")
        id3 = ID3()
        self.arbre = Arbre(id3.construit_arbre(train_bin))
        nb_noeuds = len(self.arbre.noeuds)
        nb_feuilles = len(self.arbre.noeuds_terminaux_profondeur)
        profondeur = self.arbre.profondeur()
        moyenne_longueur_branche = sum([self.arbre.longueur_branche(feuille_longueur[0]) for feuille_longueur in self.arbre.noeuds_terminaux_profondeur])/len(self.arbre.noeuds_terminaux_profondeur)
        moyenne_enfants_noeud = sum([len(noeud.enfants) for noeud in self.arbre.noeuds if noeud.enfants != None])/len([noeud for noeud in self.arbre.noeuds if not noeud.terminal()])
        print(" Done!")

        print("L'arbre a un {} noeuds dont {} feuilles".format(nb_noeuds,nb_feuilles))
        print("L'arbre a une profondeur de " + str(profondeur))
        print("La moyenne du nombre d'enfants par noeud est " +str(moyenne_enfants_noeud))
        print("La moyenne de la longueur d'une branche est " +str(moyenne_longueur_branche)) 
        
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 2")
        
        print("Parsing pre-binned testing data...")
        test_public_bin_csv = self.parseCSV("test_public_bin.csv")
        test_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_public_bin_csv]
        

        print("Setting up testing environnement...")
        binTest = BinTestEnv()

        binTest.tree_test(self.arbre.racine,test_public_bin)

        # print("Testing training with a random forest :")
        

        #binTest.test_forest(rForest,test_public_bin,True)
        # print()
        """
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 2 bis")
        
        rForest = RandomForest()
        subsamplings = list(range(1,81))
        invalid_trees_ratios =[]
        for x in subsamplings:
            test_invalid_ratio = []
            for i in range(100):
                rForest.generate_trees(train_bin,x,1000)
                rForest.select_valid_trees(train_bin)
                test_invalid_ratio.append(rForest.valid_trees_ratio())
            
            invalid_trees_ratios.append(sum(test_invalid_ratio)/100)
        
        plt.plot(subsamplings,invalid_trees_ratios)
        plt.title("Valid trees ratio")
        plt.xlabel('Subsamplings')
        plt.ylabel('Ratio of valid trees generated')
        #plt.legend()
        
        plt.savefig("Valid_trees_ratio.png")
        print("---------------------------------------------------------------------------------------------------------")
        """
        print("Task 3")
        
        self.faits_initiaux = None
        self.regles = None

        Titou = FirstYearMedSchool()
        self.regles = Titou.apprend(self.arbre.racine)
        
        diagnostics = Titou.diagnostique_hopital(test_public_bin)
        Titou.affiche_diagnostics_hopital(diagnostics)
        #binTest.rule_test(rGen, test_public_bin,True)
        
        
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 4")
        
        attributs_et_valeurs = {}
        first = True
        for donnee in train_bin:
            if first:
                for attribut in donnee[1]:
                    attributs_et_valeurs[attribut] = set(donnee[1][attribut])
                first = False
            else:
                for attribut in donnee[1]:
                    attributs_et_valeurs[attribut].update(set(donnee[1][attribut]))
            #print(attributs_et_valeurs)
        
        Chris = Docteur(attributs_et_valeurs)
        Chris.apprend(self.arbre.racine)
        
        diagnostics = Chris.diagnostique_hopital(test_public_bin)
        traitements = Chris.traitements_hopital(test_public_bin,2)
        
        Chris.affiche_diagnostics_et_traitements_hopital(diagnostics,traitements)
        
        nb_traité_nontraités = Chris.ratio_succes(traitements)
        print("On arrive à traiter {} patient.e.s sur 80".format(nb_traité_nontraités))
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 5")
        """
        """
        print("Parsing continuous training data...")    
        train_continuous_csv = self.parseCSV("train_continuous.csv")
        train_continuous = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_continuous_csv] #Gem bcp les oneliners :)
        test_continuous_csv = self.parseCSV("test_public_continuous.csv")
        test_continuous = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_continuous_csv]
        
        id3_continuous = ID3_continu()
        arbre_continuous = Arbre(id3_continuous.construit_arbre(train_continuous))
        self.arbre_advance = arbre_continuous.racine
        continuousTest = ContinuousTestEnv()

        continuousTest.test(self.arbre_advance,test_continuous,True)
        """


        

    def get_results(self):
        return [self.arbre.racine, self.faits_initiaux, self.regles, self.arbre_advance]

    def parseCSV(self,address):
        """ Takes a .csv file and returns a list of dictonaries where each element is has a key 
        given by the row #0 of the file

            :param address: address of the csv file
            :return: a list of dictionnaries
        """

        with open(address, newline='', encoding="utf-8-sig") as csvfile:

            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            first = True
            index = []
            data = []
            for row in reader:
                if first:
                    index = row[0].split(',')
                    first = False
                else:
                    dictRow= {}
                    for i in range(len(index)):
                        dictRow[index[i]] = row[0].split(',')[i]
                    data.append(dictRow)
            
            return data

result = ResultValues()
