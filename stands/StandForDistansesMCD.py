import mcd_method.MCD_Three_variables as MCD_Three_variables
import LS
import M_Estimators as MEst
import models.FactoryForModels as FactoryForModels
import matplotlib.pyplot as plt

###summary###
###Представленнфый класс необходим для получения графиков ###
### зависимости относительных расстояний от Х1 и Х2 ###
class StandForDistansesMCD:
    def __CreateGrafics(self, fileName, path, x, y, about, xlabel, ylabel, lims):

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось
        plt.xlim(-0.05, 1.05)
        plt.ylim(lims[0], lims[1])
        plt.grid()  # включение отображение сетки
        plt.scatter(x, y, color='black')  # построение графика
        plt.legend([about])
        plt.savefig(path + fileName)
        plt.show()


    def Main_StandForDistansesMCD(self, params, mode):
        n = params["n"]
        outlier = params["outlier"]

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        outSaver, nSaver = [], []
        iLS, iMCD, iCauchy, iHuber = [], [], [], []

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()

        Y, xAll = modelForData.Main_Model(params=params)
        h = int(n * (1 - outlier))

        xVectorMCD_, di = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
        self.__CreateGrafics(fileName=f"SFD__diForx1 {mode}", path="grafics/", x=xVectorMCD_[0], y=di,
                             about=f"Отношение di к x1 выбросы: {outlier}",
                             xlabel="x1", ylabel="di", lims=[0., 5.])

        self.__CreateGrafics(fileName=f"SFD__diForx2 {mode}", path="grafics/", x=xVectorMCD_[1], y=di,
                             about=f"Отношение di к x2 выбросы: {outlier}",
                             xlabel="x2", ylabel="di", lims=[0., 5.])

        self.__CreateGrafics(fileName=f"SFD__YForx1 {mode}", path="grafics/", x=xAll[0], y=Y,
                             about=f"Отношение Y к x1 выбросы: {outlier}",
                             xlabel="x1", ylabel="Y", lims=[-3., 8])

        self.__CreateGrafics(fileName=f"SFD__YForx2 {mode}", path="grafics/", x=xAll[1], y=Y,
                             about=f"Отношение Y к x2 выбросы: {outlier}",
                             xlabel="x2", ylabel="Y", lims=[-3., 8])