from functools import reduce
import collections
import numpy as np
import math

def KeyFuncion(item):
    return item[0]

class MCD:
    def __ReturnListX(self, X, Hnew, h):
        # Превращаю вектор расстояний di обратно в матрицу, чтобы засунуть в С-шаг
        newList = [[], []]
        for i in range(h):
            j = Hnew[i]
            newList[0].append(X[0][j])
            newList[1].append(X[1][j])
        return newList
    def __ReturnListY(self, Y, Hnew, h):
        newList = []
        for i in range(h):
            index = Hnew[i]
            newList.append(Y[index])
        return newList
    def __H1Generate(self, h, n):
        vector = [i for i in range(n)]
        H1 = np.random.choice(vector, size=h, replace=False)
        return H1

    def __TS_Count(self, Y, H, h):
        HValuesList = [ ]
        T1mean, T2mean, T = 0.0, 0.0, []

        # Создание Х1 и Х2, принадлежащие H вектору
        for i in range(h):
            trueIndex = H[i]
            HValuesList.append(Y[trueIndex][0])


        T1mean = np.mean(HValuesList)

        S = np.cov(HValuesList, bias=True)
        T = np.array([T1mean])
        return T, S

    def __Di(self, Y, T, S, n):
        B, di = [], []

        for i in range(n):
            B.append([Y[i] - T[0]])

        B = np.array(B)
        for i in range(n):
            C0 = reduce(np.dot, [B[i].transpose(), pow(S, -1), B[i]])[0]
            di.append([np.sqrt(C0)[0], i])
        return di
    def __ChooseHValues(self, dold, h):
        Hnew = []
        for i in range(h):
            Hnew.append(dold[i][1])
        return Hnew
    def __CStepFor500(self, Y, T1, S1, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T1)
        S.append(S1)
        for i in range(2):
            dold = self.__Di(Y, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(Y, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS1 = (S[i])
            detS2 = (S[i + 1])
            if math.isclose(detS2, 0.0):
                print(f"inside method c500 detS2 is zero")
                break
        # return S3
        return S[len(S) - 1], T[len(T) - 1]
    def __CStepFor10(self,Y, T3, S3, n, h):
        T = []
        S = []
        Hnew = []

        T.append(T3)
        S.append(S3)
        i = 0
        while 1:
            dold = self.__Di(Y, T[i], S[i], n)
            dold.sort(key=KeyFuncion)
            Hnew = self.__ChooseHValues(dold, h)
            Tnew, Snew = self.__TS_Count(Y, Hnew, h)
            T.append(Tnew)
            S.append(Snew)

            detS3 = (S[i])
            detS4 = (S[i + 1])
            i += 1
            if math.isclose(detS4, detS3) or math.isclose(detS4, 0.0):
                break
        # return S3
        return S[i], T[i]

    def FindRelativeDistances(self, X, Y, n, h):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        HiSaver10, HiSaver500, H1, dnew, Snew = [], [], [], [], [[], []]
        cStepNumber, lowestNumber = 500, 10

        # Реализация первого пункта задания с созданием 500 di расстояний
        i = 0
        while i < cStepNumber:
            H1 = self.__H1Generate(h, n)
            T1, S1 = self.__TS_Count(Y, H1, h)
            if math.isclose(S1, 0.0):
                continue
            else:
                i += 1
            Snew, Tnew = self.__CStepFor500(Y, T1, S1, n, h)
            HiSaver500.append([Snew.copy(), Snew.copy(), Tnew.copy()])

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
            Snew, Tnew = self.__CStepFor10(Y, T3, S3, n, h)
            T_H_EndVector.append([(Snew).copy(), Snew.copy(), Tnew.copy()])

        T_H_EndVector.sort(key=KeyFuncion)

        Snew = T_H_EndVector[0][1]
        Tnew = T_H_EndVector[0][2]
        diEnd = self.__Di(Y, Tnew, Snew, n)
        diEnd.sort(key=KeyFuncion)
        HEnd = self.__ChooseHValues(diEnd, h)

        X_ = self.__ReturnListX(X, HEnd, h)
        Y_ = np.array(self.__ReturnListY(Y, HEnd, h))

        return X_, Y_
