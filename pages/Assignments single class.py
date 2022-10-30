import streamlit as st
from utils.assignments_helper import plot_weekly_assignments_count, plot_monthly_assignments_count, preprocess_data
from utils.data_load import get_filtered_assignment_classdata, decrypt_data
import pandas as pd

st.set_page_config(layout="wide",
                   page_title='Assignments: single class',
                   initial_sidebar_state='expanded')

initial_21_22 = decrypt_data('data/21_22/assignments/assignments_2122.csv')
initial_22_23 = decrypt_data('data/22_23/assignments/assignments_2223.csv')

st.markdown('# Assignments: single class')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

pre_2122 = preprocess_data(initial_21_22)
pre_2223 = preprocess_data(initial_22_23)

assignments_data_datetime = pre_2122 if academic_year == '2021/2022' else pre_2223

classlist = assignments_data_datetime['Class'].unique().tolist()

left_one, right_one = st.columns(2)

with left_one:
    chosen_class = st.selectbox(label='Class', options=classlist, index=0)

with right_one:
    timeview_input = st.selectbox(label='Time view',
                                  options=['Weekly', 'Monthly'])

left_two, right_two = st.columns(2)

available_years = assignments_data_datetime[
    assignments_data_datetime['Class'] ==
    chosen_class]['Year'].unique().tolist()

with left_two:
    year_filters = st.multiselect(label='Filter years',
                                  options=available_years,
                                  default=available_years)

available_display_stauts = assignments_data_datetime[
    assignments_data_datetime['Class'] ==
    chosen_class]['Display Status'].unique().tolist()
with right_two:
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

monthly_assignments_count_chart = plot_monthly_assignments_count(classData)

weekly_assignments_count_chart = plot_weekly_assignments_count(classData)

st.markdown(
    '## Average number of assignments per student in {}'.format(chosen_class))
st.altair_chart(monthly_assignments_count_chart if timeview_input == 'Monthly'
                else weekly_assignments_count_chart,
                use_container_width=True)
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