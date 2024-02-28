import numpy as np

class cauchyModel:
    def __calculateYwithoutError(self, t, x1, x2, size):
        y_ = np.zeros((size,))
        for i in range(size):
            y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]

        return y_


    ######
    ###### Остановился пока что здесь, пытаюсь разобраться, как коши функцию накатить...

    def main_CauchyModel(self, n, tetta, outlier, limit, varMainObservations, varEmissions):
        # Search y without observation error
        x1 = np.random.uniform(0., limit, n)
        x2 = np.random.uniform(0., limit, n)

        y = self.__calculateYwithoutError(tetta, x1, x2, n)
        xall = [[], []]

        # Search observation error
        e = np.random.binomial(n=1, p=(1.0 - outlier), size=n)
        y_res = []

        for i in range(n):
            if e[i] == 1:
                y_res.append(y[i] + np.random.standard_cauchy(loc=0, scale=np.sqrt(varMainObservations)))
            else:
                y_res.append(y[i] + np.random.standard_cauchy(loc=0, scale=np.sqrt(varEmissions)))
        for i in range(n):
            xall[0].append(x1[i])
            xall[1].append(x2[i])
        y_res = np.array(y_res).reshape(n, 1)

        return y_res, xall
