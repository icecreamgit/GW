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
    return item[0]

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

    def ReturnVector(self, data, di, h):
        newList = []
        for i in range(h):
            index = di[i][1]
            newList.append(data[0][index])
        for i in range(h):
            index = di[i][1]
            newList.append(data[1][index])
        return newList
    def ReturnY(self, di, h):
        newList = []
        for i in range(h):
            index = di[i][1]
            newList.append(self.Y[index])
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
            index = di[i][1]
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
        # data - матрица из двух векторов: х1 и х2
        B, di = [], []
        flag = True
        alarm = 1
        S = np.zeros((2, 2))
        while flag == True:
            S = np.cov(data, bias=True)
            a0 = np.linalg.det(S)
            if math.isclose(a0, sComparision):
                alarm = 0
                flag = False
                continue

            mean_X0 = self.T0(data[0], h)
            mean_X1 = self.T0(data[1], h)
            for i in range(h):
                B.append([[data[0][i] - mean_X0], [data[1][i] - mean_X1]])

            for i in range(h):
                a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
                di.append([np.dot(a, np.array(B[i]))[0][0], i])
            di.sort(key=KeyFuncion)
            flag = False
        return {"di": di, "S": S}, alarm

    def FindRelativeDistances(self, X, n, mode):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        diSaver10, diSaver500, diEndVector, di = [], [], [], []
        sMatrix = np.zeros((2, 2))
        cStepNumber, lowestNumber = 500, 10

        h = int((self.n + self.p + 1) / 2)
        dataStart = self.LineInVector(X)

        # Реализация первого пункта задания с созданием 500 di расстояний
        for i in range(cStepNumber):
            newData = self.GameOfValues(dataStart, h)
            for step in range(2):
                container, alarm = self.Cstep(newData, np.linalg.det(sMatrix), h)
                if alarm != 0:
                    di = container["di"]
                    sMatrix = container["S"]
                    newData = self.CreateNewListCstep(data=newData, di=di, h=h)
                else:
                    break
            diSaver500.append([np.linalg.det(sMatrix), di])
        di.clear()

        # diSaver500 содержит [детерминант S, di - вектор]
        diSaver500.sort(key=KeyFuncion)

        # Выбираем 10 векторов с наименьшим значением S
        for step in range(lowestNumber):
            diSaver10.append(diSaver500[step])
        diSaver500.clear()


        # Реализация третьего пункта
        for i in range(lowestNumber):
            alarm = 1
            newData = self.CreateNewListCstep(data=dataStart, di=diSaver10[i][1], h=h)
            sMatrix = np.zeros((2, 2))
            while alarm != 0:
                # Тут остановился
                container, alarm = self.Cstep(newData, np.linalg.det(sMatrix), h)
                if alarm != 0:
                    di = container["di"]
                    sMatrix = container["S"]
                    newData = self.CreateNewListCstep(data=dataStart, di=di, h=h)
                else:
                    break
            diEndVector.append([np.linalg.det(sMatrix), di])


        x = self.ReturnVector(dataStart, diEndVector[0][1], h)
        y = np.array(self.ReturnY(diEndVector[0][1], h))
        return x, y

