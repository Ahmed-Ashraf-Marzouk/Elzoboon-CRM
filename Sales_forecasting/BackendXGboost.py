#  This function going to be used to integrate with Django backend
                                            #---- Data warehousing ----#
#                                                 ----------------
#-----
import pandas as pd #reading and writing csv files  
import numpy as np # dealing with arrays 
import seaborn as sns # for advanced graphs 
import matplotlib.pyplot as plt # for traditional graphs 
from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb

import warnings
warnings.filterwarnings('ignore')
                                            #---- Machine learning ----#
#                                                 ---------------- 

# draw matplotlib graphs inline 
%matplotlib inline
sns.set_style("whitegrid") # configuration for seaborn library


# Input: file
# Output: GradientBoostingRegressor Object
def train(file):
    orders = pd.read_csv(file, index_col=0)
    # orders = from database as DataFrame
    orders['TotalPrice'] = orders['UnitPrice'] * orders['Quantity']
    orders.InvoiceNo = pd.to_numeric(orders.InvoiceNo)
    # Convert InvoiceDate to datetime object
    orders.InvoiceDate = pd.to_datetime(orders.InvoiceDate)

    # Truncate the minutes part of datetime object
    orders['InvoiceDate'] = orders.InvoiceDate.dt.date

    orders = orders.groupby(['InvoiceDate', 'StockCode'], as_index=False).sum()

    orders.InvoiceDate = pd.to_datetime(orders.InvoiceDate)

    orders['Week'] = orders.InvoiceDate.dt.week
    orders['Weekday'] = orders.InvoiceDate.dt.weekday
    orders['Day'] = orders.InvoiceDate.dt.day

    orders.drop(labels = ['InvoiceNo', 'InvoiceDate', 'StockCode', 'Description', 'CustomerID', 'Quantity', 'Country', 'UnitPrice'], axis=1)
    orders['UnitPrice'] = orders.TotalPrice/orders.Quantity

    # Drop rows with negative Quantity
    orders = orders.drop(orders[orders.Quantity<=0].index).reset_index(drop=True)
    orders = orders.drop(orders[orders.TotalPrice<=0].index).reset_index(drop=True)

    # Removing outliers in Quantity and TotalPrice
    orders = orders[(np.abs(stats.zscore(orders.Quantity)) < 3)]
    orders = orders[(np.abs(stats.zscore(orders.TotalPrice)) < 3)]
    X_train = orders[['Week', 'Weekday', 'Day', 'UnitPrice']]
    Y_train = orders[['Quantity']]
    xgb_model = xgb.XGBRegressor(random_state=42, gamma=0.5, learning_rate=0.8, max_depth=3, n_estimators=250, subsample=0.4)
    xgb_model.fit(X_train, Y_train)
    return xgb_model



# Input: start and end dates
# Output: A DataFrame of each date with expected Quantity
def predict(xgb_model, start, end, UnitPrice):
    if (xgb_model is not None):
        X_pred = pd.DataFrame(pd.date_range(start, end))
        X_pred.columns = ['Date']
        X_pred['Week'] = X_pred.InvoiceDate.dt.week
        X_pred['Weekday'] = X_pred.InvoiceDate.dt.weekday
        X_pred['Day'] = X_pred.InvoiceDate.dt.day
        X_pred['UnitPrice'] = UnitPrice
        y_pred = xgb_model.predict(X_pred)
        Y_pred = pd.DataFrame({"Date": pd.date_range(start, end), "Quantity_pred": y_pred})
        return Y_pred
    return None


# xgb_model = train('../../sales_forecasting/code/Online_Retail.xlsx')

# print(predict(xgb_model, '2011-11-01', '2011-11-04' ))

