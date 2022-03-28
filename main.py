import csv
import core
import pandas
import numpy

#E:\x.xlsx
#E:\y.xlsx

pathX = input("Укажите путь в файлу X: ")
while not pathX:
    pathX = input("Укажите путь в файлу X: ")

pathY = input("Укажите путь в файлу Y: ")
while not pathX:
    pathY = input("Укажите путь в файлу Y: ")

# читаю файлы
Xfile = pandas.read_excel(pathX, header=None)
Yfile = pandas.read_excel(pathY, header=None)

# делаю из них матрицы
X = numpy.matrix(numpy.array(Xfile))
Y = numpy.matrix(numpy.array(Yfile))

result1 = core.run(X, Y, 20, 5)
core.printDic(result1)
y = numpy.array(result1["Y"])
yr = numpy.array(result1["YR"])
core.plot(numpy.hstack((y, yr)))

X = numpy.hstack((X[:,0], X[:,1], X[:,3]))

result2 = core.run(X, Y, 20, 3)
core.printDic(result2)
y = numpy.array(result2["Y"])
yr = numpy.array(result2["YR"])

core.plot(numpy.hstack((y, yr)))

core.export(result1.keys(), [result1, result2])

print("End...")

