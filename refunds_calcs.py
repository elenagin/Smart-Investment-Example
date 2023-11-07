"""
Our team has also been asked to automate the calculation of the amounts to refund to customers that want
to cancel their investment. To do so we need a script that does the following:
Uploads all files of the stocks that compose the fund and calculates the daily accumulated gain/loss in percentage. 
The files will be the same as in part 1.
Uploads a file called users.csv with the following columns: user_id, investment_open_date, investment_close_date, 
amount_invested
The script should output a file called users_refund.csv with the same columns as the previous one plus another one 
called amount_refund. The amount to be refunded is calculated with the following formula: amount_invested * (1 + 
"cumulated performance on close"/100 - "cumulated performance on open"/100)
The program will receive a path as a parameter that will be the folder where all files should be read from and 
where the output file should be written to.
We assume investors do not do partial openings or closings, that the opening and close dates will be within the 
dates of the provided files and that the open and close dates will be at least 1 day appart.
The dates in the investors file will be in format YYYY-MM-DD and "." as decimal separator and no thousands separator.
You need to create your own test data for the investors file.

"""

#Importing packages
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

def pct_change_reset(series):
    return series.pct_change().where(series.notna(), 0)

def cumsum_change_reset(series):
    return series.cumsum().where(series.notna(), 0)


#Importing dataframes
df_aapl = pd.concat([pd.read_csv('path_to_folder/AAPL_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/AAPL_1.csv', parse_dates=['Date'])], ignore_index=True)
df_amzn = pd.concat([pd.read_csv('path_to_folder/AMZN_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/AMZN_1.csv', parse_dates=['Date'])], ignore_index=True)
df_googl = pd.concat([pd.read_csv('path_to_folder/GOOGL_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/GOOGL_1.csv', parse_dates=['Date'])], ignore_index=True)
df_meta = pd.concat([pd.read_csv('path_to_folder/META_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/META_1.csv', parse_dates=['Date'])], ignore_index=True)
df_nflx = pd.concat([pd.read_csv('path_to_folder/NFLX_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/NFLX_1.csv', parse_dates=['Date'])], ignore_index=True)
df_spx = pd.concat([pd.read_csv('path_to_folder/SPX_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/SPX_1.csv', parse_dates=['Date'])], ignore_index=True)
df_tsla = pd.concat([pd.read_csv('path_to_folder/TSLA_2.csv', parse_dates=['Date'], ), pd.read_csv('path_to_folder/TSLA_1.csv', parse_dates=['Date'])], ignore_index=True)

#Parsing dates
df_aapl['Date'] = pd.to_datetime(df_aapl['Date'], utc=True).dt.date
df_aapl['Date'] = pd.to_datetime(df_aapl['Date'], format = '%Y%m')
df_amzn['Date'] = pd.to_datetime(df_amzn['Date'], utc=True).dt.date
df_amzn['Date'] = pd.to_datetime(df_amzn['Date'], format = '%Y%m')
df_googl['Date'] = pd.to_datetime(df_googl['Date'], utc=True).dt.date
df_googl['Date'] = pd.to_datetime(df_googl['Date'], format = '%Y%m')
df_meta['Date'] = pd.to_datetime(df_meta['Date'], utc=True).dt.date
df_meta['Date'] = pd.to_datetime(df_meta['Date'], format = '%Y%m')
df_nflx['Date'] = pd.to_datetime(df_nflx['Date'], utc=True).dt.date
df_nflx['Date'] = pd.to_datetime(df_nflx['Date'], format = '%Y%m')
df_tsla['Date'] = pd.to_datetime(df_tsla['Date'], utc=True).dt.date
df_tsla['Date'] = pd.to_datetime(df_tsla['Date'], format = '%Y%m')
df_spx['Date'] = pd.to_datetime(df_spx['Date'], utc=True).dt.date
df_spx['Date'] = pd.to_datetime(df_spx['Date'], format = '%Y%m')

fund_composition = {
    'META': 0.15,
    'NFLX': 0.10,
    'AAPL': 0.25,
    'TSLA': 0.15,
    'GOOGL': 0.20,
    'AMZN': 0.15,
    'SPX': 1,
}

