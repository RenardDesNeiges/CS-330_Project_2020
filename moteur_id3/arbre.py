from moteur_id3.noeud_de_decision import NoeudDeDecision

class Arbre:
    """Un arbre résultant de la recher par ID3
    Cette classe est pas forcément nécessaire, mais elle me paraissait utile pour 
    essayer de chopper des infos efficacement sur un arbre"""
 
    def __init__(self,racine = None):
        #:param racine: Racine de l'arbre donné comme résultat de ID3.construit_arbre
        if racine is None:
            raise ValueError('Arbre invalide. Pas de racine')
    
        self.racine = racine
        self.noeuds = []
        self.noeuds_terminaux_profondeur = []        
        self.explore_dfs(racine,0)
    
    def explore_dfs(self,noeud,profondeur_actuelle):
        """explore les noeuds de l'arbre en dfs et les ajoute à la liste des noeuds  
        :param noeud: racine de l'arbre qu'on explore. Comme la méthode est récursive
        le param est souvent la racine d'un sous arbre.
        :param profondeur_actuelle: la profondeur à partir de laquelle l'exploration est effectuée"""
        
        self.noeuds.append(noeud)
        
        if noeud.terminal():
            self.noeuds_terminaux_profondeur.append((noeud,profondeur_actuelle))    
        else:
            for key in noeud.enfants:
                self.explore_dfs(noeud.enfants[key],profondeur_actuelle+1)  
   
    def profondeur(self):
        
        if self.racine.terminal():
            return 1
            
        return max([Arbre(self.racine.enfants[key]).profondeur() for key in self.racine.enfants])+1
    
    def hauteur_noeud(self,noeud):
        
        if noeud not in self.noeuds:
            raise ValueError('Le noeud passé en paramètre n appartient pas à l arbre donné')
        
        return Arbre(noeud).profondeur()
    
    def longueur_branche(self,feuille):
        
        for noeud,profondeur in self.noeuds_terminaux_profondeur:
            if feuille == noeud:
                return profondeur
   
        raise ValueError('Le noeud passé en paramètre n est pas une feuille de l arbre')
    
    def repartition_atttributs_noeuds(self):
        attributs_occurences = {'age':0,'sex':0,'cp':0,'trestbps':0,'chol':0,'fbs':0,'restecg':0,'thalach':0,'exang':0,'oldpeak':0,'slope':0,'ca':0,'thal':0}
        
        for noeud in self.noeuds:
            if noeud.attribut is None:
                continue
            attributs_occurences[noeud.attribut] += 1
        
        return attributs_occurences