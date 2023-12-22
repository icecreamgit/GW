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
    def __init__(self, X, Y, n, p):
        self.X = X
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

    def __ReturnVector(self, data, di, h):
        newList = []
        for i in range(h):
            index = di[i][1]
            newList.append(data[0][index])
        for i in range(h):
            index = di[i][1]
            newList.append(data[1][index])
        return newList
    def __ReturnY(self, di, h):
        newList = []
        for i in range(h):
            index = di[i][1]
            newList.append(self.Y[index])
        return newList
    def __GameOfValues(self, data, h):
        # Рандомно вытаскиваю из исходной матрицы Х значения
        newList = [[], []]
        newKeys = []
        vector = []
        vector = [i for i in range(self.n)]

        for i in range(h):
            item = np.random.choice(vector)

            newKeys.append(item)
            newList[0].append(data[0][item])
            newList[1].append(data[1][item])

            vector.remove(item)
        return newList, newKeys
    def __CreateNewListCstep(self, data, di, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        newKeys = []
        for i in range(h):
            index = di[i][1]
            newKeys.append(index)
            newList[0].append(data[0][index])
            newList[1].append(data[1][index])
        return newList, newKeys
    def __Di(self, data, keys, h):
        B, di = [], []
        S = np.cov(data, bias=True)
        mean_X0 = np.mean(data[0])
        mean_X1 = np.mean(data[1])
        for i in range(h):
            B.append([[data[0][i] - mean_X0], [data[1][i] - mean_X1]])

        B = np.array(B)
        for i in range(h):
            C0 = reduce(np.dot, [B[i].transpose(), np.linalg.inv(S), B[i]])[0][0]
            di.append([np.sqrt(C0), keys[i]])

        return di, S

    def __Cstep(self, dataStart, newList, keys, h, numberItter):
        # data - матрица из двух векторов: х1 и х2

        dnew, Snew = [], [[], []]
        dold, Sold = self.__Di(newList, keys, h)
        dold.sort(key=KeyFuncion)

        for i in range(numberItter):
            HnewList, HnewKeys = self.__CreateNewListCstep(dataStart, dold, h)
            dnew, Snew = self.__Di(HnewList, keys, h)
            dnew.sort(key=KeyFuncion)

            detS2 = np.linalg.det(Snew)
            detS1 = np.linalg.det(Sold)
            if math.isclose(detS2, detS1) or detS2 < detS1:
                break
            else:
                dold = dnew
                Sold = Snew
        return {"dnew": dnew, "Snew": Snew}

    def FindRelativeDistances(self, X, n, h):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        diSaver10, diSaver500, diEndVector, dnew = [], [], [], []
        newKeys, newList = [], []
        cStepNumber, lowestNumber = 500, 10

        dataStart = self.__LineInVector(X)
        # Реализация первого пункта задания с созданием 500 di расстояний
        for i in range(cStepNumber):
            newList, newKeys = self.__GameOfValues(dataStart, h)

            container = self.__Cstep(dataStart, newList, newKeys, h, numberItter=2)
            dnew = container["dnew"]
            Snew = container["Snew"]

            diSaver500.append([np.linalg.det(Snew), dnew.copy()])

        dnew.clear()
        newKeys.clear()
        newList.clear()


        # diSaver500 содержит [детерминант S, [di, положение элемента в списке исходных иксов]]
        diSaver500.sort(key=KeyFuncion)

        # Выбираем 10 векторов с наименьшим значением S
        for step in range(lowestNumber):
            diSaver10.append(diSaver500[step].copy())
        diSaver500.clear()


        # Реализация третьего пункта
        for i in range(lowestNumber):
            newList, newKeys = self.__CreateNewListCstep(data=dataStart, di=diSaver10[i][1], h=h)

            container = self.__Cstep(dataStart, newList, newKeys, h, numberItter=1000000)
            dnew = container["dnew"]
            Snew = container["Snew"]

            diEndVector.append([np.linalg.det(Snew), dnew.copy()])
        diSaver10.clear()
        diEndVector.sort(key=KeyFuncion)

        X = self.__ReturnVector(dataStart, diEndVector[0][1], h)
        Y = np.array(self.__ReturnY(diEndVector[0][1], h))
        return X, Y

