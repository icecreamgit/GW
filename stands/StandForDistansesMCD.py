import mcd_method.MCD_Three_variables as MCD_Three_variables
import LS
import M_Estimators as MEst
import matplotlib.pyplot as plt

###summary###
###Представленнфый класс необходим для получения графиков ###
### зависимости относительных расстояний от Х1 и Х2 ###
class StandForDistansesMCD:
    def __CreateGrafics(self, fileName, path, x, y, about, xlabel, ylabel):
        # xVectorMCD
        plt.plot()
        plt.xlabel(xlabel)  # ось абсцисс
        plt.ylabel(ylabel)  # ось ординат
        plt.grid()  # включение отображение сетки
        plt.scatter(x, y)  # построение графика
        plt.legend(about)
        plt.savefig(path + fileName)
        plt.show()


    def Main_StandForDistansesMCD(self, params):
        n = params["n"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        limit = params["limit"]
        varMainObservations = params["varMainObservations"]
        varEmissions = params["varEmissions"]


        outSaver, nSaver = [], []
        iLS, iMCD, iCauchy, iHuber = [], [], [], []

        LSObject = LS.LS()
        MObject = MEst.M_Estimators()
        mcdMethod_three_var = MCD_Three_variables.MCD()


        Y, xAll = LSObject.ylinealModel(n, tetta, outlier, limit, varMainObservations, varEmissions)
        h = int(n * (1 - outlier))

        xVectorMCD_, di = mcdMethod_three_var.FindRelativeDistances(X=xAll, Y=Y, n=n, h=h)
        self.__CreateGrafics(fileName="SFD__diForx1", path="grafics/", x=xVectorMCD_[0], y=di,
                             about=f"Отношение di к x1 выбросы:{outlier}", xlabel="x1", ylabel="di")

        self.__CreateGrafics(fileName="SFD__diForx2", path="grafics/", x=xVectorMCD_[1], y=di,
                             about=f"Отношение di к x2 выбросы: {outlier}", xlabel="x2", ylabel="di")

