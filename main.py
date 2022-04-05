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

#E:\x.xlsx
#E:\y.xlsx

pathX = r"E:\pyproj\Data\old_x.xlsx" #input("Укажите путь в файлу X: ")
while not pathX:
    pathX = input("Укажите путь в файлу X: ")

pathY = r"E:\pyproj\Data\old_y.xlsx" #input("Укажите путь в файлу Y: ")
while not pathX:
    pathY = input("Укажите путь в файлу Y: ")

# читаю файлы
Xfile = pandas.read_excel(pathX, header=None, dtype=float)
Yfile = pandas.read_excel(pathY, header=None, dtype=float)

# делаю из них матрицы
X = numpy.matrix(numpy.array(Xfile))
Y = numpy.matrix(numpy.array(Yfile))

N = len(X)
K = len(X.transpose())
result1 = core.run(X, Y, N, K)
core.printDic(result1)
plotRes(result1)

# прогноз
#XP = pandas.read_excel(r"E:\pyproj\Data\backup\Xp.xlsx")

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

