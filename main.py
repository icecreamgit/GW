import numpy as np
import random
import MCD
def calculateYwithoutError(t, x1, x2, size):
    y_ = np.zeros((size, ))
    for i in range(size):
        y_[i] = t[0] + t[1] * x1[i] + t[2] * x2[i]
    return y_

def ylinealModel(n, tetta, outlier):
    # Search y without observation error
    x1 = sorted(np.random.uniform(0., 10., n))
    x2 = sorted(np.random.uniform(0., 10., n))

    y = calculateYwithoutError(tetta, x1, x2, n)
    xall = []

    # Search observation error
    e = np.random.binomial(n=1., p=(1 - outlier), size=n)

    counter = 0
    for i in e:
        if i == 0:
            counter += 1

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
    return x.transpose()

def relativeError(tettaTrue, tettanew):
    n, counter = len(tettaTrue), 0
    for stepi in range(n):
        counter += pow((tettaTrue[stepi] - tettanew[stepi]), 2) / pow(tettaTrue[stepi], 2)
    return counter

def CheckList(randomIndexes, el):
    for i in randomIndexes:
        if i == el:
            return True
    return False

def TestSelectiveVaribles(X, Y, n, testFactor):
    xObject = MCD.Transform(X, n)
    xNew = xObject.MatrixInVector(xInterm=[[], []], X="a")
    yNew = Y.tolist()
    element = 0
    h = [i for i in range(n)]
    for i in range(0, len(xNew)):
        randomIndexes = []
        for j in range(int(testFactor * n)):
            testExistance = True
            while testExistance:
                element = random.choice(h)
                testExistance = CheckList(randomIndexes, element)
            randomIndexes.append(element)
        randomIndexes.sort(reverse=True)
        for j in randomIndexes:
            xNew[i].pop(j)
            if i == 0:
                yNew.pop(j)
    xNewArray = xObject.VectorInMatrix(xNew, [])
    xNew.clear()
    return xNewArray, np.array(yNew)

def main():
    n, tetta, tettaNew, p = 200, np.array([1., 1.5, 2.]), np.array([0., 0., 0.]), 2
    h = int((n + p + 1) / 2)
    Outlier = 0.05

    yTrue, xAll = ylinealModel(n=n, tetta=tetta, outlier=Outlier)
    X = np.zeros((len(tetta), n))
    X = filingMatrixX(X, lineToColum(xAll, n, tetta), tetta)

    xTest, yTest = TestSelectiveVaribles(X, yTrue, n, testFactor=0.2)
    tettaTest = LMSMatrix(xTest, yTest.reshape(len(yTest), 1))

    mcdMethod = MCD.MCD(X, n, yTrue)
    mcdMethod.FindRelativeDistances(X=X, n=n,mode="TestTask")
    xMCD, yMCD = mcdMethod.GetNewX(X, p, n, yTrue, xNew=[])
    tettaMCD = LMSMatrix(xMCD, yMCD.reshape(len(yMCD), 1))

    tettaLMS = LMSMatrix(X, yTrue.reshape(n, 1))
    print("\nOutlier = ", Outlier*100,"%", "\ntetta:\n", tettaNew)
    print("\nОтносительная ошибка:\n", relativeError(tettaTrue=tetta, tettanew=tettaNew))
    Outlier += 0.05

if __name__ == '__main__':
    main()

