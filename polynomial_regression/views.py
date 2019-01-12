from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, io, base64
import sklearn.preprocessing, sklearn.linear_model
import matplotlib.pyplot, numpy

def polynomial_regression(request):
    return render(request, 'polynomial_regression/polynomial_regression.html')

def polynomial_regression_play(request):
    file = staticfiles_storage.path('xlsx/Salary_Data.csv')
    dataset = pandas.read_csv(file)
    # dataset = pandas.read_csv('./static/xlsx/Salary_Data.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    poly_reg = sklearn.preprocessing.PolynomialFeatures(degree = 8)
    X_poly = poly_reg.fit_transform(X)
    poly_reg.fit(X_poly, y)
    lin_reg_2 = sklearn.linear_model.LinearRegression()
    lin_reg_2.fit(X_poly, y)
    user_values = []
    if request.POST:
        user_number = float(request.POST['user_number'])
        user_pred = lin_reg_2.predict(poly_reg.fit_transform([[user_number]]))
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
    # Visualising the Polynomial Regression results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X), max(X), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X, y, c = numpy.random.rand(X.__len__(),))
    if request.POST:
        try:
            matplotlib.pyplot.scatter(user_number, lin_reg_2.predict(poly_reg.fit_transform([[user_number]])), color = 'red')
        except:
            pass
    matplotlib.pyplot.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue', alpha = 0.4)
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
    return render(request, 'polynomial_regression/polynomial_regression_play.html', context)