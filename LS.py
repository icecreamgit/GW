import numpy as np

class LS:
    def LSMatrix(self, x, y):
        C0 = np.dot(x.T, x)
        C1 = np.linalg.inv(C0)
        C2 = np.dot(C1, x.T)
        C3 = np.dot(C2, y)
        return C3
