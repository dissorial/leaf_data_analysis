import streamlit as st
from utils.traffic_lights_helper import plot_trafficLights_stacked, plot_traffic_meta, get_filtered_traffic_data
from utils.data_load import decrypt_data
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Traffic lights: single class',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

df_wide_2122 = decrypt_data('data/21_22/traffic/wide_traffic_2122.csv')
df_long_2122 = decrypt_data('data/21_22/traffic/long_traffic_2122.csv')
df_wide_2223 = pd.read_csv(
    'data/22_23/traffic_lights/wide_traffic_lights_2223.csv')
df_long_2223 = pd.read_csv(
    'data/22_23/traffic_lights/long_traffic_lights_2223.csv')

df_wide = df_wide_2122 if academic_year == '2021/2022' else df_wide_2223
df_long = df_long_2122 if academic_year == '2021/2022' else df_long_2223

st.markdown('# Traffic lights: single class')

left_col1, right_col3 = st.columns(2)

with left_col1:
    filter_traffic_years = st.multiselect(
        label='Filter years',
        options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        key='filter_traffic_years_single')

with right_col3:
    filter_traffic_terms = st.multiselect(label='Filter terms',
                                          options=['T1', 'T2', 'T3', 'T4'],
                                          default=['T1', 'T2', 'T3', 'T4'],
                                          key='filter_traffic_terms_single')

filtered_data_long = get_filtered_traffic_data(df_long, filter_traffic_years,
                                               filter_traffic_terms)

filtered_data_wide = get_filtered_traffic_data(df_wide, filter_traffic_years,
                                               filter_traffic_terms)

if (len(filter_traffic_years) == 0 or len(filter_traffic_terms) == 0):
    st.error('Choose at least one year and/or term')
    st.stop()

classList_long = filtered_data_long['Class'].unique().tolist()
classList_wide = filtered_data_wide['Class'].unique().tolist()
classlist = filtered_data_long['Class'].unique().tolist()

col1_left, col2_right = st.columns(2)

with col1_left:
    chosen_class = st.selectbox(label='Choose a class', options=classlist)

classdata_long = filtered_data_long[filtered_data_long['Class'] ==
                                    chosen_class]
classdata_wide = filtered_data_wide[filtered_data_wide['Class'] ==
                                    chosen_class]

with col2_right:
    traffic_split_input = st.selectbox(
        label='Split by',
        options=['Program', 'Year', 'Hall', 'Student leadership', 'Advisors'])

single_traffic_chart = plot_trafficLights_stacked(classdata_long,
                                                  traffic_split_input)

st.markdown(
    '## Comparison of traffic lights as a percentage of total for {}'.format(
        chosen_class))
st.altair_chart(single_traffic_chart, use_container_width=True)

st.markdown('## Single traffic light drilldown for {}'.format(chosen_class))
left_two, middle_two = st.columns(2)
with left_two:
    traffic_light_lineChart_input = st.selectbox(
        label='Traffic light',
        options=['Green', 'Praise', 'Orange', 'Red'],
        key='traffic_light_lineChart_input')

with middle_two:
    traffic_light_lineChart_aggfunction_input = st.selectbox(
        label='Aggregate function',
        options=['mean', 'median', 'sum'],
        key='traffic_light_lineChart_aggfunction_input')

signle_traffic_aggreagte = plot_traffic_meta(
    classdata_wide, traffic_split_input, traffic_light_lineChart_input,
    traffic_light_lineChart_aggfunction_input)

st.altair_chart(signle_traffic_aggreagte, use_container_width=True)
