import numpy as np
import random
import MCD
import LMS
import M_Estimators as MEst

def filingMatrixX(x, xall, tetta):
    nTetta = len(tetta)
    n = len(x)
    for stepi in range(n):
        x[stepi][0] = 1.
    for stepi in range(n):
        for stepj in range(1, nTetta):
            x[stepi][stepj] = xall[stepj - 1][stepi]
    return x

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
    n, tetta, tettaNew, p = 200, np.array([1., 1.5, 2.]), np.array([0., 0., 0.]), 3
    h = int(0.75 * n)
    Outlier = 0.2
    LSObject = LMS.LMS(n=n, tetta=tetta, outlier=Outlier)
    MObject = MEst.M_Estimators()

    Y, xAll = LSObject.ylinealModel(n=n, tetta=tetta, outlier=Outlier)
    X = np.zeros((n, len(tetta)))
    X = filingMatrixX(X, LSObject.lineToColum(xAll, n, tetta), tetta)
    tettaLS = LSObject.LSMatrix(X, Y)

    tettaMEstHuber = MObject.MainEstimators(tettaLS, "Huber", X, Y, n)
    tettaMEstCauchy = MObject.MainEstimators(tettaLS, "Cauchy", X, Y, n)

    mcdMethod = MCD.MCD(xAll, Y, n, p)
    xVectorMCD, yVectorMCD = mcdMethod.FindRelativeDistances(X=xAll, n=n, h=h)
    xMatrixMCD = filingMatrixX(x=np.zeros((h, len(tetta))), xall=LSObject.lineToColum(xVectorMCD, h, tetta), tetta=tetta)
    # xMCD, yMCD = mcdMethod.GetNewX(X, p, n, yTrue, xNew=[])
    tettaMCD = LSObject.LSMatrix(xMatrixMCD, yVectorMCD)

    print(f"tettaLS:\t{tettaLS}\n"
          f"tettaMCD:\t{tettaMCD}")
    print("\nOutlier = ", Outlier*100,"%", "\ntetta:\n", tettaNew)
    print("\nОтносительная ошибка:\n", relativeError(tettaTrue=tetta, tettanew=tettaNew))
    Outlier += 0.05

if __name__ == '__main__':
    main()

