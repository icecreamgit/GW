import numpy as np

class LMS:
    def __init__(self, n, tetta, outlier):
        self.n = n
        self.tetta = tetta
        self.outlier = outlier

    def calculateYwithoutError(self, t, x1, x2, size):
        y_ = np.zeros((size,))
        for i in range(size):
            y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]
        return y_

    def ylinealModel(self, n, tetta, outlier):
        # Search y without observation error
        x1 = (np.random.uniform(0., 1., n))
        x2 = (np.random.uniform(0., 1., n))

        y = LMS.calculateYwithoutError(self, tetta, x1, x2, n)
        xall = []

        # Search observation error
        e = np.random.binomial(n=1., p=(1 - outlier), size=n)

        # Search y_res:
        varMainObservations = 0.01
        varEmissions = 5.
        y_res = np.zeros((n,))

        for i in range(n):
            if e[i] == 1:
                y_res[i] = y[i] + np.random.normal(0, np.sqrt(varMainObservations))
            else:
                y_res[i] = y[i] + np.random.normal(0, np.sqrt(varEmissions))
        for i in range(n):
            xall.append(x1[i])
        for i in range(n):
            xall.append(x2[i])
        return y_res, xall

    def lineToColum(self, x, n, tetta):
        # Преобразование входной строки x в матрицу
        nTetta = len(tetta) - 1
        xnew = np.zeros((nTetta, n))
        counterDel = 0
        for stepi in range(nTetta):
            for stepj in range(n):
                xnew[stepi][stepj] = x[counterDel]
                counterDel += 1
        return xnew

    def LSMatrix(self, x, y):
        return np.dot((np.dot(np.linalg.inv(np.dot(x.transpose(), x)), x.transpose())), y)
