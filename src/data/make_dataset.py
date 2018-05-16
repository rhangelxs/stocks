# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from src.data.get_stocks import fetch_quandl
from src.features import build_features

import pandas as pd

from src.features.build_features import generate_daily_return, fix_datetime


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
	""" Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
	logger = logging.getLogger(__name__)

	symbols = ['AAPL', 'GOOG', 'FB']
	# Fetch
	for symbol in symbols:
		fetch_quandl(symbol, output_filepath="data/external")

	# Process
	datasets = []
	for symbol in symbols:
		df = pd.read_csv("data/external/%s.csv" % symbol)
		df = fix_datetime(df)
		df = generate_daily_return(df)
		df.to_csv("data/interim/%s.csv" % symbol)
		datasets.append(df)

	# Combine (reduce step)
	data = pd.concat(datasets)
	data.reset_index().drop('index', 1, errors="ignore")
	data.set_index("Date", inplace=True)
	data.to_csv("data/processed/stocks.csv")



	logger.info('making final data set from raw data')

if __name__ == '__main__':
	log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	logging.basicConfig(level=logging.INFO, format=log_fmt)

	# not used in this stub but often useful for finding various files
	project_dir = Path(__file__).resolve().parents[2]

	# find .env automagically by walking up directories until it's found, then
	# load up the .env entries as environment variables
	load_dotenv(find_dotenv())

	main()
