import csv
import sys

import pickle

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables
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

def iTurnedMyselfIntoAPickleMorty(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

class ResultValues():

    def __init__(self):
        
        # Do computations here
        
        #parsing the data from the csv file
        print("Parsing pre-binned training data...")
        train_bin_csv = self.parseCSV("train_bin.csv")
        train_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_bin_csv] #Gem bcp les oneliners :)
        print(" Done!\n")
        
        print("Task 1")
        task1_report = open('rapport/Task1_data.txt','w')
        
        task1_report.write("Generating ID3 tree from " + str(len(train_bin)) + " samples...\n")
        id3 = ID3()
        self.arbre = Arbre(id3.construit_arbre(train_bin))
        nb_noeuds = len(self.arbre.noeuds)
        nb_feuilles = len(self.arbre.noeuds_terminaux_profondeur)
        profondeur = self.arbre.profondeur()        
        moyenne_longueur_branche = sum([self.arbre.longueur_branche(feuille_longueur[0]) for feuille_longueur in self.arbre.noeuds_terminaux_profondeur])/len(self.arbre.noeuds_terminaux_profondeur)
        moyenne_enfants_noeud = sum([len(noeud.enfants) for noeud in self.arbre.noeuds if noeud.enfants != None])/len([noeud for noeud in self.arbre.noeuds if not noeud.terminal()])
        

        task1_report.write("L'arbre a un {} noeuds dont {} feuilles\n".format(nb_noeuds,nb_feuilles))
        task1_report.write("L'arbre a une profondeur de " + str(profondeur) + "\n")
        task1_report.write("La moyenne du nombre d'enfants par noeud est " +str(moyenne_enfants_noeud) + "\n")
        task1_report.write("La moyenne de la longueur d'une branche est " +str(moyenne_longueur_branche) + "\n")
        task1_report.write(NoeudDeDecision.__repr__(self.arbre.racine))
        
        task1_report.close()
        print('Done with task 1')
        
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 2")
        
        print("Parsing pre-binned testing data...")
        test_public_bin_csv = self.parseCSV("test_public_bin.csv")
        test_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_public_bin_csv]
        print("Done!\n")
        
        task2_report = open("rapport/Task2_data.txt",'w')

        print("Setting up testing environnement...")
        binTest = BinTestEnv()
        accuracy_id3_train = binTest.tree_test(self.arbre.racine,train_bin,False)
        accuracy_id3 = binTest.tree_test(self.arbre.racine,test_public_bin,False)
        
        task2_report.write("The accuracy of the the tree generated in Task 1 on the train data is : {}%\n".format(accuracy_id3_train*100)) 
        task2_report.write("The accuracy of the the tree generated in Task 1 on the test data is : {}%".format(accuracy_id3*100))
        task2_report.close()
        
        print("Done with Task 2")
        
        """
        print("---------------------------------------------------------------------------------------------------------")

        print("Task 2 bis")
        """
        #Adaboost tree test
        test_adaboost_tree = BinTestEnv()
        accuracy_total = 0
        rF_adaboost_tree = RandomForest()
        for i in range(100):
            rF_adaboost_tree.generate_trees(train_bin,4,1000)
            rF_adaboost_tree.select_valid_trees(train_bin)
            rF_adaboost_tree.construct_classifier_adaboost(train_bin)
            accuracy_total += test_adaboost_tree.test_forest(rF_adaboost_tree,'AdaBoost',test_public_bin)
        
        iTurnedMyselfIntoAPickleMorty(accuracy_total/100,"AdaBoost_test_accuracy.pkl")

        #Majority tree test
        test_majority_tree = BinTestEnv()
        accuracy_total = 0
        rF_majority_tree = RandomForest()
        for i in range(100):
            rF_majority_tree.generate_trees(train_bin,4,1000)
            rF_majority_tree.select_valid_trees(train_bin)
            accuracy_total += test_majority_tree.test_forest(rF_majority_tree,'MajorityVote',test_public_bin)
        
        iTurnedMyselfIntoAPickleMorty(accuracy_total/100,"Majority_test_accuracy.pkl")
        
        #Best tree test
        test_best_tree = BinTestEnv()
        accuracy_total = 0
        rF_best_tree = RandomForest()
        for i in range(100):
            rF_best_tree.generate_trees(train_bin,4,1000)
            rF_best_tree.select_valid_trees(train_bin)
            rF_best_tree.construct_best_tree()
            accuracy_total += test_best_tree.test_forest(rF_best_tree,'BestTree',test_public_bin)
        
        iTurnedMyselfIntoAPickleMorty(accuracy_total/100,"BestTree_test_accuracy.pkl")

        #Valid trees ratio test
        rForest = RandomForest()
        subsamplings = range(1,141)
        invalid_trees_ratios =  {}
        for x in subsamplings:
            test_invalid_ratio = []
            for i in range(100):
                rForest.generate_trees(train_bin,x,1000)
                rForest.select_valid_trees(train_bin)
                test_invalid_ratio.append(rForest.valid_trees_ratio())
            
            invalid_trees_ratios.update({x:sum(test_invalid_ratio)/100})
        
        iTurnedMyselfIntoAPickleMorty(invalid_trees_ratios,"x=subsamplings_y=invalid_trees_ratios.pkl")
        
        print("Done with Task 2 bis")
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 3")
        
        task3_report = open("rapport/Task3_data.txt",'w')
        
        Titou = FirstYearMedSchool()
        self.regles = Titou.apprend(self.arbre.racine)
        
        task3_report.write('Liste des regles developees :\n')
        for regle in self.regles:
            task3_report.write(RegleAvecVariables.__repr__(regle))
            task3_report.write("\n")
        
        self.faits_initiaux = []
        for i in range(len(train_bin)):
            self.faits_initiaux.append(Titou.convert_case_to_facts(train_bin[i][1],'patient no ' + str(i+1)))
        
        task3_report.write('Liste des faits initiaux :\n')
        for i in range(len(train_bin)):
            task3_report.write('Patient ' + str(i+1) + ':')
            task3_report.write(str(self.faits_initiaux[i]))
            task3_report.write('\n')
       
        diagnostics = Titou.diagnostique_hopital(test_public_bin)
        repr_diagnostics = Titou.repr_diagnostics_hopital(diagnostics)
        task3_report.write('Liste des diagnostics:\n')
        task3_report.write(repr_diagnostics)
        task3_report.write("\n")
        
        inference_vs_tree = [i for i in range(len(test_public_bin)) if Titou.diagnostique(test_public_bin[i][1])[0] != self.arbre.racine.classifie(test_public_bin[i][1])[-1]]
        if len(inference_vs_tree) > 0:
            case = ''
            for i in inference_vs_tree:
                case += str(i+1) + ','
            if len(case) > 0:
                case = case[:len(case)-1]
            task3_report.write("Les guess sont dlfférents pour le moteur d'inférence et pour l'arbre de décision pour les cas: " + case)
        task3_report.close()
        
        print("---------------------------------------------------------------------------------------------------------")
        print("Task 4")
        task4_report = open("rapport/Task4_data.txt",'w')
        
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
        task4_report.write('Liste des diagnotisques:\n')
        task4_report.write(Chris.repr_diagnostics_et_traitements_hopital(diagnostics,traitements))
        task4_report.write('\n')
        task4_report.write('Taux de personnes pour lesquelles ont a réussi à administrer un traitement : {}'.format(Chris.ratio_succes(traitements)))
        print("---------------------------------------------------------------------------------------------------------")
        """
        print("Task 5")
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
