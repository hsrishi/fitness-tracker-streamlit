# Imports
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import collections

from utils.misc import load_data


# Prepare data
df = load_data()
df_workouts_per_week = df.groupby('Week').agg({'Workout':'count'}).reset_index()

list_exercises = ','.join(df['Workout'].dropna().to_list()).replace(' ','').split(',')
counts_exercises = collections.Counter(list_exercises)
df_popular_exercises = pd.DataFrame.from_dict(counts_exercises, orient='index').reset_index().rename(columns={'index':'Exercise', 0:'Occurrence'}).sort_values('Occurrence', ascending=False)

# Content
st.set_page_config(page_title="Overview")

st.markdown("# Overview")
st.sidebar.header("Overview")

# Figures
# Weight over time
fig_weight_over_time = px.line(
	data_frame=df.dropna(subset=['Date', 'Weight'], how='any'), 
	x='Date',
	y='Weight'  # , 'Calories'
	).update_traces(mode='lines+markers')

fig_calories_over_time = px.line(
	data_frame=df.dropna(subset=['Date', 'Weight'], how='any'), 
	x='Date',
	y='Calories'  # , 'Calories'
	).update_traces(mode='lines+markers')

fig_steps_over_time = px.line(
	data_frame=df.dropna(subset=['Date', 'Weight'], how='any'), 
	x='Date',
	y='Steps'  # , 'Calories'
	).update_traces(mode='lines+markers')

fig_workouts_over_time = px.bar(
	data_frame=df.groupby('Date').agg({'Workout':'count'}).reset_index(),
	x='Date',
	y='Workout'
	)

fig_weight_over_time
fig_calories_over_time
fig_steps_over_time
fig_workouts_over_time
df_popular_exercises