import streamlit as st
from utils.data_f import get_data, get_classdata
from utils.assignments_f import plot_assignments_stacked, plot_assignments_default, plot_altair_line_chart_assignments, get_assignments_data_all

st.set_page_config(layout="wide")
df = get_data()

classList = df['Class'].unique().tolist()
with st.sidebar:
    chosen_class = st.selectbox(label='Choose a class', options=classList)

    input_filter_term = st.multiselect('Filter by term',
                                       options=['T1', 'T2', 'T3', 'T4'],
                                       default=['T1', 'T2', 'T3', 'T4'])

df = df[df['Term'].isin(input_filter_term)]

classdata = get_classdata(df, chosen_class, input_filter_term)

assignments_data_all = get_assignments_data_all(
    df, ['Term', 'Class', 'Hall', 'Program', 'Year', 'Student leadership'])

assignments_data_single = assignments_data_all[assignments_data_all['Class'] ==
                                               chosen_class]

assignments_groupby_input_stacked = st.selectbox(
    label='Compare by',
    options=['Program', 'Year', 'Hall', 'Student leadership'],
    index=0,
    key='assignments_groupby_input_stacked')

left_one, right_one = st.columns(2)
all_assignments_chart_stacked = plot_assignments_stacked(
    assignments_data_all, assignments_groupby_input_stacked)

single_assignments_chart_stacked = plot_assignments_stacked(
    assignments_data_single, assignments_groupby_input_stacked)

with left_one:
    st.altair_chart(all_assignments_chart_stacked, use_container_width=True)

with right_one:
    st.altair_chart(single_assignments_chart_stacked, use_container_width=True)

left_two, right_two = st.columns(2)

with left_two:
    assignments_groupby_input_default = st.selectbox(
        label='Compare by',
        options=['Program', 'Year', 'Hall', 'Student leadership'],
        index=0,
        key='assignments_groupby_input_default')

with right_two:
    assignments_filter_input_default = st.selectbox(
        label='Filter assignments',
        options=[
            'ASG_Complete', 'ASG_Complete/No Credit', 'ASG_Incomplete',
            'ASG_Late', 'ASG_Late complete', 'ASG_Not turned in',
            'ASG_Turned in/Not graded'
        ])

all_assignments_chart_default = plot_assignments_default(
    assignments_data_all, assignments_groupby_input_default,
    assignments_filter_input_default)

single_assignments_chart_default = plot_assignments_default(
    assignments_data_single, assignments_groupby_input_default,
    assignments_filter_input_default)

with left_two:
    st.altair_chart(all_assignments_chart_default)

with right_two:
    st.altair_chart(single_assignments_chart_default)

left_three, right_three = st.columns(2)

with left_three:
    assignments_lineChart_splitby_input = st.selectbox(
        label='Split by assignment status?', options=['Yes', 'No'])

with right_three:
    assignments_lineChart_aggFunc_input = st.selectbox(
        label='Aggregate function', options=['mean', 'median', 'sum'])

all_assignments_lineChart = plot_altair_line_chart_assignments(
    assignments_data_all, 'Term', 'value', assignments_lineChart_aggFunc_input,
    assignments_lineChart_splitby_input)

single_assignments_lineChart = plot_altair_line_chart_assignments(
    assignments_data_single, 'Term', 'value',
    assignments_lineChart_aggFunc_input, assignments_lineChart_splitby_input)

with left_three:
    st.altair_chart(all_assignments_lineChart, use_container_width=True)

with right_three:
    st.altair_chart(single_assignments_lineChart, use_container_width=True)