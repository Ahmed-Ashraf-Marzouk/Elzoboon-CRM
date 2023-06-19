import pandas as pd
# Description: Graph shows sales trend for each day from start to end dates
# Input:
# 1. File
# 2. start date
# 3. end date
# Output:
# 1. Date | Mean of sales
# 2. Date | Sales for each day
def sales_trend(file, start, end):
    df = pd.read_csv(file, index_col=0)
    datesIndex = pd.date_range(start, end, freq= 'M')
    datesIndex = datesIndex.tolist()
    df['invoiceDate'] = pd.to_datetime(df.invoiceDate)
    df = df.loc[df['invoiceDate'].between(start, end)]
    df.head()
    general_trend = pd.DataFrame(data={'Date':pd.to_datetime(df.InvoiceDate).dt.date,
                                    'Total price':df.Quantity*df.UnitPrice})
    general_trend = general_trend.groupby("Date")["Total price"].sum()
    general_trend = pd.DataFrame(general_trend)

    rolling_days = general_trend.copy()
    rolling_days['Mean price'] = rolling_days["Total price"].rolling(window=30).mean() 
    rolling_days.drop(['Total price'], axis=1, inplace=True)

    return general_trend, rolling_days #[0], [1]


# Description: Number of new customers each month
# Input:
# 1. File
# 2. start date
# 3. end date
# Output:
# Date | Number of customers
def new_customers(file, start, date):
    df = pd.read_csv(file, index_col=0)
    df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate)
    df = df.loc[df['InvoiceDate'].between(start, end)]
    number_customers = df.groupby(df["InvoiceDate"].dt.to_period('M'))["CustomerID"].nunique()
    number_customers = pd.DataFrame(data=number_customers).reset_index()
    number_customers["Date"] = number_customers.InvoiceDate.dt.to_timestamp()
    number_new_customers = []
    customers_seen = []
    for month in df["InvoiceDate"].dt.to_period('M').unique():
        customers = df[df["InvoiceDate"].dt.to_period('M') == month].CustomerID.unique()
        count=0
        for customer in customers:
            if customer not in customers_seen:
                count+=1
                customers_seen.append(customer)
        number_new_customers.append((month,count))
    number_new_customers = pd.DataFrame(number_new_customers,columns=["Date","New customers"])
    number_new_customers.Date = number_new_customers.Date.dt.to_timestamp()
    return number_new_customers

def daytime_encoder(date):
    if (date.hour >= 5)&(date.hour < 8):
        return "Early morning"
    elif (date.hour >= 8)&(date.hour < 11):
        return "Morning"
    elif (date.hour >= 11)&(date.hour < 13):
        return "Late morning"
    elif (date.hour >= 13)&(date.hour < 14):
        return "Early afternoon"
    elif (date.hour >= 14)&(date.hour < 15):
        return "Afternoon"
    elif (date.hour >= 15)&(date.hour < 17):
        return "Late afternoon"
    elif (date.hour >= 17)&(date.hour < 21):
        return "Evening"
    else:
        return date.hour


# Description: Number of transactions for each day time
# Input:
# 1. File
# Output:
# DayTime | Number of Transactions
def trasaction_per_daytime(file):    
    df = pd.read_csv(file)
    df['InvoiceDate'] = df['InvoiceDate'].map(daytime_encoder)
    group = df.groupby(['InvoiceDate'], as_index=False).count()
    df_daytime = pd.DataFrame()
    df_daytime['daytime'] = group['InvoiceDate']
    df_daytime['transaction'] = group['InvoiceNo']    
    return df_daytime