import streamlit as st
from utils.data_f import get_data, get_classdata
from utils.absences_f import plot_absences

st.set_page_config(layout="wide")

# df = get_data('data/data.csv')
df = get_data()

classList = df['Class'].unique().tolist()
with st.sidebar:
    chosen_class = st.selectbox(label='Choose a class', options=classList)

    input_filter_term = st.multiselect('Filter by term',
                                       options=['T1', 'T2', 'T3', 'T4'],
                                       default=['T1', 'T2', 'T3', 'T4'])

df = df[df['Term'].isin(input_filter_term)]

classdata = get_classdata(df, chosen_class, input_filter_term)

left_one, right_one = st.columns(2)

with left_one:
    input_assignments_aggregateFunction = st.selectbox(
        'Assignments : Aggregate function', options=['mean', 'median', 'sum'])

with right_one:
    absences_splitby_input = st.selectbox(
        label='Split by',
        options=['Program', 'Year', 'Hall', 'Student leadership'])

all_absences_chart = plot_absences(df, absences_splitby_input,
                                   input_assignments_aggregateFunction, 450,
                                   250)
single_absence_chart = plot_absences(classdata, absences_splitby_input,
                                     input_assignments_aggregateFunction, 450,
                                     250)

with left_one:
    st.altair_chart(all_absences_chart)

with right_one:
    st.altair_chart(single_absence_chart)