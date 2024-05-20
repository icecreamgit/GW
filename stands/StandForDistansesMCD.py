import mcd_method.MCDForStandDistances as MCD_
import mcd_method.MCD_ModForStandDistances as MCD_Modified
import math
import LS
import M_Estimators as MEst
import models.FactoryForModels as FactoryForModels
import matplotlib.pyplot as plt

###summary###
###Представленнфый класс необходим для получения графиков ###
### зависимости относительных расстояний от Х1 и Х2 ###
class StandForDistansesMCD:


    def __FindDublicates(self, xAll, xVector):
        colors = []
        count = 0
        for elementXAll in xAll:
            for elementVector in xVector:
                if math.isclose(elementVector, elementXAll, rel_tol=1e-8):
                    colors.append('green')
                    count = 1
                    break
            if count == 0:
                colors.append('red')
            count = 0

        return colors

    def __CreateGraficsForMCD_Di(self, fileName, path, xAll, x, di, xlabel, ylabel, lims):

        colors = self.__FindDublicates(xAll, x)

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось
        plt.xlim()
        plt.ylim(lims[0], lims[1])
        plt.grid()  # включение отображение сетки
        plt.scatter(xAll, di, color=colors, linewidth=1.3, edgecolors='black')  # построение графика
        plt.savefig(path + fileName)
        plt.show()

    def __CreateGraficsForMCD_Y(self, fileName, path, xAll, x, y, xlabel, ylabel, lims):
        colors = self.__FindDublicates(xAll, x)

        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось
        plt.xlim()
        plt.ylim(lims[0], lims[1])
        plt.grid()  # включение отображение сетки
        plt.scatter(xAll, y, color=colors, linewidth=1.3, edgecolors='black')  # построение графика
        plt.savefig(path + fileName)
        plt.show()

    def Main_StandForDistansesMCD(self, params, mode):
        n = params["n"]
        numberZones = params["numberZones"]
        h = params["hi"]

        factoryObject = FactoryForModels.FactoryForModels()
        modelForData = factoryObject.main_Factory(mode)

        outSaver, nSaver, xVectorMCD_, di, xAll, Y = [], [], [], [], [[], []], []
        iLS, iMCD, iCauchy, iHuber = [], [], [], []

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_ = MCD_.MCDForStandDistances()
        mcdMethod_Modified = MCD_Modified.MCD_Modified()

        lims1 = [-1, 100]
        lims2 = [-6, 15]

        Y, xAll, xAll_h, y_res_h, dictionaryZones, sampleSizes, Z = modelForData.Main_Model(params=params)

        X_n, X_h, Y_n, di_n = mcdMethod_.Main_MCDForStandDistances(X=xAll, Y=Y, n=n, h=h)

        self.__CreateGraficsForMCD_Di(fileName=f"SFD__diForx1 mcd {mode}", path="grafics/",
                                   xAll=X_n[0], x=X_h[0], di=di_n,
                                   xlabel="x1", ylabel="di", lims=lims1)

        self.__CreateGraficsForMCD_Di(fileName=f"SFD__diForx2 mcd {mode}", path="grafics/",
                                   xAll=X_n[1], x=X_h[1], di=di_n,
                                   xlabel="x2", ylabel="di", lims=lims1)

        self.__CreateGraficsForMCD_Y(fileName=f"SFD__Y_Forx1 mcd {mode}", path="grafics/",
                                   xAll=X_n[0], x=X_h[0], y=Y_n,
                                   xlabel="x1", ylabel="Y", lims=lims2)

        self.__CreateGraficsForMCD_Y(fileName=f"SFD__Y_Forx2 mcd {mode}", path="grafics/",
                                   xAll=X_n[1], x=X_h[1], y=Y_n,
                                   xlabel="x2", ylabel="Y", lims=lims2)

        lims1 = [-1, 25]
        lims2 = [-6, 15]
        X_n, X_h, Y_n, di_n = mcdMethod_Modified.Main_MCD(X=xAll,Y=Y, dictionaryZones=dictionaryZones,
                                                                       sampleSizes=sampleSizes, Z=Z, n=n, h=h,
                                                                       numberZones=numberZones)

        self.__CreateGraficsForMCD_Di(fileName=f"SFD__diForx1 mcd_modified {mode}", path="grafics/",
                                      xAll=X_n[0], x=X_h[0], di=di_n,
                                      xlabel="x1", ylabel="di", lims=lims1)

        self.__CreateGraficsForMCD_Di(fileName=f"SFD__diForx2 mcd_modified {mode}", path="grafics/",
                                      xAll=X_n[1], x=X_h[1], di=di_n,
                                      xlabel="x2", ylabel="di", lims=lims1)

        self.__CreateGraficsForMCD_Y(fileName=f"SFD__Y_Forx1 mcd_modified {mode}", path="grafics/",
                                     xAll=X_n[0], x=X_h[0], y=Y_n,
                                     xlabel="x1", ylabel="Y", lims=lims2)

        self.__CreateGraficsForMCD_Y(fileName=f"SFD__Y_Forx2 mcd_modified {mode}", path="grafics/",
                                     xAll=X_n[1], x=X_h[1], y=Y_n,
                                     xlabel="x2", ylabel="Y", lims=lims2)
