import numpy as np
from itertools import chain
from random import shuffle

class exponentModel:
    def __calculateYwithoutError(self, t, x1, x2):
        return t[0] + t[1] * x1 + t[2] * x2

    def __calibrateInputLenght(self, n, numberZones):
        h = int(n / numberZones)
        sampleSizes = [h, h, h, h]
        i = 0
        while sum(sampleSizes) < n :
            sampleSizes[i] += 1
            i += 1
            if i >= 4:
                i = 0
        return sampleSizes

    def __calculateXForZone(self, x1Zones, x2Zones, tetta, h):
        x1 = np.random.uniform(x1Zones["start"], x1Zones["finish"], h)
        x2 = np.random.uniform(x2Zones["start"], x2Zones["finish"], h)
        return x1, x2
    def __bindX1X2(self, x1, x2, size):
        xMix = []
        for i in range(size):
            xMix.append([x1[i], x2[i]])
        return xMix

    def __HGenerate(self, listOfIndexes, m):
        H = np.random.choice(listOfIndexes, size=m, replace=False)
        return H

    def __configurateXY(self, Z, H):
        xall = [[], []]
        y_res = []
        for i in H:
            x1 = Z[i][0]
            x2 = Z[i][1]
            y = Z[i][2]
            xall[0].append(x1)
            xall[1].append(x2)
            y_res.append(y)
        y_res = np.array(y_res).reshape(len(H), 1)
        return  xall, y_res

    def Main_Model(self, params):
        # n, tetta, outlier, limit, emissionZones
        n = params["n"]
        h = params["hi"]
        tetta = params["tetta"]
        start = 0.
        middleValue = 0.5
        limit = params["limit"]
        numberZones = params["numberZones"]
        emissionZones = params["emissionZones"]


        # Search y without observation error
        sampleSizes = self.__calibrateInputLenght(n, numberZones)
        x1Zones = {"start": start, "finish": middleValue}
        x2Zones = {"start": middleValue, "finish": limit}

        x1_I, x2_I = self.__calculateXForZone(x1Zones, x2Zones, tetta, sampleSizes[0])

        x1Zones = {"start": start, "finish": middleValue}
        x2Zones = {"start": start, "finish": middleValue}

        x1_II, x2_II = self.__calculateXForZone(x1Zones, x2Zones, tetta, sampleSizes[1])

        x1Zones = {"start": middleValue, "finish": limit}
        x2Zones = {"start": middleValue, "finish": limit}
        x1_III, x2_III = self.__calculateXForZone(x1Zones, x2Zones, tetta, sampleSizes[2])

        x1Zones = {"start": middleValue, "finish": limit}
        x2Zones = {"start": start, "finish": middleValue}
        x1_IV, x2_IV = self.__calculateXForZone(x1Zones, x2Zones, tetta, sampleSizes[3])

        x1 = list(chain(x1_I, x1_II, x1_III, x1_IV))
        x2 = list(chain(x2_I, x2_II, x2_III, x2_IV))
        xMix = self.__bindX1X2(x1, x2, n)
        shuffle(xMix)


        # Search observation error
        xall = [[], []]
        y_res = []

        listFirstZone = []
        listSecondZone = []
        listThirdZone = []
        listForthZone = []
        Z = []

        for i in range(n):
            x1 = xMix[i][0]
            x2 = xMix[i][1]
            if x1 < 0.5 and x2 > 0.5:
                # I zone
                y_res.append(self.__calculateYwithoutError(tetta, x1, x2) +
                             np.random.normal(loc=0, scale=np.sqrt(emissionZones[0])))
                Z.append([x1, x2, y_res[i], 1])
                listFirstZone.append(i)
            elif x1 <= 0.5 and x2 <= 0.5:
                # II zone
                y_res.append(self.__calculateYwithoutError(tetta, x1, x2) +
                             np.random.normal(loc=0, scale=np.sqrt(emissionZones[1])))
                Z.append([x1, x2, y_res[i], 2])
                listSecondZone.append(i)
            elif x1 > middleValue and x2 > middleValue:
                # III zone
                y_res.append(self.__calculateYwithoutError(tetta, x1, x2) +
                             np.random.exponential(scale=np.sqrt(emissionZones[2])))
                Z.append([x1, x2, y_res[i], 3])
                listThirdZone.append(i)

            elif x1 > middleValue and x2 < middleValue:
                # IV zone
                y_res.append(self.__calculateYwithoutError(tetta, x1, x2) +
                             np.random.exponential(scale=np.sqrt(emissionZones[3])))
                Z.append([x1, x2, y_res[i], 4])
                listForthZone.append(i)
        dictionaryZones = {"1": listFirstZone, "2": listSecondZone, "3": listThirdZone, "4": listForthZone}

        # Создание массива индексов для методов МНК и М-оценок
        if n != h:
            sampleSizesH = self.__calibrateInputLenght(h, numberZones)
        else:
            sampleSizesH = sampleSizes

        H = list(chain(self.__HGenerate(dictionaryZones["1"], sampleSizesH[0]),
                                self.__HGenerate(dictionaryZones["2"], sampleSizesH[1]),
                                self.__HGenerate(dictionaryZones["3"], sampleSizesH[2]),
                                self.__HGenerate(dictionaryZones["4"], sampleSizesH[3])))
        xall_h, y_res_h = self.__configurateXY(Z, H)

        for i in range(n):
            x1 = xMix[i][0]
            x2 = xMix[i][1]
            xall[0].append(x1)
            xall[1].append(x2)

        y_res = np.array(y_res).reshape(n, 1)

        return y_res, xall, xall_h, y_res_h, dictionaryZones, sampleSizes, Z

