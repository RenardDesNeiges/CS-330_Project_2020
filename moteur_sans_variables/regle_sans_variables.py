
class RegleSansVariables:
    """ Représentation d'une règle d'inférence pour le chaînage sans\
        variables. 
    """

    def __init__(self, conditions, conclusion):
        """ Construit une règle étant donné une liste de conditions et une\
            conclusion.
            
            :param list conditions: une collection de propositions (sans\
            variables) nécessaires pour déclencher la règle.
            :param conclusion: la proposition (sans variables) résultant du\
            déclenchement de la règle.
        """

        self.conditions = set(conditions)
        self.conclusion = conclusion

    def depend_de(self, fait):
        """ Vérifie si un fait est pertinent pour déclencher la règle.
            
            :param fait: un fait qui doit faire partie des conditions de\
            déclenchement.
            :return: ``True`` si le fait passé en paramètre fait partie des\
            conditions de déclenchement.
        """
        return fait in self.conditions

    def satisfaite_par(self, faits):
        """ Vérifie si un ensemble de faits est suffisant pour prouver la\
            conclusion.
            
            :param list faits: une liste de faits.
            :return: ``True`` si les faits passés en paramètres suffisent à\
            déclencher la règle.
        """
        return self.conditions.issubset(faits)

    def __repr__(self):
        """ Représentation d'une règle sous forme de string. """
        return '{} => {}'.format(str(list(self.conditions)), 
                                 str(self.conclusion))