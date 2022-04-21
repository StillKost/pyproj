import core
import pandas
import numpy

def plotRes(res):
    y = numpy.asarray(res["Y"]).reshape(-1)
    yr = numpy.asarray(res["YR"]).reshape(-1)
    df = pandas.DataFrame({"Y": y, "YR": yr})
    df.columns = ["Y", "YR"]
    core.plot(df)
    core.plot(pandas.DataFrame({"YRmin": numpy.asarray(res["YRmin"]).reshape(-1), "YRmax": numpy.asarray(res["YRmax"]).reshape(-1), "Y": y, "YR": yr}))

def getData(pathX, pathY):
    #pathX = r"C:\Users\hetagurov\Desktop\pyproj\Data\1\X.xlsx" #input("Укажите путь в файлу X: ")
    #while not pathX:
    #    pathX = input("Укажите путь в файлу X: ")

    #pathY = r"C:\Users\hetagurov\Desktop\pyproj\Data\1\Y.xlsx" #input("Укажите путь в файлу Y: ")
    #while not pathX:
    #    pathY = input("Укажите путь в файлу Y: ")

    # читаю файлы
    Xfile = pandas.read_excel(pathX, header=None, dtype=float)
    Yfile = pandas.read_excel(pathY, header=None, dtype=float)

    # делаю из них матрицы
    X = numpy.matrix(numpy.array(Xfile))
    Y = numpy.matrix(numpy.array(Yfile))

    X = numpy.nan_to_num(X)
    Y = numpy.nan_to_num(Y)

    return [X, Y]

data1 = getData(r"C:\Users\hetagurov\Desktop\pyproj\Data\5\X.xlsx", r"C:\Users\hetagurov\Desktop\pyproj\Data\5\Y.xlsx")
X = data1[0]
Y = data1[1]
N = len(X)
K = len(X.transpose())

core.run_sklearn(X, Y, N)

#result1 = core.run(X, Y, N, K)
#core.printDic(result1)
#plotRes(result1)

# прогноз
#XP = pandas.read_excel(r"E:\pyproj\Data\backup\Xp.xlsx")
'''''
X = numpy.hstack((X[:,0], X[:,1], X[:,3]))
N = len(X)
K = len(X.transpose())
result2 = core.run(X, Y, N, K)
core.printDic(result2)
plotRes(result2)

X = numpy.hstack((X[:,0], X[:,1], X[:,2], numpy.array(X[:,1]) ** 2, numpy.array(X[:,2]) ** 2, numpy.array(X[:,2]) * numpy.array(X[:,1])))
N = len(X)
K = len(X.transpose())

result3 = core.run(X, Y, N, K)
core.printDic(result3)
plotRes(result3)

header = ["Model", "FR", "F", "CORR", "T", "R", "Ra", "AE", "RE"]
core.export(header, [result1, result2])

print("End...")

'''''