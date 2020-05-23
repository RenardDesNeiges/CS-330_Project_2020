import random

from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3
from bin_test import BinTestEnv

from operator import itemgetter 

from math import log

class RandomForest:
    """ Implémentation claquée par terre de random forests, claquée par terre mais meilleure 
    que juste run ID3 sur tout le set de données (ça résout un peu le problème d'oversampling) """
    
    def __init__(self):
        self.trees = []
        self.valid_trees_accuracy = []
        self.best_tree = NoeudDeDecision(None,None,None)
        self.betas = {}
        self.adaboost = lambda x: '1'
    
    def generate_trees(self,train_data,subsampling,subsamples):
        """ Takes an ID3 generated tree and compares it's predictions to testing data

            :param arbre: an ID3 generated classification tree
            :param test_data: testing data formalised as in serie 10
        """
        self.trees.clear()
        
        print("Generating " + str(subsamples) + " subsamples with " + str(subsampling) + " times subsampling")
        train_sets = self.generate_training_set(train_data,int(len(train_data)/subsampling),subsamples)
        
        print("Generating trees ...")
        id3 = ID3()
        self.trees = []
        binTest = BinTestEnv()
        for item in train_sets:
            self.trees.append(id3.construit_arbre(item))

        return self.trees
    
    def select_valid_trees(self,train_data):
        print("Evaluating trees ...")
        self.valid_trees_accuracy.clear()
        binTest = BinTestEnv()
        for tree in self.trees: 
            try: #certains arbres générés sont incapables de traiter certaines données (le subset de données d'entrainement ne contenant pas forcément tous les cas de figures pour chaques attribut) c'est méga deg mais je fait juste un try catch pour ignorer ces cas làs...
                accuracy = binTest.tree_test(tree, train_data, False)
            except:
                pass
            else:
                self.valid_trees_accuracy.append((accuracy, tree))

        return self.valid_trees_accuracy
    
    def valid_trees_ratio(self):
        return len(self.valid_trees_accuracy)/len(self.trees)
   
    #Used in Adaboosting
    def binari(self,x):
        if x >= 0:
            return 1
        else:
            return 0
            

    def construct_best_tree(self):
        self.best_tree = max(self.valid_trees_accuracy, key = itemgetter(0))[1]
    
    def construct_classifier_adaboost(self,train_data):    
        total_nb_cases = len(train_data)
       
        if total_nb_cases == 0:
            raise ValueError('No train data given')
        
        attributes = list(train_data[0][1].keys())
        #Calcul de la probabilité qu'on attribut donné ai une valeur donnée
        probabilities_attributes = {}
        for attribute in attributes:
            if attribute == 'sex':
                probabilities_attributes.update({attribute: lambda x:1/2})
            else:
                probabilities_attributes.update({attribute: lambda x:len([case for case in train_data if x == case[1][attribute]])/total_nb_cases})
            
        #Calcul des probabilités des exemples
        probabiilities_cases = {}
        total_prob = 0
        for i in range(len(train_data)):
            probability = 1
            for attribute in attributes:
                probability *= probabilities_attributes[attribute](train_data[i][1][attribute])
                
            probabiilities_cases.update({i:probability})
            total_prob += probability
 
        #Normalisation des probabilité des exemples
        for case in probabiilities_cases:
            probabiilities_cases[case] /= total_prob
            
        #on en garde que les arbres avec moins de 50% de probabilité d'erreur
        bricks_trees = [arbre[1] for arbre in self.valid_trees_accuracy if sum([probabiilities_cases[i]*abs(int(arbre[1].classifie(train_data[i][1])[-1])-int(train_data[i][0])) for i in range(len(train_data))])<0.5]
        
        #Initialisation de l'algorithm Adaboosting
        wis = probabiilities_cases
        total_wis = 1
            
        #Adaboosting
        for tree in bricks_trees:
            for case in probabiilities_cases:
                probabiilities_cases[case] = wis[case]/total_wis
                
            epsilon  = sum([probabiilities_cases[case]*abs(int(tree.classifie(train_data[case][1])[-1])-int(train_data[case][0])) for case in probabiilities_cases])
            self.betas[tree] = epsilon/(1-epsilon)
            total_wis = 0
                 
            for case in wis:
                wis[case] = wis[case]*pow(self.betas[tree],1-abs(int(tree.classifie(train_data[case][1])[-1])-int(train_data[case][0])))
                total_wis += wis[case]
        
        #Construction du classifier
        self.adaboost = lambda x:str(self.binari(sum([-log(self.betas[tree])*(int(tree.classifie(x)[-1])-1/2) for tree in self.betas])))
    def generate_training_set(self,train_data,train_size,subsamples):

        train_sets = []

        if train_size > len(train_data):
            print("ERROR: training data smaller than subsampling size")
            return None
        
        for j in range(subsamples):
            subsample = train_data.copy()
            for i in range(len(train_data)-train_size):
                item = random.choice(subsample)
                subsample.remove(item)
            train_sets.append(subsample)
        
        return train_sets
    
    
    def forest_classify(self,case,method, verbose = False):
        methods_available = ['MajorityVote','BestTree','AdaBoost']
        
        if method not in methods_available:
            raise ValueError('Les méthodes possibles sont : MajorityVote, BestTree et AdaBoost. Veuillez entrer une de ces trois méthodes')
        
        if method == 'MajorityVote':
            acc = 0
            total_acc = 0
        
            for tree in self.valid_trees_accuracy:
                acc += int(tree[1].classifie(case)[-1])*tree[0]
                total_acc += tree[0]
        
            avg_c = acc/total_acc
            classification = 0
            if(avg_c>0.5): classification = 1
            else: classification = 0
            if(verbose): print("average_classification : " + str(avg_c) + " , value chosen : " + str(classification))
            return str(classification)
        
        if method == 'BestTree':
            return self.best_tree.classifie(case)[-1]
        
        if method == 'AdaBoost':
            return self.adaboost(case)