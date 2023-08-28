import matplotlib.pyplot as plt
import numpy as np


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
    x1 = np.random.uniform(0., 10.0, n)
    x2 = np.random.uniform(0., 10.0, n)

    y = calculateYwithoutError(tetta, x1, x2, n)
    xall = []

    # Search observation error
    e = np.random.binomial(n=1., p=(1 - outlier), size=n)

    # Search y_res:
    varMainObservations = 0.01
    varEmissions = 5.
    y_res = np.zeros((n,))

    for i in range(n):
        if e[i] == 1:
            y_res[i] = y[i] + np.random.normal(0, np.sqrt(varMainObservations))
        else:
            y_res[i] = y[i] + np.random.normal(0, np.sqrt(varEmissions))
    for i in range(n):
        xall.append(x1[i])
    for i in range(n):
        xall.append(x2[i])
    return y_res, xall

def lineToColum(x, n, tetta):
    # Преобразование входной строки x в матрицу
    nTetta = len(tetta) - 1
    xnew = np.zeros((nTetta, n))
    counterDel = 0
    for stepi in range(nTetta):
        for stepj in range(n):
            xnew[stepi][stepj] = x[counterDel]
            counterDel += 1
    return xnew

def LMSMatrix(x, y):
    return np.dot((np.dot(np.linalg.inv(np.dot(x.transpose(), x)), x.transpose())), y)

def filingMatrixX(x, xall, tetta):
    nTetta = len(tetta)
    n = len(x[0])
    for stepi in range(n):
        x[0][stepi] = 1.
    for stepi in range(1, nTetta):
        for stepj in range(n):
            x[stepi][stepj] = xall[stepi - 1][stepj]
    # for stepi in range(nTetta):
    #     for stepj in range(n):
    #         for stepz in range(stepj, n):
    #             x[stepi][stepj] += x[stepi][stepz]
    return x.transpose()

def relativeError(tettaTrue, tettanew):
    n, counter = len(tettaTrue), 0
    for stepi in range(n):
        counter += pow((tettaTrue[stepi] - tettanew[stepi]), 2) / pow(tettaTrue[stepi], 2)
    return counter

def main():
    N, tetta, tettaNew = 200, np.array([1., 1.5, 2.]), np.array([0., 0., 0.])

    Outlier = 0.
    while Outlier < 0.25:
        yTrue, xAll = ylinealModel(n=N, tetta=tetta, outlier=Outlier)
        X = np.zeros((len(tetta), N))
        X = filingMatrixX(X, lineToColum(xAll, N, tetta), tetta)
        tettaNew = LMSMatrix(X, yTrue.reshape(N, 1))
        print("\nOutlier = ", Outlier*100,"%", "\ntetta:\n", tettaNew)
        print("\nОтносительная ошибка:\n", relativeError(tettaTrue=tetta, tettanew=tettaNew))
        Outlier += 0.05

if __name__ == '__main__':
    main()

