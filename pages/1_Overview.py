# Imports
import streamlit as st
import pandas as pd
import numpy as np
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

	_df = df[(df['Date'] >= np.datetime64(date_start_input)) & (df['Date'] <= np.datetime64(date_end_input))]
	df_plot = _df.groupby(selected_time).agg(**{
		'Calories': pd.NamedAgg(column='Calories', aggfunc='mean'),
		'Calories_std': pd.NamedAgg(column='Calories', aggfunc='std'),
		'Weight': pd.NamedAgg(column='Weight', aggfunc='mean'),
		'Weight_std': pd.NamedAgg(column='Weight', aggfunc='std'),
		'Steps': pd.NamedAgg(column='Steps', aggfunc='mean'),
		'Steps_std': pd.NamedAgg(column='Steps', aggfunc='std'),
		'Workout': pd.NamedAgg(column='Workout', aggfunc='count')
		}
		).reset_index()

	fig_weight_over_time = px.line(
		data_frame=df_plot.dropna(subset=[selected_time, 'Weight'], how='any'), x=selected_time, y='Weight', error_y='Weight_std'
		).update_traces(mode='lines+markers')
	fig_calories_over_time = px.line(
		data_frame=df_plot.dropna(subset=[selected_time, 'Calories'], how='any'), x=selected_time, y='Calories', error_y='Calories_std'
		).update_traces(mode='lines+markers')
	fig_steps_over_time = px.line(
		data_frame=df_plot.dropna(subset=[selected_time, 'Steps'], how='any'), x=selected_time, y='Steps', error_y='Steps_std'
		).update_traces(mode='lines+markers')
	fig_workouts_over_time = px.bar(
		data_frame=df_plot.dropna(subset=[selected_time, 'Workout'], how='any'), x=selected_time, y='Workout'
		)

	for fig in [fig_weight_over_time, fig_calories_over_time, fig_steps_over_time, fig_workouts_over_time]:
		fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True)
		fig.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', mirror=True)

	return fig_weight_over_time, fig_calories_over_time, fig_steps_over_time, fig_workouts_over_time, df_plot

def generate_metrics(df):

    col1, col2, col3 = st.columns(3, gap='large')
    col1.metric(
        label='Weight', 
        value=f"{df['Weight'].dropna().iloc[-1]} lb", 
        delta=f"{np.round(df['Weight'].dropna().iloc[-1]-df['Weight'].dropna().iloc[0], 1)} lb", 
        delta_color='inverse'
        )
    col2.metric(
        label='Calories (mean)', 
        value=f"{int(df['Calories'].mean().round())}", 
        )
    col3.metric(
        label='Steps (mean)', 
        value=f"{int(df['Steps'].mean().round())}", 
        )

    return None


# Prepare data
df = load_data()
df_workouts_per_week = df.groupby('Week').agg({'Workout':'count'}).reset_index()

list_exercises = ','.join(df['Workout'].dropna().to_list()).replace(' ','').split(',')
counts_exercises = collections.Counter(list_exercises)
df_popular_exercises = pd.DataFrame.from_dict(counts_exercises, orient='index').reset_index().rename(columns={'index':'Exercise', 0:'Occurrence'}).sort_values('Occurrence', ascending=False)

# Content
if 'time_selector' not in st.session_state:
	st.session_state.time_selector = 'Day'

st.set_page_config(page_title='Overview', layout='wide')

st.markdown("# Overview")
st.sidebar.header("Overview")

## Widgets
colA, colB, colC = st.columns(3, gap='large')
with colA:
	time_selector = st.radio(
		label='Time Range Selector', options=['Day', 'Week', 'Month'], horizontal=True,
		label_visibility='hidden'
		)
with colB:
	date_start_input = st.date_input(
		label='Start Date', value=pd.to_datetime(df['Date']).min(), min_value=pd.to_datetime(df['Date']).min(), max_value=pd.to_datetime(df['Date']).max()
		)
with colC:
	date_end_input = st.date_input(
		label='End Date', value=pd.to_datetime(df['Date']).max(), min_value=pd.to_datetime(df['Date']).min(), max_value=pd.to_datetime(df['Date']).max()
		)
update_time = st.button('Update', on_click=update_time_selector,
	kwargs={'time_selector':time_selector}
    )

## Figures and Data
fig_weight_over_time, fig_calories_over_time, fig_steps_over_time, fig_workouts_over_time, df_plot = generate_plots(st.session_state.time_selector)

## Display Metrics
generate_metrics(df_plot)

## Display Figures
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