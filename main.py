import numpy as np
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

def MiddleTettas(tettas):
    n = len(tettas)
    summa = [0., 0., 0.]
    for vector in tettas:
        summa += vector
    summa /= n
    return summa

def main():
    n, tetta, p = 500, np.array([1., 1.5, 2.]), 3
    h = int( (n+p+1) / 2.)
    outSaver = []
    Outlier = 0.2
    LSObject = LMS.LMS()
    MObject = MEst.M_Estimators()


    Ncycle = 500
    iLS, iMCD, iCauchy, iHuber = [], [], [], []

    while Outlier < 0.25:
        LSsaver = []
        MCDsaver = []
        Hubersaver = []
        Cauchysaver = []

        for i in range(Ncycle):

            Y, xAll = LSObject.ylinealModel(n=n, tetta=tetta, outlier=Outlier)
            X = filingMatrixX(xAll, n, tetta)
            tettaLS = LSObject.LSMatrix(X, Y)
            LSsaver.append(tettaLS.copy())

            mcdMethod = MCD.MCD(Y, n, p)
            xVectorMCD, yVectorMCD = mcdMethod.FindRelativeDistances(X=xAll, n=n, h=h)
            xMatrixMCD = filingMatrixX(xall=xVectorMCD, n=h, tetta=tetta)
            tettaMCD = LSObject.LSMatrix(xMatrixMCD, yVectorMCD)
            MCDsaver.append(tettaMCD.copy())


            tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, Y, n)
            Hubersaver.append(tettaMEstHuber.copy())

            tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, Y, n)
            Cauchysaver.append(tettaMEstCauchy.copy())
            del Y
            del X
            print(f" i == {i}\n")
        L = MiddleTettas(LSsaver)
        MCD_ = MiddleTettas(MCDsaver)
        Hub_ = MiddleTettas(Hubersaver)
        
        extraObj = ex.ExtraThings()
        iLS.append(extraObj.MainCount(LSsaver, tetta, Ncycle)[0])
        iMCD.append(extraObj.MainCount(MCDsaver, tetta, Ncycle)[0])
        iHuber.append(extraObj.MainCount(Hubersaver, tetta, Ncycle)[0])
        iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, Ncycle)[0])

        print(f" i == {n}\n")
        outSaver.append(Outlier)
        Outlier += 0.05

    plt.plot()
    plt.xlabel("Выбросы")  # ось абсцисс
    plt.ylabel("Показатель точности")  # ось ординат
    plt.grid()  # включение отображение сетки
    plt.plot(outSaver, iLS,
             outSaver, iMCD,
             outSaver, iHuber, outSaver, iCauchy)  # построение графика
    plt.legend(("LS",
                "MCD",
                      "Huber", "Cauchy"))
    plt.show()

if __name__ == '__main__':
    main()

