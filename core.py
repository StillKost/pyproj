import uuid
import csv
import matplotlib.pyplot as plt
import math
import numpy
import scipy.stats

def run(X, Y, N, K):
    RESULT = {
        "X": X,
        "Y": Y
    }

    # коэфициенты регрессии
    B = (((numpy.transpose(X) * X) ** -1) * numpy.transpose(X) * Y)
    
    RESULT["B"] = B

    # расчетные значения зависимой переменно
    YR = numpy.matrix(X * B)
    RESULT["YR"] = YR

    tmp = numpy.square(Y - YR)
    DAD = sum(tmp) / (N - K)

    RESULT["DAD"] = DAD

    YSR = sum(Y) / N

    RESULT["YSR"] = YSR

    DY = sum(numpy.square(Y - YSR)) / N - 1

    RESULT["DY"] = DY

    FR = DY / DAD
    RESULT["FR"] = FR

    F = scipy.stats.f.ppf(q=1-0.05, dfn =  N - 1, dfd = N- K)
    RESULT["F"] = F

    #if FR > F:
    #    print("Уравнвнение адекватно")
    #else:
    #    print("Уравнвнение не адекватно")

    RESULT["FR > F"] = FR > F

    # не работает почему то
    CORR = scipy.stats.pearsonr(numpy.asarray(Y).reshape(-1), numpy.asarray(YR).reshape(-1))

    RESULT["CORR"] = CORR[0]

    T = scipy.stats.t.ppf(0.975, N - K)

    RESULT["T"] = T

    G = (numpy.transpose(X) * X) ** - 1

    for i in range(0, K):
        D = T * math.sqrt(DAD * numpy.array(G)[i][i])
        _B = numpy.array(B)[i]
        res = "значим" if D > _B else "не значим"
        RESULT["D" + str(i)] = D

    model = "Y = "
    for i in range(0, K):
        _B = numpy.array(B)[i]
        model += str(_B) + "X" + str(i)
        if i != K - 1:
            model += " + "

    RESULT["Model"] = model

    # ошибка прогоноза
    D = X * ((X.transpose() * X) ** (-1)) * X.transpose()
    D = numpy.array(D)

    # доверительный интервал
    S = [0 for x in range(N)]
    for i in range(0, N):
        s = T * math.sqrt(DAD * (1 + D[i][i]))
        S[i] = s

    RESULT["S"] = S

    YRmax = numpy.array(YR) + numpy.array(S)
    YRmin = numpy.array(YR) - numpy.array(S)

    RESULT["YRmax"] = numpy.array(YRmax[0])
    RESULT["YRmin"] = numpy.array(YRmin[0])

    R = (sum(Y - YR) ** 2) / (sum(Y - YSR) ** 2)
    RESULT["R"] = R

    Ra = 1 - (1 - R ** 2) * ((N - 1)/(N - K))
    RESULT["Ra"] = Ra

    return RESULT

def printDic(dic):
    for key in dic:
        print("%s -> %s" % (key, dic[key]))

def plot(data, title="Plot"):
    plt.title = title
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.plot(data)
    plt.legend(data.columns.values)
    plt.show()

def export(header, data):
    with open(uuid.uuid4().hex + '.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(header)
        for item in data:
            d = []
            for key in header:
                try:
                    d.append(item[key])
                except:
                    d.append("undef")
            writer.writerow(d)