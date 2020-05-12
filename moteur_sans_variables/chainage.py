
class Chainage:
    """ Le squelette d'un moteur d'inférence.

        Cette classe n'est pas censée être instanciée directement. Elle doit\ 
        être sous-classée par des classes filles qui implémentent la méthode\ 
        ``chaine``.

        :cvar self.trace: représente l'ordre dans lequel les propositions ont\
        été déduites et dans lequel les règles ont été appliquées (à utiliser\
        pour débugger votre code).
        :cvar self.solutions: doit contenir les solutions du chaînage.
    """

    __indentation = 4 * ' '

    def __init__(self, connaissances):
        """ Initialise le moteur d'inférence sans variables.
        
            :param connaissances: la base de connaissances.
        """

        self.trace = []
        self.solutions = []
        self.connaissances = connaissances

    def reinitialise(self):
        """ Réinitialise le moteur. 

            La trace et les solutions sont à nouveau vides après l'appel à\
            cette méthode.
        """

        self.trace = []
        self.solutions = []

    def chaine(self):
        """ Effectue le chaînage. 

            Si des solutions sont trouvées, elles sont placées dans\
            ``self.solutions`` et également retournées.

            :return: les solutions.
        """

        # Nous retournons un ensemble vide dans ce cas.
        return self.solutions

    def affiche_trace(self, indent=None):
        """ Affiche la trace d'un chaînage après l'appel à ``chaine``.

            :param str indent: l'identation souhaitée au début de chaque ligne\
            (quatre espaces par défaut).
        """

        if indent is None:
            indent = Chainage.__indentation

        print('Trace:')
        for evenement in self.trace:
            print('{}{}'.format(indent, evenement))

    def affiche_solutions(self, indent=None):
        """ Affiche les solutions d'un chaînage après l'appel à ``chaine``.

            :param str indent: l'identation souhaitée au début de chaque ligne\
            (quatre espaces par défaut).
        """

        if indent is None:
            indent = Chainage.__indentation

        if len(self.solutions) > 0:
            print('Faits déduits:')
            for fait in self.solutions:
                print('{}{}'.format(indent, fait))
        else:
            print('Aucun fait trouvé.')