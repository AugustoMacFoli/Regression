from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, io, base64, random
import sklearn.preprocessing, sklearn.linear_model, sklearn.svm, sklearn.model_selection
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
    if request.POST:
        try:
            curr_rdm = int(request.POST['curr_rdm'])
        except:
            pass
    else:
        curr_rdm = random.randint(0, 9999)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 1/3, random_state = curr_rdm)
    regressor = sklearn.svm.SVR(kernel = 'rbf')
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(sc_X.transform(X_test))
    user_values = []
    if request.POST:
        try:
            user_number = request.POST['user_number']
            scaled_user_number = sc_X.transform(numpy.array([[user_number]]))
            user_pred = sc_y.inverse_transform(regressor.predict(sc_X.transform(numpy.array([[user_number]]))))
            user_values = [user_number, user_pred]
        except:
            pass
    all_values = []
    for i in range(X.__len__()):
        all_values += [(X_original[i, 0], int(y_original[i]))]
    train_values = []
    for i in range(X_train.__len__()):
        train_values += [(round(float(sc_X.inverse_transform(X_train[i])), 2), sc_y.inverse_transform([y_train[i]]))]
    train_values = sorted(train_values)
    test_values = []
    for i in range(X_test.__len__()):
        test_values += [(round(float(sc_X.inverse_transform(X_test[i])), 2), (sc_y.inverse_transform([y_test[i]]), sc_y.inverse_transform([y_pred[i]])))]
    test_values = sorted(test_values)
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
    # Visualising the train results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X_train), max(X_train), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X_train, y_train, c = numpy.random.rand(X_train.__len__(),))
    matplotlib.pyplot.plot(X_grid, regressor.predict(X_grid), color = 'blue', alpha = 0.6)
    matplotlib.pyplot.xlabel('Years of Experience (scaled)')
    matplotlib.pyplot.ylabel('Salary (scaled)')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_train = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising the test results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X_train), max(X_train), 0.01)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X_test, y_test, c = numpy.random.rand(X_test.__len__(),))
    if user_values:
        matplotlib.pyplot.scatter(scaled_user_number, regressor.predict(sc_X.transform(numpy.array([[user_number]]))), color = 'red', label='User')
    matplotlib.pyplot.plot(X_grid, regressor.predict(X_grid), color = 'blue', alpha = 0.6)
    matplotlib.pyplot.xlabel('Years of Experience (scaled)')
    matplotlib.pyplot.ylabel('Salary (scaled)')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_test = base64.b64encode(buf.read()).decode()
    buf.close()
    context = {
        'all_values': all_values,
        'train_values': train_values,
        'test_values': test_values,
        'user_values': user_values,
        'curr_rdm': curr_rdm,
        'b64_train': b64_train,
        'b64_test': b64_test,
        'b64_all': b64_all
    }
    return render(request, 'svr/svr_play.html', context)