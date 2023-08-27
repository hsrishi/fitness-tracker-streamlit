# Imports
import streamlit as st
import pandas as pd

from utils.misc import load_data_s3, convert_df

# Content
st.set_page_config(page_title="Raw Data")

st.markdown("# Raw Data")
st.sidebar.header("Raw Data")

df = load_data_s3('fitness-data-hr', 'fitness_data.csv')
st.dataframe(df, use_container_width=True)

# Download button
csv_r = convert_df(df)
st.download_button(
    label='Download as CSV',
    data=csv_r,
    file_name='fitness_raw.csv',
    mime='test/csv'
    )