# Create a new dataframe for all fund
df_aapl['Ticker'] = 'AAPL'
df_amzn['Ticker'] = 'AMZN'
df_googl['Ticker'] = 'GOOGL'
df_meta['Ticker'] = 'META'
df_nflx['Ticker'] = 'NFLX'
df_tsla['Ticker'] = 'TSLA'
# df_spx['Ticker'] = 'SPX'
df_all = pd.concat([df_aapl, df_amzn, df_googl, df_meta, df_nflx, df_tsla], ignore_index=True)
df_all['Week'] = pd.to_datetime(df_all['Date']).dt.isocalendar().week
df_all['fund_composition'] = df_all['Ticker'].map(fund_composition)
df_all = df_all.sort_values(by=['Ticker', 'Date'])
df_all['gain_loss_percentage'] = df_all.groupby('Ticker')['Close'].transform(pct_change_reset) * 100
df_all['accumulated_gain_loss'] = df_all.groupby('Ticker')['gain_loss_percentage'].transform(cumsum_change_reset)

# print(df_all[df_all['Ticker'] == 'AAPL'][['Date', 'Ticker', 'Close', 'gain_loss_percentage', 'accumulated_gain_loss']].head(20))
# print(df_all[df_all['Ticker'] == 'AMZN'][['Date', 'Ticker', 'Close', 'gain_loss_percentage', 'accumulated_gain_loss']])

data = {
    'user_id': [1, 2],
    'investment_open_date': ['2022-12-02', '2022-12-02'],
    'investment_close_date': ['2023-10-20', '2022-12-19'],
    'amount_invested': [1000, 1000]
}
df_users = pd.DataFrame(data)
df_users_closed = pd.DataFrame(data)
df_users_open = pd.DataFrame(data)
df_fund_users = pd.DataFrame()

df_users.to_csv('path_to_folder/users.csv', index=False)

# Read user file
df_users = pd.read_csv('path_to_folder/users.csv')
df_all['Date'] = pd.to_datetime(df_all['Date'])


df_users_closed['Date'] = pd.to_datetime(df_users['investment_close_date'])

for fund in fund_composition:
    temp = 0
    if fund != 'SPX':
        df_merged = pd.merge(df_users_closed, df_all[df_all['Ticker'] == fund], on='Date', how='left')
        df_merged = df_merged.drop(['High', 'Low', 'Week', 'Stock Splits', 'Dividends', 'Date', 'Volume'], axis=1)
        df_fund_users = pd.concat([df_fund_users, df_merged], ignore_index=True)
        temp += df_fund_users['accumulated_gain_loss'].iloc[-1]
        
# print(df_fund_users.sort_values(by=['user_id', 'investment_close_date']))


df_fund_users['product_column'] = df_fund_users['fund_composition'] * df_fund_users['accumulated_gain_loss']
# user_sums = df_fund_users.groupby('user_id')['product_column'].sum()
# print(user_sums)


# filtered_rows = (df_fund_users['investment_close_date'] == '2022-12-19') & (df_fund_users['user_id'] == 2)
# cumulated_performance_on_close = df_fund_users.loc[filtered_rows, 'product_column'].sum()
# print("CLOSE", cumulated_performance_on_close)


df_users_refund = df_users_closed
df_users_refund['amount_refund'] = df_users_refund['amount_invested'] * (1 + df_fund_users.groupby('user_id')['product_column'].sum()[df_users_refund['user_id']]/100 - 0.092/100)
print(df_users_refund)


"""
filtered_rows = (df_fund_users['investment_open_date'] == '2022-12-02') & (df_fund_users['user_id'] == 2)
cumulated_performance_on_open = df_fund_users.loc[filtered_rows, 'product_column'].sum()
print("OPEN", cumulated_performance_on_open)"""





# filtered_rows = (df_fund_users['investment_open_date'] == '2022-12-02') & (df_fund_users['user_id'] == 2)
# cumulated_performance_on_open = df_fund_users.loc[filtered_rows, 'product_column'].sum()

# print(user_sums[2])

# print("cumulated_performance_on_open", cumulated_performance_on_open)
# print("cumulated_performance_on_close", cumulated_performance_on_close)

#df_users['amount_refund'] = df_users['amount_invested'] * (1 + cumulated_performance_on_close/100 - cumulated_performance_on_open/100)

# print(df_users)
pd.DataFrame(df_users).to_csv('path_to_folder/users_refund.csv', index=False)