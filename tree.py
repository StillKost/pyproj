from sklearn import metrics
import core
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import scipy.stats

def run(X, y):    
    N = len(X)
    K = len(X.transpose())

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = DecisionTreeRegressor()
    regressor.fit(X_train, y_train)

    Rsq = regressor.score(X_test, y_test)
    print("Rsq = ", Rsq) # Rsq

    F = scipy.stats.f.ppf(q=1 - 0.05, dfn= N - 1, dfd= N - K)
    print("F = ", F)

    f_test = (Rsq / (1 - Rsq)) * ((N - K - 1) / K)
    print("f_test = ", f_test)

    if f_test > F:
        print("Уравнвнение адекватно")
    else:
        print("Уравнвнение не адекватно")