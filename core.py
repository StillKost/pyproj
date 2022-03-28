import matplotlib.pyplot as plt
import math
import numpy
import scipy.stats

def run(X, Y, N, K):
    RESULT = {
        "X": X,
        "Y": Y
    }

    #print("X = \r\n", X)
    #print("Y = \r\n", Y)
    # коэфициенты регрессии
    B = numpy.matrix(((numpy.transpose(X) * X) ** -1) * numpy.transpose(X) * Y)
    #print("B = \r\n", B)

    RESULT["B"] = B

    # расчетные значения зависимой переменно
    YR = numpy.matrix(X * B)
    #print("YR = \r\n", YR)

    RESULT["YR"] = YR

    # plot(numpy.hstack((Y, YR)))

    tmp = numpy.square(Y - YR)
    DAD = sum(tmp) / (N - K)
    #print("DAD = \r\n", DAD)

    RESULT["DAD"] = DAD

    YSR = sum(Y) / N
    #print("YSR = \r\n", YSR)

    RESULT["YSR"] = YSR

    DY = sum(numpy.square(Y - YSR)) / N - 1
    #print("DY = \r\n", DY)

    RESULT["DY"] = DY

    FR = DY / DAD
    #print("FR = \r\n", FR)

    RESULT["FR"] = FR

    F = scipy.stats.f.ppf(q=1-0.05, dfn =  N - 1, dfd = N- K)
    #print("F = \r\n", F)

    RESULT["F"] = F

    #if FR > F:
    #    print("Уравнвнение адекватно")
    #else:
    #    print("Уравнвнение не адекватно")

    RESULT["FR > F"] = FR > F

    # не работает почему то
    #CORR = scipy.stats.pearsonr(Y, YR)
    #print("CORR = \r\n", CORR[0])

    #RESULT["CORR"] = CORR[0]

    T = scipy.stats.t.ppf(0.975, N - K)
    #print("T = \r\n", T)

    RESULT["T"] = T

    G = (numpy.transpose(X) * X) ** - 1
    #print("G = \r\n", G)
    RESULT["G"] = G

    for i in range(0, K):
        D = T * math.sqrt(DAD * numpy.array(G)[i][i])
        _B = numpy.array(B)[i]
        res = "значим" if D > _B else "не значим"
        #print("D" + str(i) + " = \r\n", D, " " + res)
        RESULT["D" + str(i)] = D

    model = "Y = "
    for i in range(0, K):
        _B = numpy.array(B)[i]
        model += str(_B) + "X * " + str(i)
        if i != K - 1:
            model += " + "

    RESULT["Model"] = model

    return RESULT



def printDic(dic):
    for key in dic:
        print("%s -> %s" % (key, dic[key]))

def plot(data, title="Plot"):
    plt.title = title
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.plot(data)
    plt.show()