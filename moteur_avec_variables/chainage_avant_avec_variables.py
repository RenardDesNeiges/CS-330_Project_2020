from moteur_sans_variables.chainage import Chainage
from .filtre import Filtre
from .regle_avec_variables import RegleAvecVariables

class ChainageAvantAvecVariables(Chainage):
    """ Un moteur d'inférence à chaînage avant avec variables. """

    def __init__(self, connaissances, methode=None):
        """
            :param methode: ``Filtre`` ou ``Unificateur``, détermine le type de\
            pattern match à appliquer. ``Filtre`` par défaut.
        """

        Chainage.__init__(self, connaissances)

        if methode is None:
            self.methode = Filtre()
        else:
            self.methode = methode

    def instancie_conclusion(self, regle, envs):
        """ Instancie la conclusion d'une règle pour tous les environnements.

            :param regle: la règle dont la conclusion doit être instanciée.
            :param list envs: les environnements servant à instancier la\
            conclusion.
            :return: une liste de propositions correspondant aux différentes\
            instanciations de la conclusion.
        """
        return [self.methode.substitue(regle.conclusion, env) for env in envs]
    
    def chaine(self):
        """ Effectue le chaînage avant sur les faits et les règles contenus\
            dans la base de connaissances.
        """
        queue = self.connaissances.faits[:]
        self.reinitialise()

        while len(queue) > 0:
            fait = queue.pop(0)

            if fait not in self.solutions:
                self.trace.append(fait)
                self.solutions.append(fait)

                # Vérifie si des règles sont déclenchées par le nouveau fait.
                for regle in self.connaissances.regles:
                    cond_envs = regle.depend_de(fait, self.methode)
                    for cond, env in cond_envs.items():
                        # Remplace l'environnement par ceux qui satisfont
                        # toutes les conditions de la règle et pas seulement la 
                        # première condition.
                        envs = regle.satisfaite_par(self.solutions, cond, env, self.methode)

                        # Ajoute la conclusion de la règle instanciée pour tous 
                        # les environnements possibles.
                        if len(envs) > 0:
                            queue.extend(self.instancie_conclusion(regle, envs))
                            self.trace[0] = regle

        return self.solutions