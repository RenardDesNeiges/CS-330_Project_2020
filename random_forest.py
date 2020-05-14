import random

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from bin_test import BinTestEnv

from operator import itemgetter 

class RandomForest:
    """ Implémentation claquée par terre de random forests, claquée par terre mais meilleure 
    que juste run ID3 sur tout le set de données (ça résout un peu le problème d'oversampling) """
    
    def generate(self,train_data,test_data,subsampling,subsamples):
        """ Takes an ID3 generated tree and compares it's predictions to testing data

            :param arbre: an ID3 generated classification tree
            :param test_data: testing data formalised as in serie 10
        """
        
        print("Generating " + str(subsamples) + " subsamples with " + str(subsampling) + " times subsampling")
        train_set = self.generate_training_set(train_data,int(len(train_data)/subsampling),subsamples)
        
        print("Generating trees ...")
        id3 = ID3()
        tree_set = []
        binTest = BinTestEnv()
        for item in train_set:
            tree_set.append(id3.construit_arbre(item))
        

        print("Evaluating trees ...")
        self.tree_acc_set = [];
        for tree in tree_set: 
            try: #certains arbres générés sont incapables de traiter certaines données (le subset de données d'entrainement ne contenant pas forcément tous les cas de figures pour chaques attribut) c'est méga deg mais je fait juste un try catch pour ignorer ces cas làs...
                accuracy = binTest.tree_test(tree, test_data, False)
            except:
                pass
            else:
                self.tree_acc_set.append( (accuracy, tree) )
        
        inv_rate = len(self.tree_acc_set)/len(tree_set)
        inv_numb = len(tree_set) - len(self.tree_acc_set)

        bestTree = max(self.tree_acc_set, key = itemgetter(0))
        print("Accuracy = " + str(bestTree[0]*100) + "%")
        print(str(inv_numb) + " invalid trees, invalid rate is : " + str(inv_rate*100) + "%")
        return bestTree[1]

    def generate_training_set(self,train_data,train_size,subsamples):

        train_set = []

        if train_size > len(train_data):
            print("ERROR: training data smaller than subsampling size")
            return None
        
        for j in range(subsamples):
            subsample = train_data.copy()
            for i in range(len(train_data)-train_size):
                item = random.choice(subsample)
                subsample.remove(item)
            train_set.append(subsample)
        
        return train_set

    def forest_classify(self,case, verbose = False):
        #class_list = []
        acc = 0
        total_acc = 0
        
        for tree in self.tree_acc_set:
            acc += int(tree[1].classifie(case)[-1])*tree[0]
            total_acc += tree[0]

        #map(lambda x: int(x),class_list)

        
        avg_c = acc/total_acc
        classification = 0
        if(avg_c>0.5): classification = 1
        else: classification = 0
        if(verbose): print("average_classification : " + str(avg_c) + " , value chosen : " + str(classification))
        return classification
