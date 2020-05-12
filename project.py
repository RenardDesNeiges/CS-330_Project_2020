import csv
import sys

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from bin_test import BinTestEnv
from random_forest import RandomForest
from rule_generator import RuleGen

class ResultValues():

    def __init__(self):
        
        # Do computations here
        
        #parsing the data from the csv file
        print("Parsing training data...")
        train_bin_csv = self.parseCSV("train_bin.csv")
        train_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_bin_csv] #Gem bcp les oneliners :)

        id3 = ID3()

        # Task 1
        print("Generating ID3 tree from " + str(len(train_bin)) + " samples...", end = "")
        self.arbre = id3.construit_arbre(train_bin)
        print(" Done!")
        
        #Task 2
        print("Parsing testing data...")
        test_public_bin_csv = self.parseCSV("test_public_bin.csv")
        test_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in test_public_bin_csv]

        print("Setting up testing environnement...")
        binTest = BinTestEnv()
        binTest.test(self.arbre,test_public_bin)

        # print("Testing training with a random forest :")
        # rForest = RandomForest()
        # rf_tree = rForest.generate(train_bin,test_public_bin,4,1000)
        # print()

        # Task 3
        self.faits_initiaux = None
        self.regles = None

        rGen = RuleGen()

        rGen.convert(self.arbre)

        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

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
