import streamlit as st
import boto3
import pandas as pd

from datetime import datetime


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
	df['Date'] = pd.to_datetime(df['Date'], format="%Y/%m/%d") # .astype(datetime)
	df['Week'] = df['Week'].fillna(method='ffill')
	df['Month-Year'] = df['Date'].dt.to_period('M').astype('str')
	# df['Month-Year'] = pd.to_datetime(df['Date']).dt.to_period('M').astype('str')

	return df

def load_file_from_s3(bucket_name: str, file_name: str) -> bytes:
	"""
	Load file from an s3 bucket

	Parameters
	----------
	bucket_name : str
	    Name of s3 bucket
	file_name : str
		Name of file in s3 bucket
	
	Returns
	-------
	data : bytes
		Bytes of data from s3 bucket
	"""

	s3 = boto3.client('s3')

	try:
		obj = s3.get_object(Bucket=bucket_name, Key=file_name)
		data = obj['Body'].read()
	except s3.exceptions.NoSuchBucket as e:
		st.error(f"Bucket {bucket_name} does not exist.")
		raise
	except s3.exceptions.NoSuchKey as e:
		st.error(f"File {file_name} does not exist in bucket {bucket_name}.")
		raise
	except Exception as e:
		st.error("An error occurred while try to load data from s3: {e}")
		raise
	
	return data


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

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')
