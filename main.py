import numpy as np
import stands.StandForFourMethods as StandForFourMethods
import stands.StandForDistansesMCD as StandForDistansesMCD

def main():
    n, tetta, p = 250, np.array([1., 1.5, 2.]), 3
    limit = 1.0
    outlier = 0.1
    nCycle = 1

    # grafic - отображение зависимости кси от выбросов
    # oneOutput - вывод в консоль значений показателей точности оценивания
    # для LS, MCD, M-estimators of Cauchy and Huber
    modeForGrafic = "oneOutput"

    # Only: "normalModel" "cauchyModel" "exponentModel"
    modes = ["normalModel", "cauchyModel", "exponentModel"]
    # For I model (only normal)
    # emissionZones = [[0., 0.01, 0., 0.25], [0., 0.25, 0., 5.]]
    # mode = "normalModel"

    # For II model (normal + cauchy)
    # emissionZones = [[0., 0.01, 0., 0.5], [0., 0.25, 0., 0.5], [0., 0.01, 0., 1.], [0., 0.25, 0., 1.]]
    # mode = "cauchyModel"

    # For III model (normal + exp)
    emissionZones = [[0., 0.1, 0., 0.5], [0., 0.25, 0., 0.5], [0., 0.01, 0., 1.], [0., 0.25, 0., 1.], [0., 0.01, 0., 2.], [0., 0.25, 0., 2.]]
    mode = "exponentModel"


    standForFourMethods = StandForFourMethods.StandForFourMethods()
    standForDistansesMCD = StandForDistansesMCD.StandForDistansesMCD()

    params = {"n": n, "tetta": tetta, "outlier": outlier, "limit": limit,
              "emissionZones": emissionZones, "nCycle": nCycle}
    for mode in modes:
        for emissionZone in emissionZones:
            params["emissionZones"] = emissionZone
            params["n"] = n
            while n <= 500:
                standForFourMethods.Main_StandForFourMethods(params, mode, modeForGrafic)
                # standForDistansesMCD.Main_StandForDistansesMCD(params)
                n += 50
                params["n"] = n
            n = 250



if __name__ == '__main__':
    main()
