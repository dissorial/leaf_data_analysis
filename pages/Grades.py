import streamlit as st
from utils.data_f import get_data, get_classdata
from utils.grades_f import plot_altair_line_chart, plot_altair_histogram, plot_class_charts

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

left_one, right_one = st.columns(2)

with left_one:
    grades_aggFunction_input = st.selectbox('Aggregate function for grades',
                                            options=['mean', 'median'])

with right_one:
    grades_overview_groupby_input = st.selectbox(
        label='Compare by',
        options=['Program', 'Year', 'Hall', 'Student leadership'],
        index=0)

height_class_grades = 100 if grades_overview_groupby_input != 'Hall' else 250

all_classes_chart = plot_class_charts(df, grades_overview_groupby_input,
                                      grades_aggFunction_input, 450,
                                      height_class_grades)
single_class_chart = plot_class_charts(classdata,
                                       grades_overview_groupby_input,
                                       grades_aggFunction_input, 450,
                                       height_class_grades)

with left_one:
    st.altair_chart(all_classes_chart)

with right_one:
    st.altair_chart(single_class_chart)

left_two, right_two = st.columns(2)

with left_two:
    grades_line_aggfunc_input = st.selectbox(label='Aggregate function',
                                             options=['mean', 'median'])
with right_two:
    grades_line_groupby_input = st.selectbox(label='Split by',
                                             options=[
                                                 'No grouping', 'Program',
                                                 'Year', 'Hall',
                                                 'Student leadership'
                                             ])

all_linechart_grades = plot_altair_line_chart(df, 'Term', 'Grade',
                                              grades_line_aggfunc_input,
                                              grades_line_groupby_input)

single_linechart_grade = plot_altair_line_chart(classdata, 'Term', 'Grade',
                                                grades_line_aggfunc_input,
                                                grades_line_groupby_input)

with left_two:
    st.altair_chart(all_linechart_grades, use_container_width=True)

with right_two:
    st.altair_chart(single_linechart_grade, use_container_width=True)

left_three, right_three = st.columns(2)

with left_three:
    hist_or_kde_input = st.selectbox(label='Plot charts below as',
                                     options=['Histogram', 'Density plot'])

with right_three:
    hist_kde_term = st.selectbox(label='Term',
                                 options=['All', 'T1', 'T2', 'T3', 'T4'])

all_classes_histogram_grades = plot_altair_histogram(
    df, hist_or_kde_input, hist_kde_term, 'Grade distribution of all classes')
single_class_histogram_grades = plot_altair_histogram(
    classdata, hist_or_kde_input, hist_kde_term,
    'Grade distribution for {}'.format(chosen_class))

with left_three:
    st.altair_chart(all_classes_histogram_grades, use_container_width=True)

with right_three:
    st.altair_chart(single_class_histogram_grades, use_container_width=True)
