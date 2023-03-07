import streamlit as st
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

def make_grid(n_cols, n_rows):
	"""
	Make a generic grid (n_cols x n_rows) via a streamlit container

	Parameters
	----------
	n_cols : int
	    Number of columns in grid
	n_rows : int
	    Number of rows in grid

	Returns
	-------
	grid : streamlit container
	"""

	grid = [0]*n_cols

	for i in range(n_cols):
		with st.container():
			grid[i] = st.columns(n_rows)

	return grid
