import streamlit as st
import pandas as pd
from utils.absences_helper import plot_daily_absences_count, plot_monthly_absences_count, plot_weekly_absences_count, plot_absences_stacked, absences_meta
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Absences',
                   initial_sidebar_state='expanded')

absences_data = decrypt_data('data/absences/Absences_jup_enc.csv')

#plotting charts
tab1, tab2 = st.tabs(['All classes', 'Single class drilldown'])

with tab1:

    st.markdown('# Absences')

    statuses = absences_data['Absence Status'].unique().tolist()

    st.markdown('## Filter and select')
    col1_abs, col2_abs, col3_abs = st.columns(3)

    with col1_abs:
        absences_drilldown = st.selectbox(label='Show absences by',
                                          options=[
                                              'Class', 'Hall', 'Term',
                                              'Program', 'Year',
                                              'Student leadership', 'Advisors'
                                          ],
                                          key='absences_drilldown')

    with col2_abs:
        filter_abs_years = st.multiselect(
            label='Filter years',
            options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            key='filter_abs_years')

    with col3_abs:
        filter_abs_terms = st.multiselect(label='Filter term',
                                          options=['T1', 'T2', 'T3', 'T4'],
                                          default=['T1', 'T2', 'T3', 'T4'],
                                          key='filter_abs_terms')

    filter_abs_status = st.multiselect(label='Filter status',
                                       options=statuses,
                                       default=statuses,
                                       key='filter_abs_status')

    if (len(filter_abs_years) == 0 or len(filter_abs_terms) == 0
            or len(filter_abs_status) == 0):
        st.error('Choose at least one parameter in each filter')
        st.stop()

    absences_data['Attendance Date'] = pd.to_datetime(
        absences_data['Attendance Date'], infer_datetime_format=True)
    absences_data['Month'] = absences_data['Attendance Date'].to_numpy(
    ).astype('datetime64[M]')
    absences_data['Week'] = absences_data['Attendance Date'].to_numpy().astype(
        'datetime64[W]')
    absences_data['abs_count'] = 1

    def get_filtered_absesence_data(df, years, status, terms):
        return df[(df['Year'].isin(years))
                  & (df['Absence Status'].isin(status)) &
                  (df['Term'].isin(terms))]

    filtered_absence_data = get_filtered_absesence_data(
        absences_data, filter_abs_years, filter_abs_status, filter_abs_terms)

    absences_stacked_chart = plot_absences_stacked(filtered_absence_data,
                                                   absences_drilldown)

    st.markdown(
        '## Comparison of absence status by status grouped by {}'.format(
            absences_drilldown))
    with st.expander('Expand/collapse', expanded=True):
        st.info(
            'Hover over the stacked bar chart below with your cursor to see the corresponding number of traffic lights belonging to each category.'
        )
        st.altair_chart(absences_stacked_chart, use_container_width=True)

    st.markdown('## Comparison of number of absences per student by {}'.format(
        absences_drilldown))
    with st.expander('Expand/collapse', expanded=True):
        absences_aggfunction = st.selectbox(label='Aggregate function',
                                            options=['mean', 'median', 'sum'],
                                            key='absences_aggfunction')

        all_absences_chart = absences_meta(filtered_absence_data,
                                           absences_drilldown,
                                           absences_aggfunction)

        st.altair_chart(all_absences_chart, use_container_width=True)

    st.markdown('## Absences over time per student')
    with st.expander('Expand/collapse', expanded=True):
        weekly_count_chart = plot_weekly_absences_count(
            filtered_absence_data, "Average number of absences by week")
        monthly_count_chart = plot_monthly_absences_count(
            filtered_absence_data, "Average number of absences by month")
        daily_count_chart = plot_daily_absences_count(
            filtered_absence_data, "Average number of absences by day of week")

        filter_view = st.selectbox(label='Time view',
                                   options=['Monthly', 'Weekly', 'Daily'])

        def select_time_chart(timeviewinput):
            if timeviewinput == 'Monthly':
                st.altair_chart(monthly_count_chart, use_container_width=True)
            elif timeviewinput == 'Weekly':
                st.altair_chart(weekly_count_chart, use_container_width=True)
            else:
                st.altair_chart(daily_count_chart, use_container_width=True)

        select_time_chart(filter_view)

