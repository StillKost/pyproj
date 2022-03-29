import matplotlib.pyplot as plt
import core
import pandas
import numpy

def plotRes(res):
    y = numpy.asarray(res["Y"]).reshape(-1)
    yr = numpy.asarray(res["YR"]).reshape(-1)
    df = pandas.DataFrame({"Y": y, "YR": yr})
    df.columns = ["Y", "YR"]
    core.plot(df)
    core.plot(pandas.DataFrame({"YRmin": res["YRmin"], "YRmax": res["YRmax"], "Y": y, "YR": yr}))

#E:\x.xlsx
#E:\y.xlsx

pathX = r"E:\pyproj\Data\x.xlsx" #input("Укажите путь в файлу X: ")
while not pathX:
    pathX = input("Укажите путь в файлу X: ")

pathY = r"E:\pyproj\Data\y.xlsx" #input("Укажите путь в файлу Y: ")
while not pathX:
    pathY = input("Укажите путь в файлу Y: ")

# читаю файлы
Xfile = pandas.read_excel(pathX, header=None)
Yfile = pandas.read_excel(pathY, header=None)

# делаю из них матрицы
X = numpy.matrix(numpy.array(Xfile))
Y = numpy.matrix(numpy.array(Yfile))

result1 = core.run(X, Y, 20, 5)
#core.printDic(result1)
plotRes(result1)

X = numpy.hstack((X[:,0], X[:,1], X[:,3]))

result2 = core.run(X, Y, 20, 3)
#core.printDic(result2)
plotRes(result2)

core.export(result1.keys(), [result1, result2])

print("End...")

