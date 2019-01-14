from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, io, base64, random
import sklearn.preprocessing, sklearn.linear_model, sklearn.model_selection
import matplotlib.pyplot, numpy

def polynomial_regression(request):
    return render(request, 'polynomial_regression/polynomial_regression.html')

def polynomial_regression_play(request):
    file = staticfiles_storage.path('xlsx/Salary_Data.csv')
    dataset = pandas.read_csv(file)
    # dataset = pandas.read_csv('./static/xlsx/Salary_Data.csv')
    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    
    if request.POST:
        try:
            curr_rdm = int(request.POST['curr_rdm'])
        except:
            pass
    else:
        curr_rdm = random.randint(0, 9999)
    
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 1/3, random_state = curr_rdm)
    
    poly_reg = sklearn.preprocessing.PolynomialFeatures(degree = 8)
    X_poly = poly_reg.fit_transform(X_train)
    poly_reg.fit(X_poly, y_train)
    lin_reg_2 = sklearn.linear_model.LinearRegression()
    lin_reg_2.fit(X_poly, y_train)
    
    y_pred = lin_reg_2.predict(poly_reg.fit_transform(X_test))
    
    train_values = []
    for i in range(X_train.__len__()):
        train_values += [(X_train[i, 0], int(y_train[i]))]
    train_values = sorted(train_values)
    
    test_values = []
    for i in range(X_test.__len__()):
        test_values += [(X_test[i, 0], (int(y_test[i]), int(y_pred[i])))]
    test_values = sorted(test_values)
    
    user_values = []
    if request.POST:
        try:
            user_number = float(request.POST['user_number'])
            user_pred = lin_reg_2.predict(poly_reg.fit_transform([[user_number]]))
            user_values = [user_number, user_pred]
        except:
            pass
        
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
    
    # Visualising the Train Results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X_train), max(X_train), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X_train, y_train, c = numpy.random.rand(X_train.__len__(),))
    matplotlib.pyplot.plot(X_grid, lin_reg_2.predict(poly_reg.fit_transform(X_grid)), color = 'blue', alpha = 0.4)
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_train = base64.b64encode(buf.read()).decode()
    buf.close()
    
    # Visualising the Test results
    matplotlib.pyplot.clf()
    X_grid = numpy.arange(min(X_train), max(X_train), 0.1)
    X_grid = X_grid.reshape((len(X_grid), 1))
    matplotlib.pyplot.scatter(X_test, y_test, c = numpy.random.rand(X_test.__len__(),))
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
        'train_values': train_values,
        'test_values': test_values,
        'user_values': user_values,
        'curr_rdm': curr_rdm,
        'b64_train': b64_train,
        'b64_test': b64_test,
        'b64_all': b64_all
    }
    
    return render(request, 'polynomial_regression/polynomial_regression_play.html', context)