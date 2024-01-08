import random
from functools import reduce

import numpy as np
import math


class Transform:
    # Меняем горизонтальный вид элементов матрицы на вертикальный
    def __init__(self, X, n):
        self.X = X
        self.n = n
    def MatrixInVector(self, xInterm, X=None, n=None):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        if isinstance(X, str):
            count = 0
            for line in xInterm:
                count += 1
                for i in range(self.n):
                    line.append(self.X[i][count])
        else:
            count = 0
            for line in xInterm:
                count += 1
                for i in range(n):
                    line.append(X[i][count])
        return xInterm
    def VectorInMatrix(self, X, xNew):
        n = len(X[0])
        for j in range(n):
            xNew.append([1., X[0][j], X[1][j]])
        return np.array(xNew)

def KeyFuncion(item):
    return item[0]

class MCD:
    def __init__(self, Y, n, p):
        self.n = n
        self.p = p
        self.Y = Y
    def __LineInVector(self, vector):
        newList = [[], []]
        counter = 0
        for line in newList:
            for j in range(self.n):
                line.append(vector[counter])
                counter += 1
        return newList
    def __ReturnY(self, di, h):
        newList = []
        for i in range(h):
            index = di[i][1]
            newList.append(self.Y[index])
        return newList

    def __CreateNewListCstep(self, data, di, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            index = di[i][1]
            newList[0].append(data[0][index])
            newList[1].append(data[1][index])
        return newList

#####################################################___NEW
    def __ReturnListX(self, X, Hnew, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            j = Hnew[i]
            newList[0].append(X[0][j])
            newList[1].append(X[1][j])
        return newList
    def __ReturnListY(self, Hnew, h):
        newList = []
        for i in range(h):
            index = Hnew[i]
            newList.append(self.Y[index])
        return newList
    def __H1Generate(self, h, n):
        H = []
        vector = [i for i in range(n)]
        for i in range(h):

            item = np.random.choice(vector)
            H.append(item)
            vector.remove(item)
        return H

    def __TS_Count(self, X, H, h):
        HValuesList = [[], []]
        T1mean, T2mean, T = 0.0, 0.0, []
        S = [[], []]

        # Создание Х1 и Х2, принадлежащие H вектору
        for i in range(h):
            trueIndex = H[i]
            HValuesList[0].append(X[0][trueIndex])
            HValuesList[1].append(X[1][trueIndex])

        T1mean = np.mean(HValuesList[0])
        T2mean = np.mean(HValuesList[1])
        S = np.cov(HValuesList)

        T = np.array([T1mean, T2mean])
        return T, S

    def __Di2(self, X, T, S, n):
        B, di = [], []

        for i in range(n):
            B.append([[X[0][i] - T[0]], [X[1][i] - T[1]]])

        B = np.array(B)
        for i in range(n):
            C0 = reduce(np.dot, [B[i].transpose(), np.linalg.inv(S), B[i]])[0][0]
            di.append([np.sqrt(C0), i])
        return di
    def __ChooseHValues(self, dold, h):
        Hnew = []
        for i in range(h):
            Hnew.append(dold[i][1])
        return Hnew
    def __CStepFor500(self, X, T1, S1, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T1)
        S.append(S1)
        for i in range(2):
            dold = self.__Di2(X, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(X, Hnew, h)
            T.append(Tnew)
            S.append(Snew)
            detS2 = np.linalg.det(S[i + 1])
            detS1 = np.linalg.det(S[i])
            if detS2 > detS1:
                print("ERROR, detS2 > detS1")

        # return S3
        return S[2], Hnew
    def __CStepFor10(self, X, T3, S3, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T3)
        S.append(S3)
        i = 0
        while 1:
            dold = self.__Di2(X, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(X, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS3 = np.linalg.det(S[i])
            detS4 = np.linalg.det(S[i + 1])
            i += 1
            if math.isclose(detS4, detS3) or math.isclose(detS4, 0.0):
                break
        index = len(T) - 1

        # return S3
        return S[index], Hnew

    def FindRelativeDistances(self, X, n, h):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        HiSaver10, HiSaver500, diEndVector, dnew, Snew = [], [], [], [], [[], []]
        cStepNumber, lowestNumber = 500, 10

        # Реализация первого пункта задания с созданием 500 di расстояний
        i = 0
        while i < cStepNumber:
            H1 = self.__H1Generate(h, n)
            T1, S1 = self.__TS_Count(X, H1, h)
            if math.isclose(np.linalg.det(S1), 0.0):
                continue
            else:
                i += 1
            Snew, Hnew = self.__CStepFor500(X, T1, S1, n, h)
            HiSaver500.append([np.linalg.det(Snew), Hnew.copy()])

        del dnew
        del Snew

        # diSaver500 содержит [детерминант S, [di, положение элемента в списке исходных иксов]]
        HiSaver500.sort(key=KeyFuncion)

        # Выбираем 10 векторов с наименьшим значением S
        step = 0
        while len(HiSaver10) < lowestNumber:
            HiSaver10.append(HiSaver500[step].copy())
            step += 1
        HiSaver500.clear()

        HiEndVector = []
        # Реализация третьего пункта
        for i in range(10):
            H1 = HiSaver10[i][1].copy()
            T3, S3 = self.__TS_Count(X, H1, h)
            Snew, Hnew = self.__CStepFor10(X, T3, S3, n, h)
            HiEndVector.append([np.linalg.det(Snew), Hnew.copy()])

        HiEndVector.sort(key=KeyFuncion)

        X = self.__ReturnListX(X, HiEndVector[0][1], h)
        Y = np.array(self.__ReturnListY(HiEndVector[0][1], h))
        return X, Y

