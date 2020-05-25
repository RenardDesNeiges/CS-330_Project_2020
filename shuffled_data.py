import csv
import sys

import pickle

from random import shuffle
from copy import deepcopy

from moteur_avec_variables.regle_avec_variables import RegleAvecVariables
from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_id3.arbre import Arbre

from bin_test import BinTestEnv

from statistics import mean

import matplotlib.pyplot as plt

def pickle_dumper(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

class ResultValues():

    def __init__(self):

        # Do computations here

        accuracies_train = []
        accuracies_test = []

        #parsing the data from the csv file
        print("Data Shuffling demonstration:")

        print("        Parsing pre-binned training data...")
        train_bin_csv = self.parseCSV("train_bin.csv")
        train_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_bin_csv]

        print("        Parsing pre-binned testing data...")
        test_public_bin_csv = self.parseCSV("test_public_bin.csv")
        test_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_public_bin_csv]

        print("        Running the shuffling tests")


        complete_dataset = train_bin + test_public_bin

        for i in range(100):
            shuffle(complete_dataset)

            train_bin = deepcopy(complete_dataset)
            del train_bin[143:]

            test_public_bin = deepcopy(complete_dataset)
            del test_public_bin[:143]
            
            id3 = ID3()
            self.arbre = Arbre(id3.construit_arbre(train_bin))

            binTest = BinTestEnv()
            try:
                accuracy_id3_train = binTest.tree_test(self.arbre.racine,train_bin,False)
                accuracy_id3 = binTest.tree_test(self.arbre.racine,test_public_bin,False)

                accuracies_test.append(accuracy_id3)
                accuracies_train.append(accuracy_id3_train)
            except:
                pass

        
        shuffle_report = open("rapport/shuffle_test.txt",'w')
        
        shuffle_report.write("The average accuracy of the the tree generated in Task 1 on the train data is : {}%\n".format(mean(accuracies_train)*100)) 
        shuffle_report.write("The average accuracy of the the tree generated in Task 1 on the test data is : {}%".format(mean(accuracies_test)*100))
        shuffle_report.close()
        
        print("    Done!")

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
