import sys
import pickle


from moteur_id3.noeud_de_decision import NoeudDeDecision
from moteur_id3.id3 import ID3

from moteur_id3.arbre import Arbre

from moteur_id3.noeud_de_decision_continu import NoeudDeDecision_continu
from moteur_id3.id3_continu import ID3_continu

from bin_test import BinTestEnv
from continuous_test import ContinuousTestEnv
from random_forest import RandomForest
from moteur_diagnostic.first_year_md import FirstYearMedSchool

from moteur_diagnostic.docteur import Docteur

rick = []

with open('trees.pkl', 'rb') as input:
    rick = pickle.load(input)

print((rick))
