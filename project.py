import csv

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

class ResultValues():

    def __init__(self):
        
        # Do computations here
        
        #parsing the data from the csv file
        train_public_bin_csv = self.parseCSV("test_public_bin.csv")
        train_public_bin = [ [line["target"], {key:val for key, val in line.items() if key != "target"}] for line in train_public_bin_csv] #I enjoy oneliners a bit too much :)

        id3 = ID3()

        # Task 1
        self.arbre = id3.construit_arbre(train_public_bin)

        print('Arbre de décision :')
        print(str(self.arbre)+"\n")

        # Task 3
        self.faits_initiaux = None
        self.regles = None
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
        with open(address, newline='') as csvfile:
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