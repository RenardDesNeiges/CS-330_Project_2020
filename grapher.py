import sys
import pickle
import matplotlib.pyplot as plt

rick = {}

with open('graph.pkl', 'rb') as input:
    rick = pickle.load(input)

plt.plot(list(rick.keys()),list(rick.values()))
plt.title("Valid trees ratio")
plt.xlabel('Subsamplings')
plt.ylabel('Ratio of valid trees generated')
plt.legend()
plt.show()
