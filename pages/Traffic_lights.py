import streamlit as st
from utils.data_f import get_data, get_classdata
from utils.traffic_f import plot_single_traffic, plot_trafficLights, plot_altair_line_chart_traffic, get_traffic_data_all

st.set_page_config(layout="wide")
df = get_data('data/data.csv')

classList = df['Class'].unique().tolist()

with st.sidebar:
    chosen_class = st.selectbox(label='Choose a class', options=classList)

    input_filter_term = st.multiselect('Filter by term',
                                       options=['T1', 'T2', 'T3', 'T4'],
                                       default=['T1', 'T2', 'T3', 'T4'])

df = df[df['Term'].isin(input_filter_term)]

classdata = get_classdata(df, chosen_class, input_filter_term)
traffic_data_all = get_traffic_data_all(
    df, ['Term', 'Class', 'Hall', 'Program', 'Year', 'Student leadership'])
traffic_data_single = traffic_data_all[traffic_data_all['Class'] ==
                                       chosen_class]

traffic_split_input = st.selectbox(
    label='Split by',
    options=['Program', 'Year', 'Hall', 'Student leadership'])

left_one, right_one = st.columns(2)
all_traffic_chart = plot_trafficLights(traffic_data_all, traffic_split_input)
single_traffic_chart = plot_trafficLights(traffic_data_single,
                                          traffic_split_input)

all_traffic_line_chart = plot_altair_line_chart_traffic(
    traffic_data_all, 'Term', 'value', 'mean', traffic_split_input)

single_traffic_line_chart = plot_altair_line_chart_traffic(
    traffic_data_single, 'Term', 'value', 'mean', traffic_split_input)

with left_one:
    st.altair_chart(all_traffic_chart)
    st.altair_chart(all_traffic_line_chart, use_container_width=True)

with right_one:
    st.altair_chart(single_traffic_chart)
    st.altair_chart(single_traffic_line_chart, use_container_width=True)

left_two, middle_two, right_two = st.columns(3)
with left_two:
    traffic_light_lineChart_input = st.selectbox(
        label='Traffic light',
        options=['TRF_Green', 'TRF_Praise', 'TRF_Orange', 'TRF_Red'],
        key='traffic_light_lineChart_input')

with middle_two:
    traffic_light_lineChart_aggfunction_input = st.selectbox(
        label='Aggregate function',
        options=['mean', 'median', 'sum'],
        key='traffic_light_lineChart_aggfunction_input')

with right_two:
    traffic_light_lineChart_splitInput = st.selectbox(
        label='Split by',
        options=['Program', 'Year', 'Hall', 'Student leadership'],
        key='traffic_light_lineChart_splitInput')

all_traffic_aggregate = plot_single_traffic(
    df, traffic_light_lineChart_input,
    traffic_light_lineChart_aggfunction_input,
    traffic_light_lineChart_splitInput)

single_traffic_aggregate = plot_single_traffic(
    classdata, traffic_light_lineChart_input,
    traffic_light_lineChart_aggfunction_input,
    traffic_light_lineChart_splitInput)

left_three, right_three = st.columns(2)
with left_three:
    st.altair_chart(all_traffic_aggregate, use_container_width=True)

with right_three:
    st.altair_chart(single_traffic_aggregate, use_container_width=True)