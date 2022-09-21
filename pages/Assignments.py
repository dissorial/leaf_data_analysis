import streamlit as st
import pandas as pd
import numpy as np
from utils.assignments_helper import plot_weekly_assignments_count, plot_monthly_assignments_count, plot_monthly_assignment_duration, plot_weekly_assignments_duration, plot_all_assignments_stacked, assignments_meta
from utils.data_load import get_filtered_assignment_classdata, decrypt_data

st.set_page_config(layout="wide", page_title='Assignments', initial_sidebar_state='expanded')

# assignments_data_status = decrypt_data(
#     'data/assignments/assignments_status01_enc.csv')

assignments_data_datetime = decrypt_data(
    'data/assignments/assignments_datetime01_enc.csv')

assignments_data_datetime['Date assigned'] = pd.to_datetime(
    assignments_data_datetime['Date assigned'], infer_datetime_format=True)
assignments_data_datetime['Due date'] = pd.to_datetime(
    assignments_data_datetime['Due date'], infer_datetime_format=True)
assignments_data_datetime['Month'] = assignments_data_datetime[
    'Date assigned'].to_numpy().astype('datetime64[M]')
assignments_data_datetime['Week'] = assignments_data_datetime[
    'Date assigned'].to_numpy().astype('datetime64[W]')
assignments_data_datetime['Assignment length'] = (
    assignments_data_datetime['Due date'] -
    assignments_data_datetime['Date assigned']) / np.timedelta64(1, 'D')
assignments_data_datetime['Assign_count'] = 1

classlist = assignments_data_datetime['Class'].unique().tolist()

tab1, tab2 = st.tabs(['All classes', 'Single class drilldown'])

with tab1:

    st.markdown('# Assignments')

    st.markdown('## Filter and select')
    col1_assign, col2_assign, col3_assign = st.columns(3)

    with col1_assign:
        assign_drilldown = st.selectbox(label='Show assignments by',
                                        options=[
                                            'Class', 'Hall', 'Term', 'Program',
                                            'Year', 'Student leadership'
                                        ],
                                        key='assign_drilldown')

    with col2_assign:
        filter_assign_years = st.multiselect(
            label='Filter years',
            options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            key='filter_assign_years')

    with col3_assign:
        filter_assign_terms = st.multiselect(label='Filter terms',
                                             options=['T1', 'T2', 'T3', 'T4'],
                                             default=['T1', 'T2', 'T3', 'T4'],
                                             key='filter_assign_terms')

    c_left, c_right = st.columns([2, 1])

    available_status_all = assignments_data_datetime[
        'Completion Status'].unique().tolist()
    with c_left:
        filter_assign_status = st.multiselect(label='Filter status',
                                              options=available_status_all,
                                              default=available_status_all,
                                              key='available_status_all')

    with c_right:
        filter_assign_display = st.multiselect(
            label='Filter dispaly',
            options=['Displayed', 'Not Displayed'],
            default=['Displayed', 'Not Displayed'],
            key='filter_assign_display')

    if (len(filter_assign_years) == 0 or len(filter_assign_terms) == 0
            or len(filter_assign_status) == 0
            or len(filter_assign_display) == 0):
        st.error('Choose at least one year and/or term')
        st.stop()

    st.markdown(
        '## Comparison of assignment status as a percentage of total, grouped by {}'
        .format(assign_drilldown))

    def get_filtered_assignment_data(df, years, terms, completion_status,
                                     display_status):
        return df[(df['Year'].isin(years)) & (df['Term'].isin(terms)) &
                  (df['Completion Status'].isin(completion_status)) &
                  (df['Display Status'].isin(display_status))]

    filtered_assignment_data = get_filtered_assignment_data(
        assignments_data_datetime, filter_assign_years, filter_assign_terms,
        filter_assign_status, filter_assign_display)

    # Fig 3
    assignments_stacked_chart = plot_all_assignments_stacked(
        filtered_assignment_data, assign_drilldown)

    with st.expander('Expand/collapse', expanded=True):
        st.info(
            'Hover over the stacked bar chart below with your cursor to see the corresponding number of traffic lights belonging to each category.'
        )
        st.info(
            'Use to mouse scroll wheel to zoom in and out; double-click to reset zoom to default.'
        )
        st.markdown(
            '- You might be wondering why the number of assignments that show on mouse hover is quite high. This is because chart below takes the sum of assignments across the groups you select.'
        )
        st.markdown(
            '- For example, take a class with 10 students. Eight of them always submit assignments on time (marked as "Complete"), and the remaining two always submit them late (marked as "Late"). If this class assigns 40 assignments throughout the entire year, the total number of assignment records is 10x40=400, of which "Complete" is 8x40=320, and "Late" is 2x40=80.'
        )
        st.altair_chart(assignments_stacked_chart, use_container_width=True)

    st.markdown('## Comparison of number of assignments, grouped by {}'.format(
        assign_drilldown))
    with st.expander('Expand/collapse', expanded=True):
        assign_aggfunction = st.selectbox(label='Aggregate function',
                                          options=['mean', 'median', 'sum'],
                                          key='assign_aggfunction')

        # Fig 4
        assignments_meta_chart = assignments_meta(filtered_assignment_data,
                                                  assign_drilldown,
                                                  assign_aggfunction)
        st.altair_chart(assignments_meta_chart, use_container_width=True)

