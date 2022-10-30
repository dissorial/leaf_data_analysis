import streamlit as st
from utils.grades_helper import grades_meta, get_filtered_grades_data, plot_altair_histogram
from utils.data_load import decrypt_data
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Grades: single class',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

grades_2122 = decrypt_data('data/21_22/grades/grades_2122.csv')
grades_2223 = pd.read_csv('data/22_23/grades/grades_2223.csv')

grades_data = grades_2122 if academic_year == '2021/2022' else grades_2223

st.markdown('# Grades: single class')
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

st.markdown('## Filter and select')
one1, two2, three3 = st.columns([2, 1, 1])

available_classes = grades_data['Class'].unique().tolist()
with one1:
    grades_chosen_class = st.selectbox(label='Choose a class',
                                       options=available_classes,
                                       key='grades_chosen_class')

classData = grades_data[grades_data['Class'] == grades_chosen_class]

available_years_single_class = classData['Year'].unique().tolist()
with two2:
    filter_grades_years_single = st.multiselect(
        label='Filter years',
        options=available_years_single_class,
        default=available_years_single_class,
        key='available_years_single_class')

available_terms_single_class = classData['Term'].unique().tolist()

with three3:
    filter_grades_terms_single = st.multiselect(
        label='Filter term',
        options=available_terms_single_class,
        default=available_terms_single_class,
        key='available_terms_single_class')

if (len(filter_grades_years_single) == 0
        or len(filter_grades_terms_single) == 0):
    st.error('Choose at least one parameter in each filter')
    st.stop()

filtered_grades_data_single = get_filtered_grades_data(
    classData, filter_grades_years_single, filter_grades_terms_single)

tab_summary, tab_distribution = st.tabs(['Summary', 'Distribution'])

with tab_summary:
    st.markdown('## Comparison of grades for {}'.format(grades_chosen_class))
    leftcolmeta, rightcolmeta = st.columns(2)

    with leftcolmeta:
        grades_drilldown_single = st.selectbox(label='Split by',
                                               options=[
                                                   'Class', 'Hall', 'Term',
                                                   'Program', 'Year',
                                                   'Student leadership',
                                                   'Advisors'
                                               ],
                                               key='grades_drilldown_single',
                                               index=2)

    with rightcolmeta:
        grades_aggfunction_single = st.selectbox(
            label='Aggregate function',
            options=['mean', 'median'],
            key='grades_aggfunction_single')

    grades_v_classes_chart_single = grades_meta(filtered_grades_data_single,
                                                grades_drilldown_single,
                                                grades_aggfunction_single)

    st.altair_chart(grades_v_classes_chart_single, use_container_width=True)
    st.markdown(
        'When you split the chart below by various groups, interpret the results with caution. Since graded classes at LEAF are often small, different leadership positions, years, halls, and programs are often represented by a very small number of students. If a class has one RA (and no other student leaders), and you split the chart by student leadership positions, the result is a comparison between the average grade of that one RA student and the rest of the class.'
    )

with tab_distribution:
    st.markdown('## Distribution of grades for {}'.format(grades_chosen_class))

    st.info(
        'Hover over the individual bars to show the number of instances (records) for that particular bar (intersection of X and Y axis).'
    )
    st.info(
        'If using a mouse (as opposed to a touchpad), use the scroll wheel to adjust the chart width. Double-click the chart to reset width to default.'
    )

    density_input_single = st.selectbox(label='Show as',
                                        options=['Histogram', 'Density plot'],
                                        key='density_input_single')

    grades_histogram_chart_single = plot_altair_histogram(
        filtered_grades_data_single, density_input_single, 60)

    st.altair_chart(grades_histogram_chart_single, use_container_width=True)
