import numpy as np
import mcd_method.MCD_Three_variables as MCD_Three_variables

import LS
import M_Estimators as MEst
import ExtraThings as ex
import generators.FactoryForModels as FactoryForModels

import matplotlib.pyplot as plt



class StandForFourMethods:
    def __filingMatrixX(self, xall, n):
        Xsaver = []
        for i in range(n):
            Xsaver.append([1.0, xall[0][i], xall[1][i]])
        Xsaver = np.array(Xsaver)
        return Xsaver

    def __MiddleTettas(self, tettas):
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

    def __CreateGrafic(self, fileName, path, outSaverX, paramMethodsY, about, xlabel, ylabel):

        iLS = paramMethodsY["iLS"]
        iMCD = paramMethodsY["iMCD"]
        iHuber = paramMethodsY["iHuber"]
        iCauchy = paramMethodsY["iCauchy"]

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось ординат
        plt.grid()  # включение отображение сетки
        plt.plot(
            outSaverX, iLS,
            outSaverX, iMCD,
            outSaverX, iHuber,
            outSaverX, iCauchy
        )  # построение графика
        plt.legend((
            about[0],
            about[1],
            about[2],
            about[3]
        ))
        plt.savefig(path + fileName)
        plt.show()


    def Main_StandForFourMethods(self, params, mode):
        n = params["n"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        nCycle = params["nCycle"]

        outSaver, nSaver = [], []
        iLS, iMCD, iCauchy, iHuber = [], [], [], []


        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()

        while outlier <= 0.25:
            LSsaver = []
            MCDsaver_ = []
            Hubersaver = []
            Cauchysaver = []

            params["outlier"] = outlier

            for i in range(nCycle):
                Y, xAll = modelForData.Main_Model(params=params)
                h = int(n * (1 - outlier))

                xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
                xMatrixMCD_ = self.__filingMatrixX(xall=xVectorMCD_, n=h)
                tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
                MCDsaver_.append(tettaMCD_.copy())

                X = self.__filingMatrixX(xAll, n)
                tettaLS = LSObject.LSMatrix(X, Y)
                LSsaver.append(tettaLS.copy())

                tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, Y, n)
                Hubersaver.append(tettaMEstHuber.copy())

                tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, Y, n)
                Cauchysaver.append(tettaMEstCauchy.copy())
                print(f" i == {i}\n")

            extraObj = ex.ExtraThings()
            iLS.append(extraObj.MainCount(LSsaver, tetta, nCycle)[0])
            iMCD.append(extraObj.MainCount(MCDsaver_, tetta, nCycle)[0])
            iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
            iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])

            print(f" Outlier == {outlier}\n")
            outSaver.append(outlier)
            outlier += 0.03

            # nSaver.append(n)
            # n += 40
        self.__CreateGrafic(fileName="SFFM_FourMethods", path="grafics/", outSaverX=outSaver,
                            paramMethodsY={"iLS": iLS, "iMCD": iMCD, "iHuber": iHuber, "iCauchy": iCauchy},
                            about=["LS", "MCD", "Huber", "Cauchy"], xlabel="Выбросы", ylabel="Показатель точности")
        print(outSaver)
