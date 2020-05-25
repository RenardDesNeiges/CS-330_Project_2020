from moteur_id3.noeud_de_decision_continu import NoeudDeDecision_continu
from moteur_id3.id3_continu import ID3_continu

class ContinuousTestEnv:
    """ Environnement de test de la classification de Task 5. """
    
    def test(self,arbre,continuous_test_data, verbose = False):
        """ Takes an ID3 generated tree and compares it's predictions to testing data

            :param arbre: an ID3 generated classification tree
            :param test_data: testing data formalised as in serie 10
        """
        correct_guesses = 0


        for case in continuous_test_data:
            if arbre.classifie(case[1])[-1] == case[0]:
                correct_guesses = correct_guesses + 1

        c_accuracy = correct_guesses/len(continuous_test_data)

        if verbose:
            print("Ran " + str(len(continuous_test_data)) + " tests, accuracy of ID3 on continuous data is : " + str(c_accuracy*100.0) + "%")
        
        return c_accuracy