# Imports
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import collections

from utils.misc import load_data, make_grid


# Functions
def update_time_selector(time_selector):
	st.session_state.time_selector = time_selector

def generate_plots(time_selector):
	dict_map_selected_time = {'Day': 'Date', 'Week': 'Week', 'Month': 'Month-Year'}
	selected_time = dict_map_selected_time[time_selector]
	df_plot = df.groupby(selected_time).agg(
		{
		'Calories':'mean', 
		'Weight':'mean', 
		'Steps':'mean', 
		'Workout':'count'
		}
		).reset_index()
	fig_weight_over_time = px.line(data_frame=df_plot.dropna(subset=[selected_time, 'Weight'], how='any'), x=selected_time, y='Weight').update_traces(mode='lines+markers')
	fig_calories_over_time = px.line(data_frame=df_plot.dropna(subset=[selected_time, 'Calories'], how='any'), x=selected_time, y='Calories').update_traces(mode='lines+markers')
	fig_steps_over_time = px.line(data_frame=df_plot.dropna(subset=[selected_time, 'Steps'], how='any'), x=selected_time, y='Steps').update_traces(mode='lines+markers')
	fig_workouts_over_time = px.bar(data_frame=df_plot.dropna(subset=[selected_time, 'Workout'], how='any'), x=selected_time, y='Workout')

	return fig_weight_over_time, fig_calories_over_time, fig_steps_over_time, fig_workouts_over_time 


# Prepare data
df = load_data()
df_workouts_per_week = df.groupby('Week').agg({'Workout':'count'}).reset_index()

list_exercises = ','.join(df['Workout'].dropna().to_list()).replace(' ','').split(',')
counts_exercises = collections.Counter(list_exercises)
df_popular_exercises = pd.DataFrame.from_dict(counts_exercises, orient='index').reset_index().rename(columns={'index':'Exercise', 0:'Occurrence'}).sort_values('Occurrence', ascending=False)

# Content
if 'time_selector' not in st.session_state:
	st.session_state.time_selector = 'Day'

st.set_page_config(page_title="Overview")

st.markdown("# Overview")
st.sidebar.header("Overview")

time_selector = st.radio(
	label='Time Range Selector', options=['Day', 'Week', 'Month'], horizontal=True,
	)
update_time = st.button('Update', on_click=update_time_selector,
	kwargs={'time_selector':time_selector}
    )

fig_weight_over_time, fig_calories_over_time, fig_steps_over_time, fig_workouts_over_time = generate_plots(st.session_state.time_selector)

col1, col2 = st.columns(2, gap='small')
col3, col4 = st.columns(2, gap='small')

with col1:
	st.plotly_chart(fig_weight_over_time, use_container_width
		=True)

with col2:
	st.plotly_chart(fig_calories_over_time, use_container_width
		=True)

with col3:
	st.plotly_chart(fig_steps_over_time, use_container_width
		=True)

with col4:
	st.plotly_chart(fig_workouts_over_time, use_container_width
		=True)

st.dataframe(df_popular_exercises.reset_index(drop=True), use_container_width=True)