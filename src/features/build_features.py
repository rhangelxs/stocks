import pandas as pd
def fix_datetime(df):
	df['Date'] = pd.to_datetime(df['Date'])
	df = df.sort_values('Date')
	return df


def generate_daily_return(df):
	df['Return'] = (df['Close'].shift(1) - df['Close']) / df['Close']
	df['Return_raw'] = (df['Close'].shift(1) - df['Close'])
	df['AdjReturn'] = (df['AdjClose'].shift(1) - df['AdjClose']) / df['AdjClose']
	return df