with tab2:
    st.markdown('# Absences')

    st.markdown('## Filter and select')
    col1_abs_single, col2_abs_single, col3_abs_single = st.columns(3)

    classlist = absences_data['Class'].unique().tolist()

    with col1_abs_single:
        chosen_class = chosen_class = st.selectbox(label='Choose a class',
                                                   options=classlist,
                                                   key='chosen_class_absences',
                                                   index=1)

    with col2_abs_single:
        filter_abs_years = st.multiselect(
            label='Filter years',
            options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            key='filter_abs_years_single')

    with col3_abs_single:
        filter_abs_terms = st.multiselect(label='Filter term',
                                          options=['T1', 'T2', 'T3', 'T4'],
                                          default=['T1', 'T2', 'T3', 'T4'],
                                          key='filter_abs_terms_single')

    second_row_left, second_row_right = st.columns(2)

    with second_row_left:
        filter_abs_status = st.multiselect(label='Filter status',
                                           options=statuses,
                                           default=statuses,
                                           key='filter_abs_status_single')

    with second_row_right:
        absence_split_input = st.selectbox(
            label='Split by',
            options=['Program', 'Class', 'Year', 'Hall', 'Student leadership'],
            key='absence_split_input')

    if (len(filter_abs_years) == 0 or len(filter_abs_terms) == 0
            or len(filter_abs_status) == 0):
        st.error('Choose at least one parameter in each filter')
        st.stop()

    def get_filtered_absesence_data(df, years, status, terms):
        return df[(df['Year'].isin(years))
                  & (df['Absence Status'].isin(status)) &
                  (df['Term'].isin(terms))]

    filtered_absence_data = get_filtered_absesence_data(
        absences_data, filter_abs_years, filter_abs_status, filter_abs_terms)

    classdata = filtered_absence_data[filtered_absence_data['Class'] ==
                                      chosen_class]

    single_absence_stacked = plot_absences_stacked(
        classdata,
        absence_split_input,
    )

    st.markdown('## Comparison of absence status grouped by {}'.format(
        absence_split_input))
    st.altair_chart(single_absence_stacked, use_container_width=True)

    st.markdown(
        '## Comparison of number of absences per student in {} by {}'.format(
            chosen_class, absence_split_input))
    third_row_left, third_row_right = st.columns(2)

    with third_row_left:
        absences_aggfunction_single = st.selectbox(
            label='Aggregate function',
            options=['mean', 'median', 'sum'],
            key='absences_aggfunction_single')

    with third_row_right:
        filter_abs_status_single = st.selectbox(
            label='Filter status',
            options=statuses,
            key='filter_abs_status_single_selectbox')

    absence_meta_single = absences_meta(
        classdata[classdata['Absence Status'] == filter_abs_status_single],
        absence_split_input, absences_aggfunction_single)

    st.altair_chart(absence_meta_single, use_container_width=True)

    weekly_count_chart_single = plot_weekly_absences_count(
        classdata, "Average number of absences by week")
    monthly_count_chart_single = plot_monthly_absences_count(
        classdata, "Average number of absences by month")
    daily_count_chart_single = plot_daily_absences_count(
        classdata, "Average number of absences by day of week")

    st.markdown('## Average number of absences across time')
    filter_view_single = st.selectbox(label='Time view',
                                      options=['Monthly', 'Weekly', 'Daily'],
                                      key='filter_view_single')

    def select_time_chart(timeviewinput):
        if timeviewinput == 'Monthly':
            st.altair_chart(monthly_count_chart_single,
                            use_container_width=True)
        elif timeviewinput == 'Weekly':
            st.altair_chart(weekly_count_chart_single,
                            use_container_width=True)
        else:
            st.altair_chart(daily_count_chart_single, use_container_width=True)

    select_time_chart(filter_view_single)
