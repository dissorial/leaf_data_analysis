import streamlit as st
from utils.grades_helper import grades_meta, get_filtered_grades_data, plot_altair_histogram
from utils.data_load import decrypt_data
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Grades: all classes',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

grades_2122 = decrypt_data('data/21_22/grades/grades_2122.csv')
grades_2223 = pd.read_csv('data/22_23/grades/grades_2223.csv')

grades_data = grades_2122 if academic_year == '2021/2022' else grades_2223

st.markdown('# Grades: all classes')

with st.expander('Grades legend (numerical vs oridnal)'):

    st.markdown('- A+ = 10')
    st.markdown('- A = 9')
    st.markdown('- A- = 8')
    st.markdown('- B+ = 7')
    st.markdown('- B = 6')
    st.markdown('- B- = 5')
    st.markdown('- C+ = 4')
    st.markdown('- C = 3')
    st.markdown('- C- = 2')
    st.markdown('- D = 1')

one, two, three, four = st.columns([1, 1, 2, 2])
with one:
    grades_drilldown = st.selectbox(label='Group by',
                                    options=[
                                        'Class', 'Hall', 'Term', 'Program',
                                        'Year', 'Student leadership',
                                        'Advisors'
                                    ],
                                    key='grades_drilldown')

with two:
    grades_aggfunction = st.selectbox(label='Aggregate function',
                                      options=['mean', 'median'],
                                      key='grades_aggfunction')

with three:
    filter_grades_years = st.multiselect(
        label='Filter years',
        options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        key='filter_grades_years')

with four:
    filter_grades_terms = st.multiselect(label='Filter terms',
                                         options=['T1', 'T2', 'T3', 'T4'],
                                         default=['T1', 'T2', 'T3', 'T4'],
                                         key='filter_grades_terms')

if (len(filter_grades_years) == 0 or len(filter_grades_terms) == 0):
    st.error('Choose at least one parameter in each filter')
    st.stop()

filtered_grades_data = get_filtered_grades_data(grades_data,
                                                filter_grades_years,
                                                filter_grades_terms)

tab_summary, tab_distribution = st.tabs(['Summary', 'Distribution'])

with tab_summary:
    st.markdown('## Comparison of {} of grades by {}'.format(
        grades_aggfunction, grades_drilldown))

    grades_v_classes_chart = grades_meta(filtered_grades_data,
                                         grades_drilldown, grades_aggfunction)
    st.altair_chart(grades_v_classes_chart, use_container_width=True)

with tab_distribution:
    st.markdown('## Distribution of grades')
    st.info(
        'Hover over the individual bars to show the number of instances (records) for that particular bar (intersection of X and Y axis).'
    )
    st.info(
        'If using a mouse (as opposed to a touchpad), use the scroll wheel to adjust the chart width. Double-click the chart to reset width to default.'
    )
    density_input = st.selectbox(label='Show as',
                                 options=['Histogram', 'Density plot'],
                                 key='density_input')

    grades_histogram_chart = plot_altair_histogram(filtered_grades_data,
                                                   density_input, 50)

    st.altair_chart(grades_histogram_chart, use_container_width=True)