import sys
from os.path import join, dirname, abspath

# Les classes définies dans ce module s'appuient sur des classes définies dans 
# inference_sans_variables.
# Nous devons donc ajouter le chemin vers ce dossier au système pour pouvoir 
# importer son contenu.
# Il s'agit d'un truc rendu nécessaire par la structure particulière des 
# dossiers de cette série d'exercices, mais qui doit être employé avec 
# précaution.
sys.path.insert(0, join(dirname(dirname(dirname(abspath(__file__)))),
                        'inference_sans_variables'))

