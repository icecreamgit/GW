import numpy as np

class NormalModel:
    def __calculateYwithoutError(self, t, x1, x2, size):
        y_ = np.zeros((size,))
        for i in range(size):
            y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]

        return y_
    def Main_Model(self, params):
        # n, tetta, outlier, limit, emissionZones
        n = params["n"]
        tetta = params["tetta"]
        outlier = params["outlier"]
        limit = params["limit"]
        emissionZones = params["emissionZones"]

        # Search y without observation error
        x1 = np.random.uniform(0., limit, n)
        x2 = np.random.uniform(0., limit, n)

        y = self.__calculateYwithoutError(tetta, x1, x2, n)
        xall = [[], []]

        # Search observation error
        y_res = []

        e = np.random.binomial(n=1, p=(1.0 - outlier), size=n)

        listZeroZone = []
        listFirstZone = []
        listSecondZone = []
        listThirdZone = []
        listForthZone = []
        Z = []

        for i in range(n):
            x1_ = x1[i]
            x2_ = x2[i]
            if e[i] == 0:
                if x1_ < 0.5 and x2_ > 0.5:
                    # I zone
                    y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[0])))
                    Z.append([x1_, x2_, y_res[i], 1])
                    listFirstZone.append(i)
                elif x1_ <= 0.5 and x2_ <= 0.5:
                    # II zone
                    y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[1])))
                    Z.append([x1_, x2_, y_res[i], 2])
                    listSecondZone.append(i)
                elif x1_ > 0.5 and x2_ > 0.5:
                    # III zone
                    y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[2])))
                    Z.append([x1_, x2_, y_res[i], 3])
                    listThirdZone.append(i)
                elif x1_ > 0.5 and x2_ < 0.5:
                    # IV zone
                    y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(emissionZones[3])))
                    Z.append([x1_, x2_, y_res[i], 4])
                    listForthZone.append(i)
            else:
                y_res.append(y[i] + np.random.normal(loc=0, scale=np.sqrt(0.01)))
                Z.append([x1_, x2_, y_res[i], 0])
                listZeroZone.append(i)

        dictionaryZones = {"0": listZeroZone, "1": listFirstZone, "2": listSecondZone, "3": listThirdZone, "4": listForthZone}
        sampleSizesN = [len(listZeroZone), len(listFirstZone), len(listSecondZone), len(listThirdZone), len(listForthZone)]

        for i in range(n):
            xall[0].append(x1[i])
            xall[1].append(x2[i])
        y_res = np.array(y_res).reshape(n, 1)

        return y_res, xall, dictionaryZones, sampleSizesN, Z