with tab2:
    st.markdown('# Assignment drilldown by class')
    with st.expander('Sample rows of data used for charts on this page'):
        st.dataframe(assignments_data_datetime[[
            'Date assigned', 'Due date', 'Class', 'Type', 'Description',
            'Completion Status', 'Display Status', 'Term', 'Year'
        ]].head(2))
        st.markdown(
            'Each row represents data about a signle assignment for a single student. In total, there are ~30,000 rows like this in the dataset, which results from the total number of assignments across all classes multiplied by the number of students in each class'
        )

    with st.expander('Explanation of data preprocessing', expanded=True):
        st.markdown(
            '- A single class taught across more years is always shown separately in Veracross. In other words, "Character Seminar Y4" and "Character Seminar Y3" are shown separately. To declutter the data, I merged such instances into a single class, such as "Character Semimnar". The filter for years below serves as a replacement.'
        )
        st.markdown(
            '- Similarly, certain classes are taught only in one year but split into two or more groups, such as "AP ENG A" and "AP ENG B". These are also merged into a single class under the assumption that the existence of two groups is the result of too many students enrolled in the class, not a difference in skill level.'
        )

    st.markdown('## Filter and select')
    left_one, right_one = st.columns(2)

    with left_one:
        chosen_class = st.selectbox(label='Class', options=classlist, index=0)

    with right_one:
        timeview_input = st.selectbox(label='Time view',
                                      options=['Monthly', 'Weekly'])

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
        display_status_filter = st.multiselect(
            label='Dispaly status',
            options=available_display_stauts,
            default=available_display_stauts)

    available_completion_status = assignments_data_datetime[
        assignments_data_datetime['Class'] ==
        chosen_class]['Completion Status'].unique().tolist()

    completion_status_filter = st.multiselect(
        label='Completion status filter',
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

    monthlyduration = plot_monthly_assignment_duration(classData)

    weekly_assignments_count_chart = plot_weekly_assignments_count(classData)

    weeklyduration = plot_weekly_assignments_duration(classData)

    st.markdown('## Average number of assignments per student in {}'.format(
        chosen_class))
    st.altair_chart(monthly_assignments_count_chart if timeview_input
                    == 'Monthly' else weekly_assignments_count_chart,
                    use_container_width=True)
    with st.expander('Explanation of the chart above', expanded=True):
        st.markdown(
            '- The aggregate metric used for grouping the number of assignments below is "Date assigned" (as opposed to "Due date").'
        )
        st.markdown(
            '- A month is defined as the range between the first and last day of the month. This also means that, for example, an assignment assigned in September with a due date in October is thought to belong to September, not October.'
        )
        st.markdown(
            '- The height of each bar corresponds to the average number of assignments for a chosen class between the tick marks (months or weeks) on each side. For example, there were 10 assignments on average per student between Sep 2021 and Oct 2021 in the CES Writing and Rhetoric class.'
        )

    st.markdown(
        '## Average length of assignment in days for {}'.format(chosen_class))

    st.altair_chart(
        monthlyduration if timeview_input == 'Monthly' else weeklyduration,
        use_container_width=True)

    with st.expander('Explanation of the chart above', expanded=True):
        st.markdown(
            "- Assignment length is defined as the number of days between an assignment's *Due date* and *Date assigned*"
        )
        st.markdown(
            '- Similarly to reading the above chart, the height of each bar corresponds to the average lenght in days for a chosen class between the tick marks (months or weeks) on each side. For example, the average length of assignments assigned between Sep 2021 and Oct 2021 in the CES Writing and Rhetoric class was a little more than 4 days.'
        )