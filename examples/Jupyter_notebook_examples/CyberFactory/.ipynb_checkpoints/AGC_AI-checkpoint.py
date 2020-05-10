import pickle
import numpy as np
import math
import pandas as pd

class AGCAI():
    def __init__(self):
        # load it ML alg
        with open('ML_Alg.pkl', 'rb') as fid:
            self.model = pickle.load(fid)

    def run(self, Thickness, Goal_Thickness):
        data = {'Thickness': [], 'Goal_Thickness': []}
        data['Thickness'].append(Thickness)
        data['Goal_Thickness'].append(Goal_Thickness)

        X = pd.DataFrame(data)

        # Change to numpy array
        X_test = np.array(X)

        # Ceshape for a single sample with many features.
        # X_test = X_test.reshape(1, -1)

        # Test prediction
        Roll_gap = self.model.predict(X_test)

        return Roll_gap

agc_ai = AGCAI()