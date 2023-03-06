import pandas as pd


def load_data():
	"""
	Load the fitness data and format table

	Reads in fitness_data.csv from data folder and formats fields for use in app (remove empty columns, fill values for unmerged cells, add a 'Month-Year' field)

	Returns
	-------
	df : pd.DataFrame

	"""
	df = pd.read_csv('data/fitness_data.csv')
	df = df.drop(columns=[c for c in df.columns if c.startswith('Unnamed: ')])  # remove empty non-data columns
	df['Week'] = df['Week'].fillna(method='ffill')
	df['Month-Year'] = pd.to_datetime(df['Date']).dt.to_period('M').astype('str')

	return df
