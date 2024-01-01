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
    def __GameOfValues(self, data, h):
        # Рандомно вытаскиваю из исходной матрицы Х значения
        newList = [[], []]
        vector = [i for i in range(self.n)]

        for i in range(h):
            item = np.random.choice(vector)

            newList[0].append(data[0][item])
            newList[1].append(data[1][item])

            vector.remove(item)
        return newList
    def __CreateNewListCstep(self, data, di, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            index = di[i][1]
            newList[0].append(data[0][index])
            newList[1].append(data[1][index])
        return newList
    def __Di(self, X, listH, n):
        B, di = [], []
        S = np.cov(listH)
        mean_X0 = np.mean(listH[0])
        mean_X1 = np.mean(listH[1])

        for i in range(n):
            B.append([[X[0][i] - mean_X0], [X[1][i] - mean_X1]])

        B = np.array(B)
        for i in range(n):
            C0 = reduce(np.dot, [B[i].transpose(), np.linalg.inv(S), B[i]])[0][0]
            di.append([np.sqrt(C0), i])
        return di, S

    def __CstepForFirstStep(self, X, n, h, numberItter):
        # data - матрица из двух векторов: х1 и х2
        dnew, Snew = [], [[], []]

        JList = self.__GameOfValues(X, h)
        d0, S0 = self.__Di(X, JList, n)
        d0.sort(key=KeyFuncion)
        H1List = self.__CreateNewListCstep(X, d0, h)

        for i in range(numberItter):
            dold, Sold = self.__Di(X, H1List, n)
            dold.sort(key=KeyFuncion)

            HnewList = self.__CreateNewListCstep(X, dold, h)
            dnew, Snew = self.__Di(X, HnewList, n)
            dnew.sort(key=KeyFuncion)

            detS2 = np.linalg.det(Snew)
            detS1 = np.linalg.det(Sold)

            H1List = HnewList.copy()

            if math.isclose(detS2, detS1) or math.isclose(detS2, 0.0):
                break

        return {"dnew": dnew, "Snew": Snew}

    def __CstepForSecondStep(self, X, diVector, n, h, numberItter):
        # data - матрица из двух векторов: х1 и х2
        resultVector = []

        for i in range(numberItter):

            dold = diVector[i][1]
            HoldList = self.__CreateNewListCstep(data=X, di=dold, h=h)

            while(1):
                dold, Sold = self.__Di(X, HoldList, n)
                dold.sort(key=KeyFuncion)

                HnewList = self.__CreateNewListCstep(data=X, di=dold, h=h)
                dnew, Snew = self.__Di(X, HnewList, n)
                dnew.sort(key=KeyFuncion)

                detS2 = np.linalg.det(Snew)
                detS1 = np.linalg.det(Sold)

                HoldList = HnewList.copy()

                if math.isclose(detS2, detS1) or math.isclose(detS2, 0.0):
                    break


            resultVector.append([np.linalg.det(Snew), dnew.copy()])
        return resultVector

#####################################################___NEW
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

        T.append([T1mean, T2mean])
        T = np.array(T)
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
            dold = self.__Di2(X, T[i][0], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(X, Hnew, h)
            T.append(Tnew)
            S.append(Snew)
        dOutput = self.__Di2(X, T[2][0], S[2], n)
        dOutput.sort(key=KeyFuncion)

        # return S3, doutput
        return S[2], dOutput
    def __CStepFor10(self, X, T3, S3, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T3)
        S.append(S3)
        for i in range(10000):
            dold = self.__Di2(X, T[i][0], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(X, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS3 = np.linalg.det(S[i])
            detS4 = np.linalg.det(S[i + 1])
            if math.isclose(detS4, detS3) or math.isclose(detS4, 0.0):
                break
        index = len(T) - 1
        dOutput = self.__Di2(X, T[index][0], S[index], n)
        dOutput.sort(key=KeyFuncion)

        # return S3, doutput
        return S[index], dOutput

    def FindRelativeDistances(self, X, n, h):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        diSaver10, diSaver500, diEndVector, dnew, Snew = [], [], [], [], [[], []]
        cStepNumber, lowestNumber = 500, 10

        # Реализация первого пункта задания с созданием 500 di расстояний
        for i in range(cStepNumber):
            H1 = self.__H1Generate(h, n)
            T1, S1 = self.__TS_Count(X, H1, h)
            Snew, dnew = self.__CStepFor500(X, T1, S1, n, h)

            # container = self.__CstepForFirstStep(X, n, h, numberItter=2)
            # dnew = container["dnew"].copy()
            # Snew = container["Snew"].copy()

            diSaver500.append([np.linalg.det(Snew), dnew.copy()])

        del dnew
        del Snew

        # diSaver500 содержит [детерминант S, [di, положение элемента в списке исходных иксов]]
        diSaver500.sort(key=KeyFuncion)

        # Выбираем 10 векторов с наименьшим значением S
        step = 0
        while len(diSaver10) < lowestNumber:
            if step > 0:
                if diSaver500[step][0] == diSaver500[step-1][0]:
                    diSaver500.remove(diSaver500[step])
                    step += 1
                    continue

            diSaver10.append(diSaver500[step].copy())
            step += 1
        diSaver500.clear()


        # Реализация третьего пункта
        for i in range(10):
            H1 = self.__ChooseHValues(diSaver10[i][1], h)
            T3, S3 = self.__TS_Count(X, H1, h)
            Snew, dnew = self.__CStepFor10(X, T3, S3, n, h)
            diEndVector.append([np.linalg.det(Snew), dnew.copy()])

        # diEndVector = self.__CstepForSecondStep(X, diSaver10, n, h, numberItter=lowestNumber)
        diEndVector.sort(key=KeyFuncion)

        X = self.__CreateNewListCstep(X, diEndVector[0][1], h)
        Y = np.array(self.__ReturnY(diEndVector[0][1], h))
        return X, Y

