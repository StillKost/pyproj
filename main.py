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

core.run(X, Y, N, K)