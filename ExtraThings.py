import numpy as np

class ExtraThings:

    def __MiddleTetta(self, Ksi):
        result = 0.
        N = len(Ksi)
        for i in range(N):
            result += Ksi[i]
        result /= N
        return result

    def __CountMark(self, tettaTrue, tettaNew, n):
        result = []

        for element in tettaNew:
            saver = 0.
            for i in range(n):
                saver += (pow(tettaTrue[i] - element[i], 2) / pow(tettaTrue[i], 2))
            result.append(saver)
        return result

    def MainCount(self, tettaCount, tettaTrue, N):
        n = len(tettaTrue)
        Ksi = self.__CountMark(tettaTrue, tettaCount, n)
        KsiEnd = self.__MiddleTetta(Ksi)

        return KsiEnd


