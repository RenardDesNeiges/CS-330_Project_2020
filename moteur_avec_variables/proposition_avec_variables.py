""" Fonctions utilitaires pour gérer des propositions sans ou avec variables\
    dans un moteur d'inférence.
"""

def est_atomique(proposition):
    """ Vérifie si la proposition courante est un atome (c'est le cas s'il\
        s'agit d'un string).

        :param proposition: une proposition.
        :return: ``True`` si la proposition est de type string.
    """
    return type(proposition) == type('')

def est_une_variable(proposition, marqueur='?'):
    """ Vérifie si la proposition courante est une variable (c'est le cas s'il\
        s'agit d'un atome dont la description commence par le marqueur de\ 
        variables).

        :param proposition: une proposition.
        :param marqueur: marqueur de variable avec valeur par défaut : ``'?'``.
        :return: ``True`` si l'argument est un atome et commence par le marqueur\
        de variables.
    """
    return est_atomique(proposition) and proposition[0] == marqueur

def tete(proposition):
    """ Coupe la proposition courante et retourne son premier élément.

        A noter que dans le cas d'une proposition atomique, la méthode soulève\
        une exception.

        :param proposition: une proposition.
        :return: la tête de la proposition composée.
    """

    if est_atomique(proposition):
        raise Exception("Proposition atomique: Impossible de la segmenter.")
    elif len(proposition) > 0:
        return proposition[0]
    else:
        raise Exception("Proposition vide: Impossible de la segmenter.")

def corps(proposition):
    """ Coupe la proposition courante et retourne la portion située après le\
        premier élément.

        A noter que dans le cas d'une proposition atomique, la méthode soulève\ 
        une exception.
        
        :param proposition: une proposition.
        :return: le corps de la proposition composée.
    """
        
    if est_atomique(proposition):
        raise Exception("Proposition atomique: Impossible de la segmenter.")
    elif len(proposition) > 0:
        return proposition[1:]
    else:
        raise Exception("Proposition vide: Impossible de la segmenter.")

def lister_variables(proposition):
    """ Retourne un ensemble (de type ``set``) contenant les variables\ 
        mentionnées dans la proposition courante.

        :param proposition: une proposition.
        :return: la liste des variables apparaissant dans la proposition.
    """

    variables = set()
    if est_atomique(proposition):
        if est_une_variable(proposition):
            variables.add(proposition)
    else:
        for sous_prop in proposition:
            variables.update(lister_variables(sous_prop))
    return variables