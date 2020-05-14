from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

class ContinuousTestEnv:
    """ Environnement de test de la classification de Task 5. """
    
    def test(self,arbre,test_data, verbose = True):
        """ Takes an ID3 generated tree and compares it's predictions to testing data

            :param arbre: an ID3 generated classification tree
            :param test_data: testing data formalised as in serie 10
        """
        correct_guesses = 0
        for case in test_data:
            if arbre.classifie(case[1])[-1] == case[0]:
                correct_guesses = correct_guesses + 1

        accuracy = correct_guesses/len(test_data)

        if verbose:
            print("Ran " + str(len(test_data)) + " tests, accuracy of ID3 on continuous data is : " + str(accuracy*100.0) + "%")
        
        return accuracy