import numpy as np
import methods.MCD_Three_variables as MCD_Three_variables
import methods.MCD_Modified as MCD_Modified
import methods.MCD_Mod_ForN as MCD_ModForN

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

    def __CompareMCDsGrafics(self, fileName, path, outSaverX, paramMethodsY, about, xlabel, ylabel):
        iFirst = paramMethodsY["iFirst"]
        iSecond = paramMethodsY["iSecond"]

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось ординат
        plt.grid()  # включение отображение сетки

        plt.plot(
            outSaverX, iFirst,
            outSaverX, iSecond,
        )  # построение графика
        plt.legend((
            about[0],
            about[1],
        ))
        plt.savefig(path + fileName)
        plt.show()
    def __CreateThreeDistrGrafic(self, fileName, path, outSaverX, paramMethodsY, about, xlabel, ylabel):

        iFirst = paramMethodsY["iFirst"]
        iSecond = paramMethodsY["iSecond"]
        iThird = paramMethodsY["iThird"]

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось ординат
        plt.grid()  # включение отображение сетки

        plt.plot(
            outSaverX, iFirst,
            outSaverX, iSecond,
            outSaverX, iThird,
        )  # построение графика
        plt.legend((
            about[0],
            about[1],
            about[2],
        ))
        plt.savefig(path + fileName)
        plt.show()

    def __CreateGrafic(self, fileName, path, outSaverX, paramMethodsY, about, xlabel, ylabel):

        iLS = paramMethodsY["iLS"]
        iMCD = paramMethodsY["iMCD"]
        iMCD_Mod = paramMethodsY["iMCD_Mod"]
        iHuber = paramMethodsY["iHuber"]
        iCauchy = paramMethodsY["iCauchy"]

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось ординат
        plt.grid()  # включение отображение сетки

        plt.plot(
            outSaverX, iLS,
            outSaverX, iMCD,
            outSaverX, iMCD_Mod,
            outSaverX, iHuber,
            outSaverX, iCauchy
        )  # построение графика
        plt.legend((
            about[0],
            about[1],
            about[2],
            about[3],
            about[4]
        ))
        plt.savefig(path + fileName)
        plt.show()
    def __CreateFileForIndexes(self, name, path, LS, MCD, MCD_Modified, Huber, Cauchy, message):
        with open(f"{path}{name}.txt", "w") as file:
            file.write(message)
            file.write(f"\nLS: {LS}\nMCD: {MCD}\nMCD_Modified: {MCD_Modified}\nHuber: {Huber}\nCauchy: {Cauchy}\n\n"
                       f"{round(LS[0], 5)}\t{round(MCD[0], 5)}\t{round(MCD_Modified[0], 5)}\t"
                       f"{round(Huber[0], 5)}\t{round(Cauchy[0], 5)}")

    # Стандартная метод для расчёта показателя точности с выбросами
    # Плюс, отрисовывается график для методов MCD, МНК, М-оценок
    def __FunctionForGraficWithOutliers(self, params, mode):
        n = params["n"]
        itteratorOitlier = params["itteratorOutlier"]
        numberZones = params["numberZones"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        nCycle = params["nCycle"]

        outSaver, nSaver = [], []
        iLS, iMCD, iMCD_Mod, iCauchy, iHuber = [], [], [], [], []

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()
        mcd_For_N = MCD_ModForN.MCD_Modified()


        while outlier <= 0.25:
            LSsaver = []
            MCDsaver_ = []
            Hubersaver = []
            Cauchysaver = []
            MCD_Mod_saver_ = []

            params["outlier"] = outlier
            for i in range(nCycle):
                Y, xAll, dictionaryZones, sampleSizes, Z = modelForData.Main_Model(params=params)
                h = int(n * (1 - outlier))

                xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
                xMatrixMCD_ = self.__filingMatrixX(xall=xVectorMCD_, n=h)
                tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
                MCDsaver_.append(tettaMCD_.copy())

                xVectorMCD_Modified, yVectorMCD_Modified = mcd_For_N.Main_MCD(X=xAll, Y=Y,
                                                                              outlier=outlier,
                                                                              dictionaryZones=dictionaryZones,
                                                                              sampleSizes=sampleSizes, Z=Z,
                                                                              n=n, h=h,
                                                                              numberZones=numberZones)
                xMatrixMCD_Modified = self.__filingMatrixX(xall=xVectorMCD_Modified, n=h)
                tettaMCD_Modified_ = LSObject.LSMatrix(xMatrixMCD_Modified, yVectorMCD_Modified)
                MCD_Mod_saver_.append(tettaMCD_Modified_.copy())

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
            iMCD_Mod.append(extraObj.MainCount(MCD_Mod_saver_, tetta, nCycle)[0])
            iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
            iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])

            print(f" Outlier == {outlier}\n")
            outSaver.append(outlier)
            outlier += itteratorOitlier

        self.__CreateGrafic(
            fileName=f"С_выбросами_все_графики{mode}_n_{n}_nCycle_{nCycle}_points_{len(outSaver)}",
            path=f"grafics/{mode}/", outSaverX=outSaver,
            paramMethodsY={"iLS": iLS, "iMCD": iMCD, "iMCD_Mod": iMCD_Mod, "iHuber": iHuber, "iCauchy": iCauchy},
            about=["МНК", "MCD", "MCD модификация", "М-оценки Хьюбера", "М-оценки Коши"], xlabel="Выбросы", ylabel="Показатель точности")

        self.__CreateThreeDistrGrafic(
            fileName=f"С_выбросами_три_графика{mode}_n_{n}_nCycle_{nCycle}_points_{len(outSaver)}_МНК_MCD_Хьюбер",
            path=f"grafics/{mode}/", outSaverX=outSaver,
            paramMethodsY={"iFirst": iCauchy, "iSecond": iMCD, "iThird": iHuber},
            about=["М-оценки Коши", "MCD", "М-оценки Хьюбера"], xlabel="Выбросы",
            ylabel="Показатель точности")

        self.__CreateThreeDistrGrafic(
            fileName=f"С_выбросами_три_графика{mode}_n_{n}_nCycle_{nCycle}_points_{len(outSaver)}_МНК_MCD_Mod_Коши",
            path=f"grafics/{mode}/", outSaverX=outSaver,
            paramMethodsY={"iFirst": iCauchy, "iSecond": iMCD_Mod, "iThird": iHuber},
            about=["М-оценки Коши", "MCD модификация", "М-оценки Хьюбера"], xlabel="Выбросы",
            ylabel="Показатель точности")
        self.__CompareMCDsGrafics(
            fileName=f"С_выбросами_MCD_MCD_Mod_графика{mode}_n_{n}_nCycle_{nCycle}_points_{len(outSaver)}",
            path=f"grafics/{mode}/", outSaverX=outSaver,
            paramMethodsY={"iFirst": iMCD, "iSecond": iMCD_Mod},
            about=["MCD", "MCD модификация"], xlabel="Выбросы",
            ylabel="Показатель точности")


    # Стандартная метод для расчёта показателя точности с выбросами
    # График не отрисовывается, но в файл записываются значения показателя точности
    # Эта функция делает то же, что и __FunctionForGraficWithOutliers, просто графики не рисует
    def __FunctionForTextOutput(self, params, mode):
        n = params["n"]
        tetta = params["tetta"]
        h = params["hi"]
        nCycle = params["nCycle"]
        numberZones = params["numberZones"]


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
            Y, xAll, xAll_h, y_res_h, dictionaryZones, sampleSizes, Z = modelForData.Main_Model(params=params)


            xVectorMCD_, yVectorMCD_ = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
            xMatrixMCD_ = self.__filingMatrixX(xall=xVectorMCD_, n=h)
            tettaMCD_ = LSObject.LSMatrix(xMatrixMCD_, yVectorMCD_)
            MCDsaver_.append(tettaMCD_.copy())

            xVectorMCD_Modified, yVectorMCD_Modified = mcdMethod_Modified.Main_MCD(X=xAll,Y=Y, dictionaryZones=dictionaryZones,
                                                                                   sampleSizes=sampleSizes, Z=Z, n=n, h=h,
                                                                                   numberZones=numberZones)
            xMatrixMCD_Modified = self.__filingMatrixX(xall=xVectorMCD_Modified, n=h)
            tettaMCD_Modified_ = LSObject.LSMatrix(xMatrixMCD_Modified, yVectorMCD_Modified)
            MCD_Modified_saver_.append(tettaMCD_Modified_.copy())

            X = self.__filingMatrixX(xAll_h, h)
            tettaLS = LSObject.LSMatrix(X, y_res_h)
            LSsaver.append(tettaLS.copy())

            tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, y_res_h, h)
            Hubersaver.append(tettaMEstHuber.copy())

            tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, y_res_h, h)
            Cauchysaver.append(tettaMEstCauchy.copy())
            print(f" i == {i}\n")

        extraObj = ex.ExtraThings()
        iLS.append(extraObj.MainCount(LSsaver, tetta, nCycle)[0])
        iMCD.append(extraObj.MainCount(MCDsaver_, tetta, nCycle)[0])
        iMCD_Modified.append(extraObj.MainCount(MCD_Modified_saver_, tetta, nCycle)[0])
        iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
        iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])


        zones = params["emissionZones"]
        message = f"{mode}_n = {n}_nCycle = {nCycle}_h = {h}_params = {zones[0]}_{zones[1]}_{zones[2]}_{zones[3]}"

        self.__CreateFileForIndexes(
            name=f"{mode}_n_{n}_nCycle_{nCycle}_h_{h}_params_{zones[0]}_{zones[1]}_{zones[2]}_{zones[3]}",
            path=f"dataForIndex/{mode}/",
            LS=iLS, MCD=iMCD, MCD_Modified=iMCD_Modified, Huber=iHuber, Cauchy=iCauchy, message=message)


    # Отрисовка графиков для MCD, МНК, м-оценок с фиксированной долей выбросов,
    # Нужен для демонстрации приближения графика MCD к графикам МНК и м-оценок
    def __FunctionForGraficWithN(self, params, mode):
        n = params["n"]
        iteratorN = params["iteratorN"]
        limitN = params["limitN"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        nCycle = params["nCycle"]
        numberZones = params["numberZones"]
        coefficient = 0.95

        nSaver = []
        iLS, iMCD, iMCD_Mod, iCauchy, iHuber = [], [], [], [], []

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()
        mcd_For_N = MCD_ModForN.MCD_Modified()

        while n <= limitN:
            LSsaver = []
            MCDsaver_ = []
            Hubersaver = []
            Cauchysaver = []
            MCD_Mod_saver_ = []

            params["n"] = n
            for i in range(nCycle):
                Y, xAll, dictionaryZones, sampleSizes, Z = modelForData.Main_Model(params=params)
                h = int(n * coefficient)

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

                xVectorMCD_Modified, yVectorMCD_Modified = mcd_For_N.Main_MCD(X=xAll, Y=Y,
                                                                                outlier=outlier,
                                                                                dictionaryZones=dictionaryZones,
                                                                                sampleSizes=sampleSizes, Z=Z,
                                                                                n=n, h=h,
                                                                                numberZones=numberZones)
                xMatrixMCD_Modified = self.__filingMatrixX(xall=xVectorMCD_Modified, n=h)
                tettaMCD_Modified_ = LSObject.LSMatrix(xMatrixMCD_Modified, yVectorMCD_Modified)
                MCD_Mod_saver_.append(tettaMCD_Modified_.copy())


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
            iMCD_Mod.append(extraObj.MainCount(MCD_Mod_saver_, tetta, nCycle)[0])
            iHuber.append(extraObj.MainCount(Hubersaver, tetta, nCycle)[0])
            iCauchy.append(extraObj.MainCount(Cauchysaver, tetta, nCycle)[0])

            nSaver.append(n)
            n += iteratorN

        self.__CreateGrafic(fileName=f"SFFM_GraficForN_{mode}_n_{n}_nCycle_{nCycle}_points_{len(nSaver)}_",
                            path=f"grafics/{mode}/", outSaverX=nSaver,
                            paramMethodsY={"iLS": iLS, "iMCD": iMCD, "iMCD_Mod":iMCD_Mod, "iHuber": iHuber, "iCauchy": iCauchy},
                            about=["МНК", "MCD", "MCD модификация", "М-оценки Хьюбера", "М-оценки Коши"],
                            xlabel="Объём выборки", ylabel="Показатель точности")

        self.__CreateThreeDistrGrafic(fileName=f"SFFM_GraficForN_{mode}_n_{n}_nCycle_{nCycle}_points_{len(nSaver)}_МНК_Хьюбер_Коши_",
                            path=f"grafics/{mode}/", outSaverX=nSaver,
                            paramMethodsY={"iFirst": iLS, "iSecond": iHuber,
                                           "iThird": iCauchy},
                            about=["МНК", "М-оценки Хьюбера", "М-оценки Коши"], xlabel="Объём выборки",
                            ylabel="Показатель точности")
        self.__CompareMCDsGrafics(
            fileName=f"SFFM_GraficForN_{mode}_n_{n}_nCycle_{nCycle}_points_{len(nSaver)}_MCD_MCD_Mod_",
            path=f"grafics/{mode}/", outSaverX=nSaver,
            paramMethodsY={"iFirst": iMCD, "iSecond":iMCD_Mod},
            about=["MCD", "MCD модификация"], xlabel="Объём выборки",
            ylabel="Показатель точности")

    def Main_StandForHGOutliers(self, params, mode, modeForGrafic):
        if modeForGrafic == "grafic":
            self.__FunctionForGraficWithOutliers(params, mode)
        elif modeForGrafic == "textOutput":
            self.__FunctionForTextOutput(params, mode)
        elif modeForGrafic == "grafic_for_N":
            self.__FunctionForGraficWithN(params, mode)






