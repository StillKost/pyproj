import core
import pandas
import numpy

N = 20
K = 5

# читаю файлы
Xfile = pandas.read_excel(r'E:\x.xlsx', header=None)
Yfile = pandas.read_excel(r'E:\y.xlsx', header=None)

# делаю из них матрицы
X = numpy.matrix(numpy.array(Xfile))
Y = numpy.matrix(numpy.array(Yfile))

result1 = core.run(X, Y, N, K)

core.printDic(result1)

y = numpy.array(result1["Y"])
yr = numpy.array(result1["YR"])

core.plot(numpy.hstack((y, yr)))

print("End...")

