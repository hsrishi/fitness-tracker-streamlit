# Imports
import streamlit as st
import pandas as pd

from utils.misc import load_data

# Content
st.set_page_config(page_title="Raw Data")

st.markdown("# Raw Data")
st.sidebar.header("Raw Data")

df = load_data()
st.dataframe(df, use_container_width=True)
