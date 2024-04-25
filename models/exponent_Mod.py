import numpy as np
from itertools import chain

class exponentModel:
    def __calculateYwithoutError(self, t, x1, x2, size):
        y_ = np.zeros((size,))
        for i in range(size):
            y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]

        return y_
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

    def __calculateXYForZone(self, x1Zones, x2Zones, tetta, h):
        x1 = np.random.uniform(x1Zones["start"], x1Zones["finish"], h)
        x2 = np.random.uniform(x2Zones["start"], x2Zones["finish"], h)
        y = self.__calculateYwithoutError(tetta, x1, x2, h)
        return x1, x2, y

    ######
    ###### Остановился пока что здесь, пытаюсь разобраться, как коши функцию накатить...

    def Main_Model(self, params):
        # Search y without observation error
        # n, tetta, outlier, limit, emissionZones
        y_res = []
        xall = [[], []]
        n = params["n"]
        numberZones = params["numberZones"]
        tetta = params["tetta"]

        start = 0.
        middleValue = 0.5
        limit = params["limit"]

        emissionZones = params["emissionZones"]

        # Search y without observation error
        sampleSizes = self.__calibrateInputLenght(n, numberZones)
        x1Zones = {"start": start, "finish": middleValue}
        x2Zones = {"start": middleValue, "finish": limit}
        x1_I, x2_I, y_I = self.__calculateXYForZone(x1Zones, x2Zones, tetta, sampleSizes[0])

        x1Zones = {"start": start, "finish": middleValue}
        x2Zones = {"start": start, "finish": middleValue}
        x1_II, x2_II, y_II = self.__calculateXYForZone(x1Zones, x2Zones, tetta, sampleSizes[1])

        x1Zones = {"start": middleValue, "finish": limit}
        x2Zones = {"start": middleValue, "finish": limit}
        x1_III, x2_III, y_III = self.__calculateXYForZone(x1Zones, x2Zones, tetta, sampleSizes[2])

        x1Zones = {"start": middleValue, "finish": limit}
        x2Zones = {"start": start, "finish": middleValue}
        x1_IV, x2_IV, y_IV = self.__calculateXYForZone(x1Zones, x2Zones, tetta, sampleSizes[3])

        x1 = list(chain(x1_IV, x1_II, x1_I, x1_III))
        x2 = list(chain(x2_IV, x2_II, x2_I, x2_III))
        y = list(chain(y_IV, y_II, y_I, y_III))

        listFirstZone = []
        listSecondZone = []
        listThirdZone = []
        listForthZone = []

        for i in range(n):
            if x1[i] < middleValue and x2[i] > middleValue:
                # I zone
                y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[0])))
                listFirstZone.append(i)

            elif x1[i] <= middleValue and x2[i] <= middleValue:
                # II zone
                y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[1])))
                listSecondZone.append(i)

            elif x1[i] > middleValue and x2[i] > middleValue:
                # III zone
                y_res.append(y[i] + np.random.exponential(scale=np.sqrt(emissionZones[2])))
                listThirdZone.append(i)

            elif x1[i] > middleValue and x2[i] < middleValue:
                # IV zone
                y_res.append(y[i] + np.random.exponential(scale=np.sqrt(emissionZones[3])))
                listForthZone.append(i)

        for i in range(n):
            xall[0].append(x1[i])
            xall[1].append(x2[i])
        dictionaryZones = {"1": listFirstZone, "2": listSecondZone, "3": listThirdZone, "4": listForthZone}
        y_res = np.array(y_res).reshape(n, 1)

        return y_res, xall, dictionaryZones, sampleSizes
