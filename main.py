import numpy as np
import stands.StandForFourMethods as StandForFourMethods
import stands.StandForDistansesMCD as StandForDistansesMCD

def main():
    n, tetta, p = 500, np.array([1., 1.5, 2.]), 3
    limit = 1.0
    outlier = 0.05
    nCycle = 1

    # Only: "normalModel" "cauchyModel" "exponentModel"

    # For I model (only normal)
    # emissionZones = [0.1, 0.5, 1., 5]
    # mode = "normalModel"

    # For II model (normal + cauchy)
    # emissionZones = [0.1, 0.5, 0.5, 1.]
    # mode = "cauchyModel"

    # For III model (normal + exp)
    emissionZones = [0., 0.1, 0.5, 1.]
    mode = "exponentModel"


    standForFourMethods = StandForFourMethods.StandForFourMethods()
    standForDistansesMCD = StandForDistansesMCD.StandForDistansesMCD()

    params = {"n": n, "tetta": tetta, "outlier": outlier, "limit": limit,
              "emissionZones": emissionZones, "nCycle": nCycle}

    standForFourMethods.Main_StandForFourMethods(params, mode)
    # standForDistansesMCD.Main_StandForDistansesMCD(params)



if __name__ == '__main__':
    main()
