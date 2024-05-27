from functools import reduce
from itertools import chain

import numpy as np
import math


def KeyFuncion(item):
    return item[0]

class MCD_Modified:

    def __ReturnListX_Mod(self, Z, Hnew, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            j = Hnew[i]
            newList[0].append(Z[j][0])
            newList[1].append(Z[j][1])
        return newList

    def __ReturnListY_Mod(self, Z, Hnew, h):
        newList = []
        for i in range(h):
            index = Hnew[i]
            newList.append(Z[index][2])
        return np.array(newList).reshape(h, 1)


    def __H1Generate(self, h, n):
        vector = [i for i in range(n)]
        H1 = np.random.choice(vector, size=h, replace=False)
        return H1

    def __H1Generate_Mod(self, listOfIndexes, m):
        H1 = np.random.choice(listOfIndexes, size=m, replace=False)
        return H1

    def __TS_Count(self, X, Y, H, h):
        x1 = []
        x2 = []
        y = []
        # Создание Х1 и Х2, принадлежащие H вектору
        for i in range(h):
            trueIndex = H[i]
            x1.append(X[0][trueIndex])
            x2.append(X[1][trueIndex])
            y.append(Y[trueIndex][0])

        x = np.stack((x1, x2, y))

        T1mean = np.mean(x[0])
        T2mean = np.mean(x[1])
        T3mean = np.mean(y)

        S = np.cov(x, bias=True)

        T = np.array([T1mean, T2mean, T3mean])
        return T, S

    def __TS_Modified(self, Z, H, h):
        x1 = []
        x2 = []
        y = []
        # Создание Х1 и Х2, принадлежащие H вектору
        for i in range(h):
            trueIndex = H[i]
            x1.append(Z[trueIndex][0])
            x2.append(Z[trueIndex][1])
            y.append(Z[trueIndex][2])

        x = np.stack((x1, x2, y))

        T1mean = np.mean(x[0])
        T2mean = np.mean(x[1])
        T3mean = np.mean(y)

        S = np.cov(x, bias=True)

        T = np.array([T1mean, T2mean, T3mean])
        return T, S

    def __Di_Modified(self, X, Y, Z, T, S, n):
        B, di = [], []
        indexesZones = []
        for i in range(n):
            B.append([[Z[i][0] - T[0]], [Z[i][1] - T[1]], [Z[i][2] - T[2]]])
            indexesZones.append(Z[i][3])

        B = np.array(B)
        Sinv = np.linalg.inv(S)
        for i in range(n):
            C0 = reduce(np.dot, [B[i].T, Sinv, B[i]])[0][0]
            di.append([np.sqrt(C0), i, indexesZones[i]])
        return di

    def __ChooseHValues_Modified(self, dold, sampleSizesH, n):
        Hnew, indexZeroZone, indexFirstZone, indexSecondZone, indexThirdZone, indexForthZone = [], 0, 0, 0, 0, 0

        for i in range(n):
            if (dold[i][2] == 0 and indexZeroZone < sampleSizesH[0]):
                Hnew.append(dold[i][1])
                indexFirstZone += 1
                continue
            if (dold[i][2] == 1 and indexFirstZone < sampleSizesH[1]):
                Hnew.append(dold[i][1])
                indexFirstZone += 1
                continue

            if (dold[i][2] == 2 and indexSecondZone < sampleSizesH[2]):
                Hnew.append(dold[i][1])
                indexSecondZone += 1
                continue

            if (dold[i][2] == 3 and indexThirdZone < sampleSizesH[3]):
                Hnew.append(dold[i][1])
                indexThirdZone += 1
                continue

            if (dold[i][2] == 4 and indexForthZone < sampleSizesH[4]):
                Hnew.append(dold[i][1])
                indexForthZone += 1
                continue
        return Hnew
    def __Di(self, X, Y, T, S, n):
        B, di = [], []

        for i in range(n):
            B.append([[X[0][i] - T[0]], [X[1][i] - T[1]], [Y[i][0] - T[2]]])

        B = np.array(B)
        Sinv = np.linalg.inv(S)
        for i in range(n):
            C0 = reduce(np.dot, [B[i].T, Sinv, B[i]])[0][0]
            di.append([np.sqrt(C0), i])
        return di
    def __ChooseHValues(self, dold, h):
        Hnew = []
        for i in range(h):
            Hnew.append(dold[i][1])
        return Hnew
    def __CStepFor500(self, X, Y, Z, sampleSizesH, T1, S1, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T1)
        S.append(S1)
        for i in range(2):
            # dold = self.__Di(X, Y, T[i], S[i], n)
            # dold.sort(key=KeyFuncion)
            # Hnew = self.__ChooseHValues(dold, h)

            dold = self.__Di_Modified(X, Y, Z, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues_Modified(dold, sampleSizesH, n)

            Tnew, Snew = self.__TS_Modified(Z, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS1 = np.linalg.det(S[i])
            detS2 = np.linalg.det(S[i + 1])
            if math.isclose(detS2, 0.0):
                print(f"inside method c500 detS2 is zero")
                break
        # return S3
        return S[len(S) - 1], T[len(T) - 1]

    def __CStepFor10(self, X, Y, Z, sampleSizesH, T3, S3, n, h):
        T = []
        S = []

        T.append(T3)
        S.append(S3)
        i = 0
        while 1:
            # dold = self.__Di(X, Y, T[i], S[i], n)
            # dold.sort(key=KeyFuncion)
            # Hnew = self.__ChooseHValues(dold, h)

            dold = self.__Di_Modified(X, Y, Z, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues_Modified(dold, sampleSizesH, n)

            Tnew, Snew = self.__TS_Modified(Z, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS3 = np.linalg.det(S[i])
            detS4 = np.linalg.det(S[i + 1])
            i += 1
            if math.isclose(detS4, detS3) or math.isclose(detS4, 0.0):
                break
        # return S3
        return S[i], T[i], Hnew

    def __diTransform(self, di):
        saver = []
        for element in di:
            saver.append(element[0])
        return saver

    def __calibrateInputLenght(self, sampleSizes, n, h, outlier, numberZones):

        c = int((n - sampleSizes[0]) * (1. - outlier))
        sampleSizes[0] *= (1. - outlier)
        hForFourZones = int(c / (numberZones - 1))

        sampleSizesH = [hForFourZones, hForFourZones, hForFourZones, hForFourZones]

        i = 0
        while sum(sampleSizesH) < c:
            sampleSizesH[i] += 1
            i += 1
            if i >= 4:
                i = 0
        sampleSizesH.insert(0, h)
        return sampleSizesH
    def Main_MCD(self, X, Y, outlier, dictionaryZones, sampleSizes, Z, n, h, numberZones):
        HiSaver10, HiSaver500, H1, dnew, Snew = [], [], [], [], [[], []]
        cStepNumber, lowestNumber = 500, 10

        # return xNew, Ynew
        i = 0
        sampleSizeH = []
        if n != h:
            sampleSizesH = self.__calibrateInputLenght(sampleSizes, n, h, outlier, numberZones)
        else:
            sampleSizesH = sampleSizes

        while i < cStepNumber:
            H1 = self.__H1Generate(h, n)
            T1, S1 = self.__TS_Modified(Z, H1, h)
            if math.isclose(np.linalg.det(S1), 0.0):
                continue
            else:
                i += 1
            Snew, Tnew = self.__CStepFor500(X, Y, Z, sampleSizesH, T1, S1, n, h)
            HiSaver500.append([np.linalg.det(Snew), Snew.copy(), Tnew.copy()])

        # diSaver500 содержит [детерминант S, [di, положение элемента в списке исходных иксов]]
        HiSaver500.sort(key=KeyFuncion)

        # Выбираем 10 векторов с наименьшим значением S
        step = 0
        while len(HiSaver10) < lowestNumber:
            HiSaver10.append(HiSaver500[step].copy())
            step += 1
        HiSaver500.clear()

        T_H_EndVector = []
        # Реализация третьего пункта
        for i in range(10):
            S3 = HiSaver10[i][1]
            T3 = HiSaver10[i][2]
            Snew, Tnew, Hnew = self.__CStepFor10(X, Y, Z, sampleSizesH, T3, S3, n, h)
            T_H_EndVector.append([np.linalg.det(Snew), Snew.copy(), Tnew.copy()])

        T_H_EndVector.sort(key=KeyFuncion)

        Snew = T_H_EndVector[0][1]
        Tnew = T_H_EndVector[0][2]

        diEnd = self.__Di_Modified(X, Y, Z, Tnew, Snew, n)
        diEnd.sort(key=KeyFuncion)
        # HEnd = self.__ChooseHValues(diEnd, h)
        HEnd = self.__ChooseHValues_Modified(diEnd, sampleSizesH, n)

        X_ = self.__ReturnListX_Mod(Z, HEnd, h)
        Y_ = self.__ReturnListY_Mod(Z, HEnd, h)
        return X_, Y_

