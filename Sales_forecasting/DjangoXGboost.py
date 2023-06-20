 
def readMachineLearingData(request): 
 
    global xgb_sales

    orders = pd.DataFrame(list(Ml.objects.all().values())) 
    orders = orders.drop(labels = ['updated', 'id'], axis=1) 
    orders['totalPrice'] = orders['unitPrice'] * orders['quantity'] 
    orders.invoiceNo = pd.to_numeric(orders.invoiceNo) 
    # Convert InvoiceDate to datetime object 
    orders.invoiceDate = pd.to_datetime(orders.invoiceDate) 

    # Truncate the minutes part of datetime object 
    orders['invoiceDate'] = orders.invoiceDate.dt.date 

    orders = orders.groupby(['invoiceDate'], as_index=False).sum() 

    orders.invoiceDate = pd.to_datetime(orders.invoiceDate) 

    orders['Week'] = orders.invoiceDate.dt.week 
    orders['Weekday'] = orders.invoiceDate.dt.weekday 
    orders['Day'] = orders.invoiceDate.dt.day 

    orders.drop(labels = ['invoiceNo', 'invoiceDate', 'stockCode', 'description', 'customerID', 'quantity', 'country', 'unitPrice'], axis=1) 
    # orders['unitPrice'] = orders.totalPrice/orders.quantity 

    # Drop rows with negative Quantity 
    orders = orders.drop(orders[orders.quantity<=0].index).reset_index(drop=True) 
    orders = orders.drop(orders[orders.totalPrice<=0].index).reset_index(drop=True) 

    # Removing outliers in Quantity and TotalPrice 
    orders = orders[(np.abs(stats.zscore(orders.quantity)) < 3)] 
    orders = orders[(np.abs(stats.zscore(orders.totalPrice)) < 3)] 
    X_train = orders[['Week', 'Weekday', 'Day']] 
    Y_train = orders[['totalPrice']] 
    xgb_model = xgb.XGBRegressor(random_state=42, gamma=0.5, learning_rate=0.8, max_depth=3, n_estimators=250, subsample=0.4) 
    xgb_model.fit(X_train, Y_train) 

    xgb_sales = xgb_model

def readMachineLearingData2(type): 
    global xgb_sales

    orders = pd.DataFrame(list(Ml.objects.all().values())) 
    orders = orders.drop(labels = ['updated', 'id'], axis=1) 
    orders['totalPrice'] = orders['unitPrice'] * orders['quantity'] 
    orders.invoiceNo = pd.to_numeric(orders.invoiceNo) 
    # Convert InvoiceDate to datetime object 
    orders.invoiceDate = pd.to_datetime(orders.invoiceDate) 

    # Truncate the minutes part of datetime object 
    orders['invoiceDate'] = orders.invoiceDate.dt.date 

    orders = orders.groupby(['invoiceDate'], as_index=False).sum() 

    orders.invoiceDate = pd.to_datetime(orders.invoiceDate) 

    orders['Week'] = orders.invoiceDate.dt.week 
    orders['Weekday'] = orders.invoiceDate.dt.weekday 
    orders['Day'] = orders.invoiceDate.dt.day 

    orders.drop(labels = ['invoiceNo', 'invoiceDate', 'stockCode', 'description', 'customerID', 'quantity', 'country', 'unitPrice'], axis=1) 
    # orders['unitPrice'] = orders.totalPrice/orders.quantity 

    # Drop rows with negative Quantity 
    orders = orders.drop(orders[orders.quantity<=0].index).reset_index(drop=True) 
    orders = orders.drop(orders[orders.totalPrice<=0].index).reset_index(drop=True) 

    # Removing outliers in Quantity and TotalPrice 
    orders = orders[(np.abs(stats.zscore(orders.quantity)) < 3)] 
    orders = orders[(np.abs(stats.zscore(orders.totalPrice)) < 3)] 
    X_train = orders[['Week', 'Weekday', 'Day']] 
    Y_train = orders[['totalPrice']] 
    xgb_model = xgb.XGBRegressor(random_state=42, gamma=0.5, learning_rate=0.8, max_depth=3, n_estimators=250, subsample=0.4) 
    xgb_model.fit(X_train, Y_train) 

    return xgb_model

def predictXG(request): 
    print(request) 
    global xgb_sales
    # data = request..decode('utf8').replace("'", '"') 
    # data = json.loads(data) 
    # data = json.dumps(data, indent=4, sort_keys=True) 
    # data = json.loads(data) 
            
    start = request.GET['start'] 
    end =  request.GET['end']         
    
    print("xgb_sales") 
    print(xgb_sales) 
    
    if (xgb_sales is not None): 
        print("asdasdas") 
        date = pd.date_range(start, end) 
        X_pred = pd.DataFrame(date) 
        X_pred.columns = ['Date'] 
        X_pred['Date'] = pd.to_datetime(X_pred["Date"]) 

        print(X_pred) 
        X_pred['Week'] = X_pred.Date.dt.week 
        X_pred['Weekday'] = X_pred.Date.dt.weekday 
        X_pred['Day'] = X_pred.Date.dt.day 
        # X_pred['unitPrice'] = UnitPrice 
        # X_pred['unitPrice'] =  float(UnitPrice) 
        
        X_pred=X_pred.drop(labels = ['Date'], axis=1) 
        
        y_pred = xgb_sales.predict(X_pred) 
        Y_pred = pd.DataFrame({"Date": date, "Total sales": y_pred}) 
        Y_pred['Date'] = Y_pred['Date'].dt.strftime('%Y-%m-%d') 
        Y_pred = Y_pred.to_json() 
        
        return HttpResponse(Y_pred)
    else:
        xgb_sales = readMachineLearingData2() 
        predicted =  predict2(xgb_sales, start, end, UnitPrice) 
        predicted['Date'] = predicted['Date'].dt.strftime('%Y-%m-%d') 
        predicted = predicted.to_json()
        
        return HttpResponse(predicted)

def predict2(xgb_sales, start, end): 
        
    date = pd.date_range(start, end) 
    X_pred = pd.DataFrame(date) 
    X_pred.columns = ['Date'] 
    X_pred['Date'] = pd.to_datetime(X_pred["Date"]) 

    print(X_pred) 
    X_pred['Week'] = X_pred.Date.dt.week 
    X_pred['Weekday'] = X_pred.Date.dt.weekday 
    X_pred['Day'] = X_pred.Date.dt.day 
    # X_pred['unitPrice'] = UnitPrice 
    # X_pred['unitPrice'] =  float(UnitPrice) 
    
    X_pred=X_pred.drop(labels = ['Date'], axis=1) 
    
    y_pred = xgb_sales.predict(X_pred) 
    Y_pred = pd.DataFrame({"Date": date, "Total sales": y_pred}) 
    
    return Y_pred

























