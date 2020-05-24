import csv
import sys

import pickle

from random import shuffle
from copy import deepcopy

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
        print("Data Shuffling demonstration: \n")

        print("Parsing pre-binned training data...")
        train_bin_csv = self.parseCSV("train_bin.csv")
        train_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_bin_csv]

        print("Parsing pre-binned testing data...")
        test_public_bin_csv = self.parseCSV("test_public_bin.csv")
        test_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_public_bin_csv]

        print("Shuffling the data...")

        complete_dataset = train_bin + test_public_bin
        shuffle(complete_dataset)

        train_bin = deepcopy(complete_dataset)
        del train_bin[143:]

        test_public_bin = deepcopy(complete_dataset)
        del test_public_bin[:143]
        print("Task 1")
        task1_report = open('rapport/Task1_data_shuffled.txt','w')
        
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
        
        task2_report = open("rapport/Task2_data_shuffled.txt",'w')

        print("Setting up testing environnement...")
        binTest = BinTestEnv()
        accuracy_id3_train = binTest.tree_test(self.arbre.racine,train_bin,False)
        accuracy_id3 = binTest.tree_test(self.arbre.racine,test_public_bin,False)
        
        task2_report.write("The accuracy of the the tree generated in Task 1 on the train data is : {}%\n".format(accuracy_id3_train*100)) 
        task2_report.write("The accuracy of the the tree generated in Task 1 on the test data is : {}%".format(accuracy_id3*100))
        task2_report.close()
        
        print("Done with Task 2")

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
