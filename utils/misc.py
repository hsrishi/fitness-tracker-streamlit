import streamlit as st
import boto3
import pandas as pd

from datetime import datetime
from io import BytesIO


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
		st.error(f"An error occurred while try to load data from s3: {e}")
		raise
	
	return data


def read_file_as_df(data: bytes, file_name: str) -> pd.DataFrame:
	"""
	Read file (passed as bytes) as a pandas dataframe

	Parameters
	----------
	data : bytes
	    Bytes of data to read into dataframe
	file_name : str
		Name of file
	
	Returns
	-------
	df : pd.DataFrame
		Dataframe of data
	"""

	file_type = file_name.split('.')[-1]

	if file_type == 'csv':
		try:
			df = pd.read_csv(BytesIO(data))
		except Exception as e:
			st.error(f"An error occurred while trying to read file {file_name} as a csv: {e}")
			raise
	elif file_type in ['xls', 'xlsx']:
		try:
			df = pd.read_excel(BytesIO(data))
		except Exception as e:
			st.error(f"An error occurred while trying to read file {file_name} as an excel file: {e}")
			raise
	elif file_type in ['txt']:
		try:
			df = pd.read_table(BytesIO(data))
		except Exception as e:
			st.error(f"An error occurred while trying to read file {file_name} as a text file: {e}")
			raise
	else:
		st.error(f"File type {file_type} not supported.")
		raise Exception(f"File type {file_type} not supported.")

	return df


def load_data_s3(bucket_name: str, file_name: str) -> pd.DataFrame:
	"""
	Wrapper function for loading fitness data from s3 bucket and formatting table

	Parameters
	----------
	bucket_name : str
		Name of s3 bucket
	file_name : str
		Name of file in s3 bucket
	
	Returns
	-------
	df : pd.DataFrame
		Dataframe of data
	
	Example
	-------
	>>> df = load_data_s3('fitness-data-hr', 'fitness_data.csv')
	"""

	data = load_file_from_s3(bucket_name, file_name)
	df = read_file_as_df(data, file_name)

	df = df.drop(columns=[c for c in df.columns if c.startswith('Unnamed: ')])  # remove empty non-data columns
	df['Date'] = pd.to_datetime(df['Date']) # .astype(datetime)  # , format="%Y/%m/%d"
	df['Week'] = df['Week'].fillna(method='ffill')
	df['Month-Year'] = df['Date'].dt.to_period('M').astype('str')

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

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')
