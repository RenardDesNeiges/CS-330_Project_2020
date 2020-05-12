from .chainage import Chainage

class ChainageAvantSansVariables(Chainage):
    """ Un moteur d'inférence à chaînage avant sans variables. """

    def chaine(self):
        """ Effectue le chaînage avant sur les faits et les règles contenus\
            dans la base de connaissances.
        """
        queue = self.connaissances.faits[:]
        self.reinitialise()

        while len(queue) > 0:
            fait = queue.pop(0)

            if fait not in self.solutions:
                self.solutions.append(fait)
                self.trace.append(fait)

                # Vérifie si des règles sont déclenchées par le nouveau fait.
                for regle in self.connaissances.regles:
                    if regle.depend_de(fait) and regle.satisfaite_par(self.solutions):
                        queue.append(regle.conclusion)
                        self.trace.append(regle)

        return self.solutions