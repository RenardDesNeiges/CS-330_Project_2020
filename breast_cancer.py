import csv
import sys
import matplotlib.pyplot as plt

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_id3.arbre import Arbre

from moteur_id3.noeud_de_decision_continu import NoeudDeDecision_continu
from moteur_id3.id3_continu import ID3_continu

from bin_test import BinTestEnv
from continuous_test import ContinuousTestEnv
from random_forest import RandomForest
from rule_generator import RuleGen

from moteur_diagnostic.diagnostique import Diagnostique

class ResultValues():

    def __init__(self):

        # Do computations here

        #parsing the data from the csv file
        print("Parsing pre-binned training data...")
        raw_csv = self.parseCSV("breast-cancer-wisconsin.csv")

        thresholds = []
        accuracies = []

        thresh = 300
        train_data = [[line['Class'],
                    {key: val for key, val in line.items() if key != "Class" and key != "id"}]
                    for line in raw_csv.copy()[:thresh]]

        test_data = [[line['Class'],
                    {key: val for key, val in line.items() if key != "Class" and key != "id"}]
                    for line in raw_csv.copy()[thresh:]]

        print("Generating ID3 tree from " +
            str(len(train_data)) + " samples...")
        id3 = ID3()
        self.arbre = Arbre(id3.construit_arbre(train_data))

            #print("Testing...")
        binTest = BinTestEnv()
        accuracy = binTest.tree_test(self.arbre.racine, test_data, True)

        
        
        # Task 5

        print("Parsing pre-binned training data for continuous algorith test (removing cases with unknown values)...")
        raw_cont_csv = list(filter(lambda x: not ('?' in x.values()), self.parseCSV("breast-cancer-wisconsin.csv")))

        train_cont_data = [[line['Class'],
                       {key: val for key, val in line.items() if key != "Class" and key != "id"}]
                        for line in raw_cont_csv.copy()[:300]]

        test_cont_data = [[line['Class'],
                      {key: val for key, val in line.items() if key != "Class" and key != "id"}]
                        for line in raw_cont_csv.copy()[300:]]

        print("Generating continuous ID3 tree from " +
              str(len(train_data)) + " samples...")
        id3_continuous = ID3_continu()
        self.arbre_advance = id3_continuous.construit_arbre(train_cont_data)

        continuousTest = ContinuousTestEnv()

        continuousTest.test(self.arbre_advance, test_cont_data, True)


        

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
