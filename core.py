from asyncio.windows_events import NULL
from pandas import array
import pandas
from sklearn.datasets import load_iris
from sklearn.metrics import matthews_corrcoef
from sklearn.feature_selection import f_regression, mutual_info_regression
from sklearn import linear_model

import uuid
import csv
import matplotlib.pyplot as plt
import math
import numpy
import scipy.stats

def run_sklearn(X, Y, N):   
    numpy.seterr(divide='ignore', invalid='ignore')
    reg = linear_model.LinearRegression()

    m = reg.fit(X, Y)

    print("N = ", N)
    print("K = ", reg.n_features_in_)

    T = scipy.stats.t.ppf(0.975, N - reg.n_features_in_)
    print("T = ", T)

    # если есть фиктивный столбец то B0 = 0 всегда ???
    B =  numpy.transpose(reg.coef_) #(((numpy.transpose(X) * X) ** -1) * numpy.transpose(X) * Y)

    print("B = ", B)

    F = scipy.stats.f.ppf(q=1 - 0.05, dfn= N - 1, dfd= N - reg.n_features_in_)
    print("F = ", F)

    Rsq = m.score(X, Y)
    print("Rsq = ", Rsq ** 2)

    Ra = 1 - (1 - Rsq ** 2) * ((N - 1)/(N - reg.n_features_in_))    
    print("Rasq", Ra ** 2)

    f_test = (Rsq / (1 - Rsq)) * ((N - reg.n_features_in_ - 1) / reg.n_features_in_)
    print("f_test = ", f_test)

    YR = (X * numpy.matrix(reg.coef_).transpose())

    CORR = scipy.stats.pearsonr(numpy.asarray(Y).reshape(-1), numpy.asarray(YR).reshape(-1))
    print("CORR = ", CORR[0])

    YR = numpy.matrix(X * B)
    print("YR = ", YR)
    tmp = numpy.square(Y - YR)
    DAD = sum(tmp) / (N - reg.n_features_in_)

    D = X * ((X.transpose() * X) ** (-1)) * X.transpose()
    D = numpy.array(D)

    S = [0 for x in range(N)]
    for i in range(0, N):
        s = T * math.sqrt(DAD * (1 + D[i][i]))
        S[i] = s
        

    YRmax = (YR) + (S)
    YRmin = (YR) - (S)    

    y = numpy.asarray(Y).reshape(-1)
    yr = numpy.asarray(YR).reshape(-1)

    df = pandas.DataFrame({"Y": y, "YR": yr})
    df.columns = ["Y", "YR"]
    plot(df)
    plot(pandas.DataFrame({"YRmin": numpy.asarray(YRmin)[0], "YRmax": numpy.asarray(YRmax)[0], "Y": y, "YR": yr}))


    if f_test > F:
        print("Уравнвнение адекватно")
    else:
        print("Уравнвнение не адекватно")

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
        RESULT["D" + str(i)] = str(D) + ' - ' + res

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

    YRmax = (YR) + (S)
    YRmin = (YR) - (S)

    RESULT["YRmax"] = (YRmax[:,0])
    RESULT["YRmin"] = (YRmin[:,0])

    R = (sum(Y - YR) ** 2) / (sum(Y - YSR) ** 2)
    RESULT["R"] = R
    RESULT["Rsq"] = str(R ** 2)

    Ra = 1 - (1 - R ** 2) * ((N - 1)/(N - K))
    RESULT["Ra"] = Ra
    RESULT["Rasq"] = Ra ** 2

    TR = abs(CORR[0]) * numpy.sqrt((N - K)/(1-CORR[0] ** 2))
    RESULT["TR"] = TR
    return RESULT

#def run_sklearn():

def printDic1(dic):
    for key in dic:
        print("%s -> %s" % (key, dic[key]))

def printDic(dic, keys:array = NULL):
    for key in dic:
        if (key in keys) == True:
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