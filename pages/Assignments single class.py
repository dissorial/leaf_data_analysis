import streamlit as st
from utils.assignments_helper import preprocess_data, seaborn_barchart_create, seaborn_barchart_resampe_data, load_data_assignments
from utils.data_load import get_filtered_assignment_classdata
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Assignments: single class',
                   initial_sidebar_state='expanded')

st.markdown('# Assignments: single class')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

df_loaded = load_data_assignments(academic_year)
assignments_data_datetime = preprocess_data(df_loaded)
classlist = assignments_data_datetime['Class'].unique().tolist()

st.markdown('## Filter and select')
left_one, middle_one, right_one = st.columns(3)

with left_one:
    chosen_class = st.selectbox(label='Class', options=classlist, index=0)

available_years = assignments_data_datetime[
    assignments_data_datetime['Class'] ==
    chosen_class]['Year'].unique().tolist()

with middle_one:
    year_filters = st.multiselect(label='Filter years',
                                  options=available_years,
                                  default=available_years)

available_display_stauts = assignments_data_datetime[
    assignments_data_datetime['Class'] ==
    chosen_class]['Display Status'].unique().tolist()
with right_one:
    display_status_filter = st.multiselect(label='Dispaly status',
                                           options=available_display_stauts,
                                           default=available_display_stauts)

available_completion_status = assignments_data_datetime[
    assignments_data_datetime['Class'] ==
    chosen_class]['Completion Status'].unique().tolist()

completion_status_filter = st.multiselect(label='Completion status filter',
                                          options=available_completion_status,
                                          default=available_completion_status,
                                          key='completion_status_filter')

if (len(year_filters) == 0 or len(display_status_filter) == 0):
    st.error('Select at least one year and display status')
    st.stop()

classData = get_filtered_assignment_classdata(assignments_data_datetime,
                                              chosen_class, year_filters,
                                              completion_status_filter,
                                              display_status_filter)

st.markdown('## Charts')
with st.expander('Monthly', expanded=True):
    st.markdown('## Average number of assignments per student in {}'.format(
        chosen_class))
    sea_monthly_count_data = seaborn_barchart_resampe_data(
        classData, 'Month', 'Assign_count')
    sea_monthly_count_chart = seaborn_barchart_create(
        sea_monthly_count_data, 'Month', 'avg', [
            'September', 'October', 'November', 'December', 'January',
            'February', 'March', 'April', 'May'
        ])
    st.pyplot(sea_monthly_count_chart.figure)

    st.markdown('## Average length of assignments in {}'.format(chosen_class))
    sea_monthly_duration_data = seaborn_barchart_resampe_data(classData,
                                                              'Month',
                                                              'Assign_count',
                                                              duration=True)
    sea_monthly_duration_chart = seaborn_barchart_create(
        sea_monthly_duration_data, 'Month', 'avg', [
            'September', 'October', 'November', 'December', 'January',
            'February', 'March', 'April', 'May'
        ])
    st.pyplot(sea_monthly_duration_chart.figure)

with st.expander('Weekly', expanded=True):
    st.markdown('## Average number of assignments per student in {}'.format(
        chosen_class))
    sea_weekly_count_data = seaborn_barchart_resampe_data(
        classData, 'Week', 'Assign_count')
    sea_weekly_count_chart = seaborn_barchart_create(sea_weekly_count_data,
                                                     'Week',
                                                     'avg',
                                                     rotated_labels=True)
    st.pyplot(sea_weekly_count_chart.figure)

    st.markdown('## Average length of assignments in {}'.format(chosen_class))
    sea_weekly_duration_data = seaborn_barchart_resampe_data(classData,
                                                             'Week',
                                                             'Assign_count',
                                                             duration=True)
    sea_weekly_duration_chart = seaborn_barchart_create(
        sea_weekly_duration_data, 'Week', 'avg', rotated_labels=True)
    st.pyplot(sea_weekly_duration_chart.figure)

st.markdown('## Explanations')
with st.expander('Explanation of the chart above'):
    st.markdown(
        '- The aggregate metric used for grouping the number of assignments below is "Date assigned" (as opposed to "Due date").'
    )
    st.markdown(
        '- A month is defined as the range between the first and last day of the month. This also means that, for example, an assignment assigned in September with a due date in October is thought to belong to September, not October.'
    )
    st.markdown(
        '- "Avg length" legend on the right denotes the average assignment length in days as defined by *assignment due date* minus *assignment date assigned*'
    )

with st.expander('Sample rows of data used for charts on this page'):
    st.dataframe(assignments_data_datetime[[
        'Date assigned', 'Due date', 'Class', 'Type', 'Description',
        'Completion Status', 'Display Status', 'Term', 'Year'
    ]].head(2))
    st.markdown(
        'Each row represents data about a signle assignment for a single student. In total, there are ~30,000 rows like this in the dataset, which results from the total number of assignments across all classes multiplied by the number of students in each class'
    )

with st.expander('Explanation of data preprocessing'):
    st.markdown(
        '- A single class taught across more years is always shown separately in Veracross. In other words, "Character Seminar Y4" and "Character Seminar Y3" are shown separately. To declutter the data, I merged such instances into a single class, such as "Character Semimnar". The filter for years below serves as a replacement.'
    )
    st.markdown(
        '- Similarly, certain classes are taught only in one year but split into two or more groups, such as "AP ENG A" and "AP ENG B". These are also merged into a single class under the assumption that the existence of two groups is the result of too many students enrolled in the class, not a difference in skill level.'
    )