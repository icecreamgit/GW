import numpy as np

def T0(xMassive, j, h):
    mean = 0
    for value in xMassive:
        mean += value[j]
    return mean / h

class Transform:
    # Меняем горизонтальный вид элементов матрицы на вертикальный
    def __init__(self, X, n):
        self.X = X
        self.n = n
    def MatrixInVector(self, xInterm, X=None, n=None):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        if isinstance(X, str):
            count = 0
            for line in xInterm:
                count += 1
                for i in range(self.n):
                    line.append(self.X[i][count])
        else:
            count = 0
            for line in xInterm:
                count += 1
                for i in range(n):
                    line.append(X[i][count])
        return xInterm
    def VectorInMatrix(self, X, xNew):
        n = len(X[0])
        for j in range(n):
            xNew.append([1., X[0][j], X[1][j]])
        return np.array(xNew)

def KeyFuncion(item):
    return item[1]
class MCD:
    def __init__(self, X, n, Y):
        self.X = X
        self.n = n
        self.Y = Y

    def FindRelativeDistances(self, X, n, mode):
        # Т.к. в питоне нет перегрузки методов, приходится использовать костыль:
        B, xInterm, self.di = [], [[], []], []
        xObject = Transform(X, n)
        p = 2

        if (mode == "TestTask"):
            xInterm = xObject.MatrixInVector([[], []], X="a")
            data = np.array([xInterm[0], xInterm[1]])
            S = np.cov(data, bias=True)

            if np.linalg.det(S) == 0:
                print("det(S) == 0!")

            mean_X0 = T0(xInterm, 0, n)
            mean_X1 = T0(xInterm, 1, n)
            for i in range(n):
                B.append([[xInterm[0][i] - mean_X0], [xInterm[1][i] - mean_X1]])

            for i in range(n):
                a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
                self.di.append([i, np.dot(a, np.array(B[i]))[0][0]])
            self.di.sort(key=KeyFuncion)
        else:
            while 1:
                h = int((n + p + 1) / 2)
                xInterm = xObject.MatrixInVector([[], []], X="a")
                data = np.array([xInterm[0], xInterm[1]])
                S = np.cov(data, bias=True)

                if np.linalg.det(S) == 0:
                    print("det(S) == 0!")
                    break

                mean_X0 = T0(xInterm, 0, h)
                mean_X1 = T0(xInterm, 1, h)
                for i in range(h):
                    B.append([[xInterm[0][i] - mean_X0], [xInterm[1][i] - mean_X1]])

                for i in range(h):
                    a = np.dot(np.array(B[i]).transpose(), pow(S, -1))
                    self.di.append(np.dot(a, np.array(B[i]))[0][0])
                xInterm.clear()
        B.clear()
        xInterm.clear()

    def GetNewX(self, X, p, n, Y, xNew):
        xObject = Transform(X, n)
        dh = MCD.SetHValuesRelativeDistances(self, p=p, n=n)
        xInterm = xObject.MatrixInVector([[], []], X="a")
        yNew = []
        for j in dh:
            xNew.append([1., xInterm[0][j[0]], xInterm[1][j[0]]])
            yNew.append(Y[j[0]])
        return np.array(xNew), np.array(yNew)
    def SetHValuesRelativeDistances(self, p, n):
        h = int((n + p + 1) / 2)
        return [self.di[i] for i in range(h)]
    def GetRelativeDistances(self):
        return self.di
