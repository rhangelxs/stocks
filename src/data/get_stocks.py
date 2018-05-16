from pandas_datareader import data as web
import requests_cache

import datetime


def fetch_quandl(symbol, output_filepath):
	start = datetime.datetime(2009, 1, 1)
	end = datetime.datetime(2017, 12, 31)

	expire_after = datetime.timedelta(days=3)
	session = requests_cache.CachedSession(cache_name='cache', backend='sqlite', expire_after=expire_after)

	df = web.DataReader("WIKI/%s" % symbol, 'quandl', start, end, session=session)
	df['Stock'] = symbol
	df.to_csv("%s/%s.csv" % (output_filepath, symbol))

