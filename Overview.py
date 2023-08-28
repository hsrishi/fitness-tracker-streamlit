# Imports
import streamlit as st
import pandas as pd
import numpy as np

from utils.misc import load_data_s3, convert_df
from langchain.llms import OpenAI


# Functions
def get_summary_df():
    """
    Prepare summary dataframe with weekly stats
    """

    df = load_data_s3('fitness-data-hr', 'fitness_data.csv')

    df_s = df.groupby(['Week']).agg(**{
        'Weight': pd.NamedAgg(column='Weight', aggfunc='mean'),
        'Calories': pd.NamedAgg(column='Calories', aggfunc='mean'),
        'Protein': pd.NamedAgg(column='Protein (g)', aggfunc='mean'),
        'Steps': pd.NamedAgg(column='Steps', aggfunc='mean'),
        'Steps (tot)': pd.NamedAgg(column='Steps', aggfunc='sum'),
        'Lifting Days': pd.NamedAgg(column='Workout', aggfunc='count'),
        'Conditioning Days': pd.NamedAgg(column='Conditioning (cal estimated using apps)', aggfunc='count'),
        }
        )
    df_s.index.name = 'Week'
    df_s = df_s.rename(columns={'Weight':'Weight (lb)', 'Protein':'Protein (g)'})
    df_s = df_s.round(1)
    df_s['Steps'] = df_s['Steps'].round(0)
    df_s['Weight Loss (lb)'] = df_s['Weight (lb)'].diff().round(1)

    col_order = [
        'Weight (lb)', 'Weight Loss (lb)', 'Steps (tot)',
        'Calories', 'Protein (g)',
        'Lifting Days', 'Conditioning Days', 'Steps'
        ]
    df_s = df_s[col_order]

    return df_s


def generate_response(input_text):
    """
    Generate response from OpenAI
    """

    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    st.info(llm(input_text))


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fitness Tracker",
        page_icon="👋",
    )
    # title/sidebar
    text = st.sidebar.title("Contents")
    title = st.title("Fitness Tracker")
    
    st.sidebar.success("Select a section from above.")
    openai_api_key = st.sidebar.text_input('OpenAI API Key')

    # Prepare data
    df_s = get_summary_df()
    st.dataframe(df_s, use_container_width=True)
    st.write('*Fields represent means unless otherwise noted.')

    # Download button
    csv_s = convert_df(df_s)
    st.download_button(
        label='Download as CSV',
        data=csv_s,
        file_name='fitness_summary.csv',
        mime='test/csv'
        )
    
    # LLM chat interface
    with st.form('my_form'):
        text = st.text_area('Enter text:', 'Ask a question...')
        submitted = st.form_submit_button('Submit')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter an OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            generate_response(text)

