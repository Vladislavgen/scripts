import pygsheets
import pandas as pd
from transactions import get_transctions
import os

url_shop_metrics = os.environ.get('URL_REPORTS')
url_provider_metrics = os.environ.get('URL_COUNT')
creds_shop = {'user': os.environ.get('BASIC_LOGIN_SHOP'), 'pass': os.environ.get('BASIC_PASS_SHOP')}
creds_provider = {'user': os.environ.get('BASIC_LOGIN_COUNT'), 'pass': os.environ.get('BASIC_PASS_COUNT')}

transactions_info = get_transctions(url_provider_metrics, creds=creds_provider)
# transactions_all = get_transctions(url_shop_metrics, creds=creds_shop)
gc = pygsheets.authorize(service_file='creds.json')

# Create empty dataframe
df = pd.DataFrame()

# Create a column
## ALL TRANSACTIONS

df['date_from'] = [transactions_info['report_params']['from'], transactions_info['report_params']['from'], transactions_info['report_params']['from']]
df['date_to'] = [transactions_info['report_params']['to'], transactions_info['report_params']['to'], transactions_info['report_params']['to']]
df['payment_method'] = ['credit_card', 'alternative', 'erip']
df['successful_count'] = [transactions_info['credit_card']['successful'], transactions_info['alternative']['successful'], transactions_info['erip']['successful']]
df['failed_count'] = [transactions_info['credit_card']['failed'], transactions_info['alternative']['failed'], transactions_info['erip']['failed']]
df['pending_count'] = [transactions_info['credit_card']['pending'], transactions_info['alternative']['pending'], transactions_info['erip']['pending']]
df['ratio'] = [transactions_info['credit_card']['ratio'], transactions_info['alternative']['ratio'], transactions_info['erip']['ratio']]

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Transactions')
#select the first sheet
wks = sh[0]

#update the first sheet with df, starting at cell B2.

wks.set_dataframe(df,(1,1))