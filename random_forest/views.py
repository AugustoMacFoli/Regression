from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, io, base64
import sklearn.preprocessing, sklearn.ensemble
import matplotlib.pyplot, numpy

def random_forest(request):
    return render(request, 'random_forest/random_forest.html')

def random_forest_play(request):
    file = staticfiles_storage.path('xlsx/Salary_Data.csv')
    dataset = pandas.read_csv(file)
    # dataset = pandas.read_csv('./static/xlsx/Salary_Data.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    regressor = sklearn.ensemble.RandomForestRegressor(n_estimators = 10, random_state = 0)
    regressor.fit(X, y)
    user_values = []
    if request.POST:
        user_number = float(request.POST['user_number'])
        user_pred = regressor.predict([[user_number]])
        user_values = [user_number, user_pred]
    all_values = []
    for i in range(X.__len__()):
        all_values += [(X[i, 0], int(y[i]))]
    # Visualising All Data
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X), max(X), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X, y, c = numpy.random.rand(X.__len__(),))
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_all = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising the Decision Tree Regression results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X, y, c = numpy.random.rand(X.__len__(),))
    if user_values:
        matplotlib.pyplot.scatter(user_number, regressor.predict([[user_number]]), color = 'red')
    matplotlib.pyplot.plot(X_grid, regressor.predict(X_grid), color = 'blue', alpha = 0.6)
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_test = base64.b64encode(buf.read()).decode()
    buf.close()
    context = {
        'all_values': all_values,
        'user_values': user_values,
        'b64_test': b64_test,
        'b64_all': b64_all
    }
    return render(request, 'random_forest/random_forest_play.html', context)