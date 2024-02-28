import numpy as np
import stands.StandForFourMethods as StandForFourMethods
import stands.StandForDistansesMCD as StandForDistansesMCD

def main():
    n, tetta, p = 500, np.array([1., 1.5, 2.]), 3
    limit = 1.0
    outlier = 0.05
    varMainObservations = 0.1
    varEmissions = 1.5
    nCycle = 1

    standForFourMethods = StandForFourMethods.StandForFourMethods()
    standForDistansesMCD = StandForDistansesMCD.StandForDistansesMCD()

    params = {"n": n, "tetta": tetta, "outlier": outlier, "limit": limit,
              "varMainObservations": varMainObservations, "varEmissions": varEmissions, "nCycle": nCycle}

    standForFourMethods.Main_StandForFourMethods(params)
    # standForDistansesMCD.Main_StandForDistansesMCD(params)



if __name__ == '__main__':
    main()
