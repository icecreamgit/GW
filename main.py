import numpy as np
import random
import MCD
import LMS
import M_Estimators as MEst
import ExtraThings as ex

import matplotlib.pyplot as plt
def filingMatrixX(xall, n, tetta):
    Xsaver = []
    for i in range(n):
        Xsaver.append([1.0, xall[0][i], xall[1][i]])
    Xsaver = np.array(Xsaver)
    return Xsaver

def relativeError(tettaTrue, tettanew):
    n, counter = len(tettaTrue), 0
    for stepi in range(n):
        counter += pow((tettaTrue[stepi] - tettanew[stepi]), 2) / pow(tettaTrue[stepi], 2)
    return counter

def CheckList(randomIndexes, el):
    for i in randomIndexes:
        if i == el:
            return True
    return False

def TestSelectiveVaribles(X, Y, n, testFactor):
    xObject = MCD.Transform(X, n)
    xNew = xObject.MatrixInVector(xInterm=[[], []], X="a")
    yNew = Y.tolist()
    element = 0
    h = [i for i in range(n)]
    for i in range(0, len(xNew)):
        randomIndexes = []
        for j in range(int(testFactor * n)):
            testExistance = True
            while testExistance:
                element = random.choice(h)
                testExistance = CheckList(randomIndexes, element)
            randomIndexes.append(element)
        randomIndexes.sort(reverse=True)
        for j in randomIndexes:
            xNew[i].pop(j)
            if i == 0:
                yNew.pop(j)
    xNewArray = xObject.VectorInMatrix(xNew, [])
    xNew.clear()
    return xNewArray, np.array(yNew)

def main():
    n, tetta, p = 200, np.array([1., 1.5, 2.]), 3
    h = int( (n+p+1) / 2.)
    outSaver = []
    Outlier = 0.
    LSObject = LMS.LMS(n=n, tetta=tetta, outlier=Outlier)
    MObject = MEst.M_Estimators()
    LSsaver = []
    MCDsaver = []
    Hubersaver = []
    Cauchysaver = []

    Ncycle = 100
    iLS, iMCD, iCauchy, iHuber = [], [], [], []

    while Outlier < 0.25:
        for i in range(Ncycle):

            Y, xAll = LSObject.ylinealModel(n=n, tetta=tetta, outlier=Outlier)
            X = filingMatrixX(xAll, n, tetta)
            tettaLS = LSObject.LSMatrix(X, Y)
            LSsaver.append(tettaLS.copy())

            # mcdMethod = MCD.MCD(Y, n, p)
            # xVectorMCD, yVectorMCD = mcdMethod.FindRelativeDistances(X=xAll, n=n, h=h)
            # xMatrixMCD = filingMatrixX(x=np.zeros((h, len(tetta))), xall=LSObject.lineToColum(xVectorMCD, h, tetta), tetta=tetta)
            # tettaMCD = LSObject.LSMatrix(xMatrixMCD, yVectorMCD)
            # MCDsaver.append(tettaMCD.copy())


            tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, Y, n)
            Hubersaver.append(tettaMEstHuber.copy())

            tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, Y, n)
            Cauchysaver.append(tettaMEstCauchy.copy())

            print(f" i == {i}\ntettaLS:\n{tettaLS}\n"
                  # f"tettaMCD:\n{tettaMCD}\n"
                  f"tettaMEstHuber\n{tettaMEstHuber}\n"
                  f"tettaMEstCauchy\n{tettaMEstCauchy}\n")

        extraObj = ex.ExtraThings()
        iLS.append(extraObj.MainCount(LSsaver, tetta, Ncycle, "LS")[0])
        # iMCD.append(extraObj.MainCount(MCDsaver, tetta, Ncycle, "MCD")[0])
        iHuber.append(extraObj.MainCount(Hubersaver, tetta, Ncycle, "Huber")[0])
        iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, Ncycle, "Cauchy")[0])

        LSsaver = []
        MCDsaver = []
        Hubersaver = []
        Cauchysaver = []
        outSaver.append(Outlier)
        Outlier += 0.05

    plt.plot()
    plt.xlabel("Выбросы")  # ось абсцисс
    plt.ylabel("Показатель точности")  # ось ординат
    plt.grid()  # включение отображение сетки
    plt.plot(outSaver, iLS, outSaver, iHuber, outSaver, iCauchy)  # построение графика
    plt.legend(("LS", "Huber", "Cauchy"))
    plt.show()

if __name__ == '__main__':
    main()

