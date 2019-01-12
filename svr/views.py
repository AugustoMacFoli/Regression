from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, io, base64
import sklearn.preprocessing, sklearn.linear_model, sklearn.svm
import matplotlib.pyplot, numpy

def svr(request):
    return render(request, 'svr/svr.html')

def svr_play(request):
    file = staticfiles_storage.path('xlsx/Salary_Data.csv')
    dataset = pandas.read_csv(file)
    # dataset = pandas.read_csv('./static/xlsx/Salary_Data.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    X_original = dataset.iloc[:, :-1].values
    y_original = dataset.iloc[:, 1].values
    sc_X = sklearn.preprocessing.StandardScaler()
    sc_y = sklearn.preprocessing.StandardScaler()
    X = sc_X.fit_transform(X)
    y = numpy.ravel(sc_y.fit_transform(y.reshape(-1, 1)))
    regressor = sklearn.svm.SVR(kernel = 'rbf')
    regressor.fit(X, y)
    user_values = []
    if request.POST:
        user_number = request.POST['user_number']
        scaled_user_number = sc_X.transform(numpy.array([[user_number]]))
        user_pred = sc_y.inverse_transform(regressor.predict(sc_X.transform(numpy.array([[user_number]]))))
        user_values = [user_number, user_pred]
    all_values = []
    for i in range(X.__len__()):
        all_values += [(X_original[i, 0], int(y_original[i]))]
    # Visualising All Data
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X), max(X), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X_original, y_original, c = numpy.random.rand(X.__len__(),))
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_all = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising the SVR results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X), max(X), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X, y, c = numpy.random.rand(X.__len__(),))
    if user_values:
        matplotlib.pyplot.scatter(scaled_user_number, regressor.predict(sc_X.transform(numpy.array([[user_number]]))), color = 'red')
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
    print(user_values)
    return render(request, 'svr/svr_play.html', context)