import math

import numpy as np

class LMS:
    def calculateYwithoutError(self, t, x1, x2, size):
        y_ = np.zeros((size,))
        for i in range(size):
            y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]
        return y_

    def ylinealModel(self, n, tetta, outlier):
        # Search y without observation error
        x1 = np.random.uniform(0., 1., n)
        x2 = np.random.uniform(0., 1., n)

        y = self.calculateYwithoutError(tetta, x1, x2, n)
        xall = [[], []]

        # Search observation error
        e = np.random.binomial(n=1, p=(1.0 - outlier), size=n)

        # Search y_res:
        varMainObservations = 0.1
        varEmissions = 0.5
        y_res = []

        for i in range(n):
            if e[i] == 1:
                y_res.append(y[i] + np.random.normal(0, np.sqrt(varMainObservations)))
            else:
                y_res.append(y[i] + np.random.normal(0, np.sqrt(varEmissions)))
        for i in range(n):
            xall[0].append(x1[i])
            xall[1].append(x2[i])
        y_res = np.array(y_res).reshape(n, 1)

        return y_res, xall

    def LSMatrix(self, x, y):
        C0 = np.dot(x.transpose(), x)
        C1 = np.linalg.inv(C0)
        C2 = np.dot(C1, x.transpose())
        C3 = np.dot(C2, y)
        return C3
