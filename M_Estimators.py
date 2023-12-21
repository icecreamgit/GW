import numpy as np
from functools import reduce

class M_Estimators:
    def __LineFunction(self, tetta, X, n):
        fi = []
        for i in range(n):
            fi.append(tetta[0] + tetta[1] * X[i][1] + tetta[2] * X[i][2])
        fi = np.array(fi)
        return fi

    def __Ei(self, fi, Y, n):
        ei = []
        for i in range(n):
            ei.append(abs(fi[i] - Y[i]))
        ei = np.array(ei)
        return ei
    def __Ui(self, ei, l, n):
        for i in range(n):
            ei[i] /= l
        return ei

    def __WiCauchy(self, ui, n):
        c = 2.3849
        vector = []
        wi = np.zeros((n, n))
        for i in range(n):
            vector.append(1. / (1 + pow(ui[i] / c, 2)))
        # Заполняю диагональ матрицы n x n элементами вектора wi
        for i in range(n):
            wi[i][i] = vector[i]
        return wi
    def __WiHuber(self, ui, n):
        k = 1.345
        vector = []
        wi = np.zeros((n, n))
        for i in range(n):
            if ui[i] <= k:
                vector.append(1)
            else:
                vector.append(k * np.sign(ui[i]) / ui[i])
        # Заполняю диагональ матрицы n x n элементами вектора wi
        for i in range(n):
            wi[i][i] = vector[i]
        return wi

    def __TettaCount(self, X, W, Y):
        return np.dot(np.linalg.inv(reduce(np.dot, [X.transpose(), W, X])),    reduce(np.dot, [X.transpose(), W, Y]))

    def __Verification(self, tettaOld, tettaNew, eps):
        result = True
        vector = []

        for i in range(len(tettaOld)):
            vector.append( abs( (tettaOld[i] - tettaNew[i]) / tettaOld[i] ) )
        if max(vector) > eps:
            result = False
        return result

    def MainEstimators(self, tetta, typeEst, X, Y, n):
        W = np.zeros((n, n))
        eps = 0.001
        fiStar = Y
        tettaOld = tetta

        while True:
            fi = self.__LineFunction(tettaOld, X, n)
            ei = self.__Ei(fi, Y, n)
            l = 1. / 0.67449 * (np.median(ei))
            ui = self.__Ui(ei, l, n)
            if typeEst == "Huber":
                W = self.__WiHuber(ui, n)
            elif typeEst == "Cauchy":
                W = self.__WiCauchy(ui, n)
            tettaNew = self.__TettaCount(X, W, Y.reshape(n, 1))

            if self.__Verification(tettaOld, tettaNew, eps) == False:
                break
            fiStar = fi
            tettaOld = tettaNew

        return tettaNew