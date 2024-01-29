import numpy as np
import MCD
import MCD_Test
import MCD_Three_variables

import LMS
import M_Estimators as MEst
import ExtraThings as ex

import matplotlib.pyplot as plt
def filingMatrixX(xall, n):
    Xsaver = []
    for i in range(n):
        Xsaver.append([1.0, xall[0][i], xall[1][i]])
    Xsaver = np.array(Xsaver)
    return Xsaver


def MiddleTettas(tettas):
    n = len(tettas)
    summa = [0., 0., 0.]
    for vector in tettas:
        i = 0
        for element in vector:
            summa[i] += element[0]
            i += 1
    for i in range(len(summa)):
        summa[i] /= n
    return summa

def main():
    n, tetta, p = 500, np.array([1., 1.5, 2.]), 3
    limit = 10.0
    Outlier = 0.17
    varMainObservations = 0.1
    varEmissions = 50.

    outSaver, nSaver = [], []
    iLS, iMCD, iCauchy, iHuber = [], [], [], []

    LSObject = LMS.LS()
    MObject = MEst.M_Estimators()
    mcdMethod = MCD.MCD()
    mcdMethod_test = MCD_Test.MCD()
    mcdMethod_three_var = MCD_Three_variables.MCD()

    Ncycle = 2

    while Outlier <= 0.25:
        LSsaver = []
        MCDsaver = []
        MCDsaver_ = []
        Hubersaver = []
        Cauchysaver = []

        h = int((1. - Outlier) * n)

        for i in range(Ncycle):

            Y, xAll = LSObject.ylinealModel(n, tetta, Outlier, limit, varMainObservations, varEmissions)


            xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
            xMatrixMCD_ = filingMatrixX(xall=xVectorMCD_, n=h)
            tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
            MCDsaver_.append(tettaMCD_.copy())

            # xVectorMCD, yVectorMCD = mcdMethod.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
            # xMatrixMCD = filingMatrixX(xall=xVectorMCD, n=h)
            # tettaMCD = LSObject.LSMatrix(xMatrixMCD, yVectorMCD)
            # MCDsaver.append(tettaMCD.copy())

            X = filingMatrixX(xAll, n)
            tettaLS = LSObject.LSMatrix(X, Y)
            LSsaver.append(tettaLS.copy())
            # tettaLSTest = np.linalg.lstsq(X, Y, rcond=None)[0]


            tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, Y, n)
            Hubersaver.append(tettaMEstHuber.copy())

            tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, Y, n)
            Cauchysaver.append(tettaMEstCauchy.copy())
            print(f" i == {i}\n")
        
        extraObj = ex.ExtraThings()
        iLS.append(extraObj.MainCount(LSsaver, tetta, Ncycle)[0])
        iMCD.append(extraObj.MainCount(MCDsaver, tetta, Ncycle)[0])
        iHuber.append(extraObj.MainCount(Hubersaver, tetta, Ncycle)[0])
        iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, Ncycle)[0])

        print(f" i == {n}\n")
        outSaver.append(Outlier)
        Outlier += 0.05

        # nSaver.append(n)
        # n += 40

    plt.plot()
    plt.xlabel("Выбросы")  # ось абсцисс
    plt.ylabel("Показатель точности")  # ось ординат
    plt.grid()  # включение отображение сетки
    plt.plot(outSaver, iLS,
             outSaver, iMCD,
             outSaver, iHuber,
             outSaver, iCauchy)  # построение графика
    plt.legend(("LS",
                "MCD",
                "Huber",
                "Cauchy"))
    plt.show()

if __name__ == '__main__':
    main()

