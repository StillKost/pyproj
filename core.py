import math
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.stats

def run(X, Y, N, K):
    print("X = \r\n", X)
    print("Y = \r\n", Y)
    # коэфициенты регрессии
    B = numpy.matrix(((numpy.transpose(X) * X) ** -1) * numpy.transpose(X) * Y)
    print("B = \r\n", B)

    # расчетные значения зависимой переменно
    YR = numpy.matrix(X * B)
    print("YR = \r\n", YR)

    plot(numpy.hstack((Y, YR)))

    tmp = numpy.square(Y - YR)
    DAD = sum(tmp) / (N - K)
    print("DAD = \r\n", DAD)

    YSR = sum(Y) / N
    print("YSR = \r\n", YSR)

    DY = sum(numpy.square(Y - YSR)) / N - 1
    print("DY = \r\n", DY)

    FR = DY / DAD
    print("FR = \r\n", FR)

    F = scipy.stats.f.ppf(q=1-0.05, dfn =  N - 1, dfd = N- K)
    print("F = \r\n", F)

    if FR > F:
        print("Уравнвнение адекватно")
    else:
        print("Уравнвнение не адекватно")

    CORR = scipy.stats.pearsonr(Y, YR)
    print("CORR = \r\n", CORR[0])

    T = scipy.stats.t.ppf(0.975, N - K)
    print("F = \r\n", T)

    G = (numpy.transpose(X) * X) ** - 1
    print("G = \r\n", G)

    for i in range(0, K):
        D = T * math.sqrt(DAD * numpy.array(G)[i][i])
        _B = numpy.array(B)[i]
        res = "значим" if D > _B else "не значим"
        print("D" + str(i) + " = \r\n", D, " " + res)

    model = "Y = "
    for i in range(0, K):
        _B = numpy.array(B)[i]
        model += str(_B) + "X" + str(i) + "*"

    print(model)

def plot(data, title="Plot"):
    plt.title = title
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.plot(data)
    plt.show()