import streamlit as st
from utils.traffic_lights_helper import plot_trafficLights_stacked, plot_traffic_meta, get_filtered_traffic_data
from utils.data_load import decrypt_data
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Traffic lights: all classes',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

df_wide_2122 = decrypt_data('data/21_22/traffic/wide_traffic_2122.csv')
df_long_2122 = decrypt_data('data/21_22/traffic/long_traffic_2122.csv')
df_wide_2223 = decrypt_data('data/22_23/traffic_lights/wide_traffic_lights_2223.csv')
df_long_2223 = decrypt_data('data/22_23/traffic_lights/long_traffic_lights_2223.csv')

df_wide = df_wide_2122 if academic_year == '2021/2022' else df_wide_2223
df_long = df_long_2122 if academic_year == '2021/2022' else df_long_2223

st.markdown('# Traffic lights: all classes')

left_col, middle_col, right_col = st.columns(3)
with left_col:
    traffic_drilldown = st.selectbox(
        label='Group traffic lights by',
        options=['Class', 'Hall', 'Term', 'Program', 'Year', 'Advisors'],
        key='traffic_drilldown')

with middle_col:
    filter_traffic_years = st.multiselect(
        label='Filter years',
        options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        key='filter_traffic_years')

with right_col:
    filter_traffic_terms = st.multiselect(label='Filter terms',
                                          options=['T1', 'T2', 'T3', 'T4'],
                                          default=['T1', 'T2', 'T3', 'T4'],
                                          key='filter_traffic_terms')

filtered_data_long = get_filtered_traffic_data(df_long, filter_traffic_years,
                                               filter_traffic_terms)

if (len(filter_traffic_years) == 0 or len(filter_traffic_terms) == 0):
    st.error('Choose at least one year and/or term')
    st.stop()

tab_traffic_stacked, tab_single_traffic = st.tabs(
    ['All traffic lights', 'Single traffic light'])

with tab_traffic_stacked:
    all_traffic_chart_stacked = plot_trafficLights_stacked(
        filtered_data_long, traffic_drilldown)

    st.markdown(
        '## Comparison of traffic lights as a percentage of total, grouped by {}'
        .format(traffic_drilldown))

    st.info(
        'Hover over the stacked bar chart below with your cursor to see the corresponding number of traffic lights belonging to each category.'
    )
    st.info(
        'Use to mouse scroll wheel to zoom in and out; double-click to reset zoom to default.'
    )

    st.altair_chart(all_traffic_chart_stacked, use_container_width=True)

with tab_single_traffic:
    st.markdown('## Single traffic light drilldown, grouped by {}'.format(
        traffic_drilldown))

    one, two = st.columns(2)
    with one:
        traffic_aggfunction = st.selectbox(label='Aggregate function',
                                           options=['mean', 'median', 'sum'],
                                           key='traffic_aggfunction')

    with two:
        traffic_single_selection = st.selectbox(
            label='Traffic light',
            options=['Green', 'Praise', 'Orange', 'Red'],
            key='traffic_single_selection')

    filtered_data_wide = get_filtered_traffic_data(df_wide,
                                                   filter_traffic_years,
                                                   filter_traffic_terms)

    single_traffic_chart = plot_traffic_meta(filtered_data_wide,
                                             traffic_drilldown,
                                             traffic_single_selection,
                                             traffic_aggfunction)

    st.altair_chart(single_traffic_chart, use_container_width=True)
