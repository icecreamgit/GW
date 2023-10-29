import numpy as np
import random
import MCD
import LMS

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
    LMSObject = LMS.LMS(n=n, tetta=tetta, outlier=Outlier)

    yTrue, xAll = LMSObject.ylinealModel(n=n, tetta=tetta, outlier=Outlier)
    X = np.zeros((len(tetta), n))
    X = filingMatrixX(X, LMSObject.lineToColum(xAll, n, tetta), tetta)

    xTest, yTest = TestSelectiveVaribles(X, yTrue, n, testFactor=0.2)
    tettaTest = LMSObject.LMSMatrix(xTest, yTest.reshape(len(yTest), 1))

    mcdMethod = MCD.MCD(X, n, yTrue)
    mcdMethod.FindRelativeDistances(X=X, n=n,mode="TestTask")
    xMCD, yMCD = mcdMethod.GetNewX(X, p, n, yTrue, xNew=[])
    tettaMCD = LMSObject.LMSMatrix(xMCD, yMCD.reshape(len(yMCD), 1))

    tettaLMS = LMSObject.LMSMatrix(X, yTrue.reshape(n, 1))
    print("\nOutlier = ", Outlier*100,"%", "\ntetta:\n", tettaNew)
    print("\nОтносительная ошибка:\n", relativeError(tettaTrue=tetta, tettanew=tettaNew))
    Outlier += 0.05

if __name__ == '__main__':
    main()

