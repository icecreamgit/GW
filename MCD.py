import random

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
    return item[1]
class MCD:
    def __init__(self, X, Y, n, p):
        self.X = X
        self.n = n
        self.p = p
        self.Y = Y
    def LineInVector(self, vector):
        newList = [[], []]
        counter = 0
        for line in newList:
            for j in range(self.n):
                line.append(vector[counter])
                counter += 1
        return newList
    def GameOfValues(self, data, h):
        # Рандомно вытаскиваю из исходной матрицы Х значения
        newList = [[], []]
        vector = [i for i in range(self.n)]

        for i in range(h):
            item = random.choice(vector)
            newList[0]. append(data[0][item])
            newList[1].append(data[1][item])
            vector.remove(item)
        return newList
    def CreateNewListCstep(self, data, di, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            index = di[i][0]
            newList[0].append(data[0][index])
            newList[1].append(data[1][index])
        return newList
    def T0(self, xMassive, h):
        # Вычисляю мат. ожидание
        mean = 0.
        for value in xMassive:
            mean += value
        return mean / h

    def Cstep(self, data, sComparision, h):
        B, di = [], []
        flag = True
        alarm = 1
        S = np.zeros((2, 2))
        while flag == True:
            S = np.cov(data, bias=True)
            if np.linalg.det(S) == np.linalg.det(sComparision):
                alarm = 0
                flag = False
                continue

            mean_X0 = self.T0(data[0], h)
            mean_X1 = self.T0(data[1], h)
            for i in range(h):
                B.append([[data[0][i] - mean_X0], [data[1][i] - mean_X1]])

            for i in range(h):
                a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
                di.append([i, np.dot(a, np.array(B[i]))[0][0]])
            di.sort(key=KeyFuncion)
            flag = False
        return {"di": di, "S": S}, alarm

    def FindRelativeDistances(self, X, n, mode):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        B, xInterm, diSaver500, di = [], [[], []], [], []
        sMatrix = np.zeros((2, 2))
        cStepNumber = 500

        h = int((self.n + self.p + 1) / 2)
        dataStart = self.LineInVector(X)

        for i in range(cStepNumber):
            newData = self.GameOfValues(dataStart, h)
            for step in range(2):
                container, alarm = self.Cstep(newData, sMatrix, h)
                if alarm != 0:
                    di = container["di"]
                    sMatrix = container["S"]
                    self.CreateNewListCstep(data=newData, di=di, h=h)
                else:
                    break
            diSaver500.append([di, sMatrix])
        a = 0
        # if (mode == "TestTask"):
        #     xInterm = xObject.MatrixInVector([[], []], X="a")
        #     data = np.array([xInterm[0], xInterm[1]])
        #     self.CreateNewList(data)
        #     S = np.cov(data, bias=True)
        #
        #     if np.linalg.det(S) == 0:
        #         print("det(S) == 0!")
        #
        #     mean_X0 = self.T0(xInterm, 0, n)
        #     mean_X1 = self.T0(xInterm, 1, n)
        #     for i in range(n):
        #         B.append([[xInterm[0][i] - mean_X0], [xInterm[1][i] - mean_X1]])
        #
        #     for i in range(n):
        #         a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
        #         self.di.append([i, np.dot(a, np.array(B[i]))[0][0]])
        #     self.di.sort(key=KeyFuncion)
        # else:
        #     while 1:
        #         h = int((n + p + 1) / 2)
        #         xInterm = xObject.MatrixInVector([[], []], X="a")
        #         data = np.array([xInterm[0], xInterm[1]])
        #         S = np.cov(data, bias=True)
        #
        #         if math.isclose(np.linalg.det(S), 0):
        #             print("det(S) == 0!")
        #             break
        #
        #         mean_X0 = self.T0(xInterm, 0, h)
        #         mean_X1 = self.T0(xInterm, 1, h)
        #         for i in range(h):
        #             B.append([[xInterm[0][i] - mean_X0], [xInterm[1][i] - mean_X1]])
        #
        #         for i in range(h):
        #             a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
        #             self.di.append(np.dot(a, np.array(B[i]))[0][0])
        #         xInterm.clear()
        # B.clear()
        # xInterm.clear()

