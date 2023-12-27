import numpy as np

class ExtraThings:

    def __MiddleTetta(self, tetta, N):
        result = np.zeros((len(tetta[0]), 1))
        for i in range(N):
            result += tetta[i]
        result /= N
        return result

    def __CountMark(self, tettaStart, midTetta, n):
        result = 0.
        for i in range(n):
            result += pow(tettaStart[i] - midTetta[i], 2) / pow(tettaStart[i], 2)
        return result

    def MainCount(self, tettaCount, tettaStart, N, method):
        midTetta = self.__MiddleTetta(tettaCount, N)

        n = len(tettaStart)
        endFalue = self.__CountMark(tettaStart, midTetta, n)

        return endFalue


