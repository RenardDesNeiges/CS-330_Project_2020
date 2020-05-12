from .proposition_avec_variables import est_atomique, est_une_variable, tete, corps

class Unificateur:
    """ Classe implémentant les méthodes de l'unification de propositions avec\
        variables. """

    echec = 'échec'

    def substitue(self, pattern, env):
        """ Effectue des substitutions de variables dans un pattern.
            
            :param pattern: une proposition dont les variables doivent être\
            remplacées par d'autres propositions.
            :param dict env: un environnment, c'est-à-dire un dictionnaire de\
            substitutions ``{variable : proposition}``.
            :return: le pattern dont les variables ont été remplacées les\
            propositions qui leur sont associées dans l'environnement.
        """
        if est_atomique(pattern):
            if pattern in env:
                return self.substitue(env[pattern], env)
            else:
                return pattern

        pattern_subst = ()

        for sous_pattern in pattern:
            sous_pattern_subst = self.substitue(sous_pattern, env)
            pattern_subst = pattern_subst + (sous_pattern_subst, )

        return pattern_subst

    def unifie(self, prop1, prop2):
        """ Effectue l'unification entre deux propositions.

            :param prop1: une proposition pouvant contenir des variables.
            :param prop2: une proposition pouvant contenir des variables.
            :return: un environnment, c'est-à-dire un dictionnaire de\
            substitutions ``{variable : proposition}``, ou ``'échec'`` si\
            l'unification a échoué.
        """
        if len(prop1) == 0 and len(prop2) == 0:
            return {}
        if len(prop1) == 0 or len(prop2) == 0:
            return Unificateur.echec

        # Une des deux propositions est un atome => on essaie de le matcher.
        if est_atomique(prop1) or est_atomique(prop2):
            if prop1 == prop2:
                return {}

            if not est_atomique(prop1):
                prop1, prop2 = prop2, prop1

            if est_une_variable(prop1):
                if prop1 in prop2:
                    return Unificateur.echec
                else:
                    return {prop1: prop2}

            if est_une_variable(prop2):
                return {prop2: prop1}

            # Dans les autres cas, l'unification est un échec.
            return Unificateur.echec

        # Aucune des propositions n'est atomique : on unifie récursivement.
        prop1_tete = tete(prop1)
        prop2_tete = tete(prop2)
        prop1_reste = corps(prop1)
        prop2_reste = corps(prop2)
        tete_env = self.unifie(prop1_tete, prop2_tete)
        if tete_env == Unificateur.echec:
            return Unificateur.echec

        prop1_reste = self.substitue(prop1_reste, tete_env)
        prop2_reste = self.substitue(prop2_reste, tete_env)
        reste_env = self.unifie(prop1_reste, prop2_reste)
        if reste_env == Unificateur.echec:
            return Unificateur.echec

        tete_env.update(reste_env)
        return tete_env

    def pattern_match(self, prop1, prop2, env=None):
        """ Effectue l'unification en tenant compte d'un environnement initial.

            :param prop1: une proposition pouvant contenir des variables.
            :param prop2: une proposition pouvant contenir des variables.
            :param dict env: l'environnement initial à prendre en compte.
            :return: un nouvel environnment ou ``'échec'``.
        """
        if env is not None:
            prop1 = self.substitue(prop1, env)
            prop2 = self.substitue(prop2, env)
            env = env.copy()
        else:
            env = {}

        resultat = self.unifie(prop1, prop2)
        if resultat == Unificateur.echec:
            return Unificateur.echec

        env.update(resultat)
        return env