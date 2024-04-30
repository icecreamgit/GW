import numpy as np
import mcd_method.MCD_Three_variables as MCD_Three_variables
import mcd_method.MCD_Modified as MCD_Modified

import LS
import M_Estimators as MEst
import ExtraThings as ex
import models.FactoryForModels as FactoryForModels

import matplotlib.pyplot as plt


# Класс для работы с неоднородными ошибками
class StandForHGOutliers:
    def __filingMatrixX(self, xall, n):
        Xsaver = []
        for i in range(n):
            Xsaver.append([1.0, xall[0][i], xall[1][i]])
        Xsaver = np.array(Xsaver)
        return Xsaver

    def __YTransformIn_Nx1(self, Ymatrix_Nx2):
        Yout = []
        for line in Ymatrix_Nx2:
            Yout.append(line[0])
        return np.array(Yout).reshape(len(Ymatrix_Nx2), 1)

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
    def __CreateFileForIndexes(self, name, path, LS, MCD, MCD_Modified, Huber, Cauchy, message):
        with open(f"{path}{name}.txt", "w") as file:
            file.write(message)
            file.write(f"\nLS: {LS}\nMCD: {MCD}\nMCD_Modified: {MCD_Modified}\nHuber: {Huber}\nCauchy: {Cauchy}")

    # Стандартная метод для расчёта показателя точности с выбросами
    # Плюс, отрисовывается график для методов MCD, МНК, М-оценок
    def __FunctionForGraficWithOutliers(self, params, mode):
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

        self.__CreateGrafic(fileName=f"SFFM_FourMethods_{mode}_n_{n}_nCycle_{nCycle}_points_{len(outSaver)}",
                            path=f"grafics/{mode}/", outSaverX=outSaver,
                            paramMethodsY={"iLS": iLS, "iMCD": iMCD, "iHuber": iHuber, "iCauchy": iCauchy},
                            about=["LS", "MCD", "Huber", "Cauchy"], xlabel="Выбросы", ylabel="Показатель точности")

    # Стандартная метод для расчёта показателя точности с выбросами
    # График не отрисовывается, но в файл записываются значения показателя точности
    # Эта функция делает то же, что и __FunctionForGraficWithOutliers, просто графики не рисует
    def __FunctionForTextOutput(self, params, mode):
        n = params["n"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        nCycle = params["nCycle"]

        outSaver, nSaver = [], []
        iLS, iMCD, iMCD_Modified, iCauchy, iHuber = [], [], [], [], []

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)


        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()
        mcdMethod_Modified = MCD_Modified.MCD_Modified()

        LSsaver = []
        MCDsaver_ = []
        Hubersaver = []
        Cauchysaver = []
        MCD_Modified_saver_ = []

        for i in range(nCycle):
            Y, xAll, dictionaryZones, sampleSizes, Z = modelForData.Main_Model(params=params)
            h = int(n / 4)

            xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
            xMatrixMCD_ = self.__filingMatrixX(xall=xVectorMCD_, n=h)
            tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
            MCDsaver_.append(tettaMCD_.copy())

            xVectorMCD_Modified, yVectorMCD_Modified = mcdMethod_Modified.Main_MCD(X=xAll,Y=Y, dictionaryZones=dictionaryZones,
                                                                                            sampleSizes=sampleSizes, Z=Z, n=n, h=h)
            xMatrixMCD_Modified = self.__filingMatrixX(xall=xVectorMCD_Modified, n=h)
            tettaMCD_Modified_ = LSObject.LSMatrix(xMatrixMCD_Modified, yVectorMCD_Modified)
            MCD_Modified_saver_.append(tettaMCD_Modified_.copy())

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
        iMCD_Modified.append(extraObj.MainCount(MCD_Modified_saver_, tetta, nCycle)[0])
        iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
        iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])


        zones = params["emissionZones"]
        message = f"{mode}_n = {n}_nCycle = {nCycle}_outlier = {outlier}_params = {zones[0]}_{zones[1]}_{zones[2]}_{zones[3]}"

        self.__CreateFileForIndexes(
            name=f"{mode}_n_{n}_nCycle_{nCycle}_outlier_{outlier}_params_{zones[0]}_{zones[1]}_{zones[2]}_{zones[3]}",
            path=f"dataForIndex/{mode}/",
            LS=iLS, MCD=iMCD, MCD_Modified=iMCD_Modified, Huber=iHuber, Cauchy=iCauchy, message=message)


    # Отрисовка графиков для MCD, МНК, м-оценок с фиксированной долей выбросов,
    # Нужен для демонстрации приближения графика MCD к графикам МНК и м-оценок
    def __FunctionForGraficWithN(self, params, mode):
        n = params["n"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        nCycle = params["nCycle"]

        nSaver = []
        iLS, iMCD, iCauchy, iHuber = [], [], [], []

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()

        while n <= 1000:
            LSsaver = []
            MCDsaver_ = []
            Hubersaver = []
            Cauchysaver = []

            params["n"] = n
            for i in range(nCycle):
                Y, xAll = modelForData.Main_Model(params=params)
                h = int(n * 0.75)

                hValues_1, hValues_2, yForH = [], [], []
                for z in range(h):
                    hValues_1.append(xAll[0][z])
                    hValues_2.append(xAll[1][z])
                    yForH.append(Y[z])
                yForH = np.array(yForH).reshape(h, 1)
                xForH = np.stack((hValues_1, hValues_2))

                xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
                xMatrixMCD_ = self.__filingMatrixX(xall=xVectorMCD_, n=h)
                tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
                MCDsaver_.append(tettaMCD_.copy())



                X = self.__filingMatrixX(xForH, h)
                tettaLS = LSObject.LSMatrix(X, yForH)
                LSsaver.append(tettaLS.copy())

                tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, yForH, h)
                Hubersaver.append(tettaMEstHuber.copy())

                tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, yForH, h)
                Cauchysaver.append(tettaMEstCauchy.copy())
                print(f"nCycle: {i}")
            print(f" n == {n}\n")

            extraObj = ex.ExtraThings()
            iLS.append(extraObj.MainCount(LSsaver, tetta, nCycle)[0])
            iMCD.append(extraObj.MainCount(MCDsaver_, tetta, nCycle)[0])
            iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
            iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])

            nSaver.append(n)
            n += 50

        self.__CreateGrafic(fileName=f"SFFM_GraficForN_{mode}_n_{n}_nCycle_{nCycle}_points_{len(nSaver)}",
                            path=f"grafics/{mode}/", outSaverX=nSaver,
                            paramMethodsY={"iLS": iLS, "iMCD": iMCD, "iHuber": iHuber, "iCauchy": iCauchy},
                            about=["LS", "MCD", "Huber", "Cauchy"], xlabel="Объём выборки", ylabel="Показатель точности")

    def Main_StandForHGOutliers(self, params, mode, modeForGrafic):
        if modeForGrafic == "grafic":
            self.__FunctionForGraficWithOutliers(params, mode)
        elif modeForGrafic == "textOutput":
            self.__FunctionForTextOutput(params, mode)
        elif modeForGrafic == "grafic_for_N":
            self.__FunctionForGraficWithN(params, mode)






