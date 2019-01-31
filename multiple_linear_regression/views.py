from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import io, random, base64, matplotlib.pyplot, pandas, sklearn.preprocessing, sklearn.model_selection, sklearn.linear_model

def multiple_linear_regression(request):
    return render(request, 'multiple_linear_regression/multiple_linear_regression.html')

def multiple_linear_regression_play(request):
    file = staticfiles_storage.path('xlsx/50_Startups.csv')
    dataset = pandas.read_csv(file)
    # dataset = pandas.read_csv('./static/xlsx/50_Startups.csv')
    X = dataset.iloc[:, :-2].values
    y = dataset.iloc[:, 4].values
    if request.POST:
        try:
            curr_rdm = int(request.POST['curr_rdm'])
        except:
            pass
    else:
        curr_rdm = random.randint(0, 9999)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.2, random_state = curr_rdm)
    regressor = sklearn.linear_model.LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    user_values = []
    if request.POST:
        try:
            txt_rd = int(request.POST['txt_rd'].replace(',', ''))
            txt_admin = int(request.POST['txt_admin'].replace(',', ''))
            txt_mkt = int(request.POST['txt_mkt'].replace(',', ''))
            user_pred = regressor.predict([[txt_rd, txt_admin, txt_mkt]])
            user_values = [txt_rd, txt_admin, txt_mkt, user_pred]
        except:
            pass
    # Visualising All Data
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X[:,0], y, color = 'green', label='R&D', alpha=0.6)
    matplotlib.pyplot.scatter(X[:,1], y, color = 'blue', label='Admin', alpha=0.6)
    matplotlib.pyplot.scatter(X[:,2], y, color = 'yellow', label='Mkt', alpha=0.6)
    matplotlib.pyplot.xlabel('Investment')
    matplotlib.pyplot.ylabel('Profit')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_all = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising Train Data
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X_train[:,0], y_train, color = 'green', label='R&D', alpha=0.6)
    matplotlib.pyplot.scatter(X_train[:,1], y_train, color = 'blue', label='Admin', alpha=0.6)
    matplotlib.pyplot.scatter(X_train[:,2], y_train, color = 'yellow', label='Mkt', alpha=0.6)
    for i in range(0, y.__len__()):
        try:
            matplotlib.pyplot.axhline(y=y_train[i], color='black', linestyle='-', alpha=0.1)
        except:
            pass
    matplotlib.pyplot.xlabel('Investment')
    matplotlib.pyplot.ylabel('Profit')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_train = base64.b64encode(buf.read()).decode()
    buf.close()
    # Visualising Test Data
    matplotlib.pyplot.clf()
    matplotlib.pyplot.scatter(X_test[:,0], y_test, color = 'green', label='R&D', alpha=0.6)
    matplotlib.pyplot.scatter(X_test[:,1], y_test, color = 'blue', label='Admin', alpha=0.6)
    matplotlib.pyplot.scatter(X_test[:,2], y_test, color = 'yellow', label='Mkt', alpha=0.6)
    for i in range(0, y.__len__()):
        try:
            matplotlib.pyplot.axhline(y=regressor.predict([X_test[i]]), color='black', linestyle='-', alpha=0.2)
        except:
            pass
    if user_values:
        try:
            y_predicted = regressor.predict([[txt_rd, txt_admin, txt_mkt]])
            matplotlib.pyplot.scatter(txt_rd, y_predicted, color = 'red', label='User', alpha=0.6)
            matplotlib.pyplot.scatter(txt_admin, y_predicted, color = 'red', alpha=0.6)
            matplotlib.pyplot.scatter(txt_mkt, y_predicted, color = 'red', alpha=0.6)
            matplotlib.pyplot.axhline(y=y_predicted, color='red', linestyle='-', alpha=0.2)
        except:
            pass
    matplotlib.pyplot.xlabel('Investment')
    matplotlib.pyplot.ylabel('Profit')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.tight_layout()
    buf = io.BytesIO()
    matplotlib.pyplot.savefig(buf, format='png')
    buf.seek(0)
    b64_test = base64.b64encode(buf.read()).decode()
    buf.close()
    all_values = []
    for i in range(X.__len__()):
        all_values += [[int(X[i, 0]), int(X[i, 1]), int(X[i, 2]), int(y[i])]]
    train_values = []
    for i in range(X_train.__len__()):
        train_values += [[int(X_train[i, 0]), int(X_train[i, 1]), int(X_train[i, 2]), int(y_train[i])]]
    train_values = sorted(train_values, key=lambda value: value[3], reverse=True)
    test_values = []
    for i in range(X_test.__len__()):
        test_values += [[int(X_test[i, 0]), int(X_test[i, 1]), int(X_test[i, 2]), int(y_test[i]), int(y_pred[i])]]
    test_values = sorted(test_values, key=lambda value: value[3], reverse=True)
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
    return render(request, 'multiple_linear_regression/multiple_linear_regression_play.html', context)









