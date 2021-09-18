import pygsheets
import pandas as pd
from transactions import get_transctions
import os

url_shop_metrics = os.environ.get('URL_REPORTS')
url_provider_metrics = os.environ.get('URL_COUNT')
creds_shop = {'user': os.environ.get('BASIC_LOGIN_SHOP'), 'pass': os.environ.get('BASIC_PASS_SHOP')}
creds_provider = {'user': os.environ.get('BASIC_LOGIN_COUNT'), 'pass': os.environ.get('BASIC_PASS_COUNT')}

transactions_info = get_transctions(url_provider_metrics, creds=creds_provider)
print(transactions_info)
# print(get_transctions(url_shop_metrics, creds=creds_shop))

#authorization
gc = pygsheets.authorize(service_file='creds.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
## ALL TRANSACTIONS

df['date_from'] = [transactions_info['report_params']['from']]
df['date_to'] = [transactions_info['report_params']['to']]
df['successful_count'] = [transactions_info['all']['successful_count']]
df['failed_count'] = [transactions_info['all']['failed_count']]
df['ratio'] = [transactions_info['ratio']]

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Transactions')

print(dir(sh[0]))
#select the first sheet
wks = sh[0]

#update the first sheet with df, starting at cell B2.

wks.set_dataframe(df,(2,1))