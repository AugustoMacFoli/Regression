from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas, random, io, base64
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot, numpy

def linear_regression(request):
    return render(request, 'linear_regression/linear_regression.html')

def linear_regression_play(request):
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = curr_rdm)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    user_values = []
    if request.POST:
        try:
            user_number = float(request.POST['user_number'])
            user_pred = regressor.predict([[user_number,]])
            user_values = (user_number, user_pred)
        except:
            pass
    all_values = []
    for i in range(X.__len__()):
        all_values += [(X[i, 0], int(y[i]))]
    train_values = []
    for i in range(X_train.__len__()):
        train_values += [(X_train[i, 0], int(y_train[i]))]
    train_values = sorted(train_values)
    test_values = []
    for i in range(X_test.__len__()):
        test_values += [(X_test[i, 0], (int(y_test[i]), int(y_pred[i])))]
    test_values = sorted(test_values)
    # Visualising All Data
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X, y, c=numpy.random.rand(X.__len__(),))
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_all = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising the Training set results
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X_train, y_train, c=numpy.random.rand(X_train.__len__(),))
    matplotlib.pyplot.plot(X_train, regressor.predict(X_train), color = 'blue', alpha=0.6)
    matplotlib.pyplot.xlabel('Years of Experience')
    matplotlib.pyplot.ylabel('Salary')
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_train = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising the Test set results
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X_test, y_test, c=numpy.random.rand(X_test.__len__(),))
    if user_values:
        try:
            matplotlib.pyplot.scatter(user_number, user_pred, color = 'red')
        except:
            pass
    matplotlib.pyplot.plot(X_train, regressor.predict(X_train), color = 'blue', alpha=0.6)
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
    return render(request, 'linear_regression/linear_regression_play.html', context)