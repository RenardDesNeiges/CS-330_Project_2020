from .proposition_avec_variables import est_atomique, est_une_variable, tete, corps

class Filtre:
    """ Classe implémentant les méthodes de filtrage de propositions avec\
        variables.
    """

    echec = 'échec'

    def substitue(self, pattern, env):
        """ Effectue des substitutions de variables par leurs valeurs dans un\
            pattern.

            :param pattern: une proposition dont les variables doivent être\
            remplacées par des valeurs.\
            Une proposition est soit un atome, soit une liste contenant des\
            atomes et / ou d'autre listes.
            :param dict env: un environnment, c'est-à-dire un dictionnaire de\
            substitutions ``{variable : valeur}``.
            :return: le pattern dont les variables ont été remplacées par leurs\
            valeurs dans l'environnment. 
        """
        if est_atomique(pattern):
            if pattern in env:
                return env[pattern]
            else:
                return pattern

        pattern_subst = ()

        for sous_pattern in pattern:
            sous_pattern_subst = self.substitue(sous_pattern, env)
            pattern_subst = pattern_subst + (sous_pattern_subst,)

        return pattern_subst

    def filtre(self, datum, pattern):
        """ Effectue le filtrage entre un datum et un pattern.

            :param datum: une proposition sans variables.
            :param pattern: une proposition pouvant contenir des variables.
            :return: un environnment c'est-à-dire un dictionnaire de\
            substitutions ``{variable : valeur}``, ou ``'échec'`` si le filtrage\
            échoue.
        """
        if len(pattern) == 0 and len(datum) == 0:
            return {}

        if len(pattern) == 0 or len(datum) == 0:
            return Filtre.echec

        if est_atomique(pattern):
            if datum == pattern:
                return {}
            if est_une_variable(pattern):
                return {pattern: datum}

            return Filtre.echec

        if est_atomique(datum):
            return Filtre.echec

        datum_tete = tete(datum)
        pattern_tete = tete(pattern)
        datum_reste = corps(datum)
        pattern_reste = corps(pattern)

        tete_env = self.filtre(datum_tete, pattern_tete)

        if tete_env == Filtre.echec:
            return Filtre.echec

        pattern_reste = self.substitue(pattern_reste, tete_env)
        reste_env = self.filtre(datum_reste, pattern_reste)
        
        if reste_env == Filtre.echec:
            return Filtre.echec

        tete_env.update(reste_env)

        return tete_env

    def pattern_match(self, datum, pattern, env=None):
        """ Effectue le filtrage en tenant compte d'un environnement initial.

            :param datum: une proposition sans variables.
            :param pattern: une proposition pouvant contenir des variables.
            :param dict env: l'environnement initial à prendre en compte.
            :return: un nouvel environnment ou ``'échec'``.
        """
        if env is not None:
            env = env.copy()
        else:
            env = {}

        pattern = self.substitue(pattern, env)
        resultat = self.filtre(datum, pattern)
        if resultat == Filtre.echec:
            return Filtre.echec

        env.update(resultat)
        return env