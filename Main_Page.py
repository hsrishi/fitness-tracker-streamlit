# Imports
import streamlit as st
import pandas as pd
import numpy as np

from utils.misc import load_data, convert_df

# Functions
def get_summary_df():
    """
    Prepare summary dataframe with weekly stats
    """

    df = load_data()

    df_s = df.groupby(['Week']).agg(**{
        'Weight': pd.NamedAgg(column='Weight', aggfunc='mean'),
        'Calories': pd.NamedAgg(column='Calories', aggfunc='mean'),
        'Protein': pd.NamedAgg(column='Calories', aggfunc='mean'),
        'Steps': pd.NamedAgg(column='Steps', aggfunc='mean'),
        'Steps (tot)': pd.NamedAgg(column='Steps', aggfunc='sum'),
        'Lifting Days': pd.NamedAgg(column='Workout', aggfunc='count'),
        'Conditioning Days': pd.NamedAgg(column='Conditioning (cal estimated using apps)', aggfunc='count'),
        }
        )
    df_s.index.name = 'Week'
    df_s = df_s.rename(columns={'Weight':'Weight (lb)', 'Protein':'Protein (g)'})
    df_s = df_s.round(1)  # .reset_index(drop=False)
    df_s['Weight Loss (lb)'] = df_s['Weight (lb)'].diff()

    col_order = [
        'Weight (lb)', 'Weight Loss (lb)', 'Steps (tot)',
        'Calories', 'Protein (g)',
        'Lifting Days', 'Conditioning Days', 'Steps'
        ]
    df_s = df_s[col_order]

    return df_s


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fitness Tracker",
        page_icon="👋",
    )
    # title/sidebar
    text = st.sidebar.title("Contents")
    title = st.title("Fitness Tracker")
    
    st.sidebar.success("Select a section from above.")

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

