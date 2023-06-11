import random
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, Bounds, LinearConstraint, NonlinearConstraint

def calculateYwithoutError(t, x1, x2, size):
    y_ = np.zeros((size, ))
    for i in range(size):
        y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]
    return y_

def Painting(x, y):
    fig, axes = plt.subplots()
    axes.scatter(x, y, c='green')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.show()

def ylinealModel(n, tetta, outlier):
    # Search y without observation error
    x1 = np.random.uniform(0, 10.0, n)
    x2 = np.random.uniform(0, 10.0, n)
    y = calculateYwithoutError(tetta, x1, x2, n)

    # Search observation error
    e = np.random.binomial(n=1, p=(1 - outlier), size=n)

    # Search y_res:
    varMainObservations = 0.01
    varEmissions = 0.5
    y_res = np.zeros((n,))

    for i in range(n):
        if e[i] == 1:
            y_res[i] = y[i] + np.random.normal(0, np.sqrt(varMainObservations))
        else:
            y_res[i] = y[i] + np.random.normal(0, np.sqrt(varEmissions))
    return y_res

def lineToColum(x, n):
    # Преобразование входной строки x в матрицу
    count = int(len(x) / n)
    saverDraft, xnew = [], []
    for stepi in range(count):
        for stepj in range(n):
            saverDraft.append(x[stepj])
        xnew.append(saverDraft)
        saverDraft = []
    xnew = np.array(xnew).reshape(count, n)
    return xnew

def LSM(x, params):
    y = params['y'].copy()
    t = params['tetta'].copy()
    n = params['n']
    e = 0

    xNew = lineToColum(x, n)
    print("\nHere...\n")

    # Расчёт значения ошибки
    for i in range(n):
        e += pow(y[i] - (t[0] + t[1] * xNew[0][i] + t[2] * xNew[1][i]), 2)
    return e

def Minimize(tetta, y, n, count): # count - число иксов
    xAll = np.zeros((n * count))
    print("\nminimise...\n")
    res = minimize(fun=LSM, x0=xAll,args={"y": y, "tetta": tetta, "n": n}, method='TNC')
    res = lineToColum(np.array(res.__getitem__('x')), n)
    return res

def main():
    N, tetta = 200, np.array([1., 1.5, 2.])
    Outlier = 0.
    yTrue = ylinealModel(n=N, tetta=tetta, outlier=Outlier)

    print("\nres:\n", Minimize(tetta, yTrue, N, (len(tetta) - 1)))









if __name__ == '__main__':
    main()

