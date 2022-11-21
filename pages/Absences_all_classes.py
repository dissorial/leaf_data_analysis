import streamlit as st
import pandas as pd
from utils.absences_helper import plot_absences_stacked, absences_meta, seaborn_barchart_create, seaborn_barchart_resampe_data, load_data_absences, preprocess
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Absences: all classes',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

df_loaded = load_data_absences(academic_year)
absences_data = preprocess(df_loaded)

st.markdown('# Absences: all classes')

statuses = absences_data['Absence Status'].unique().tolist()

filter_abs_status = st.multiselect(label='Filter status',
                                   options=statuses,
                                   default=statuses,
                                   key='filter_abs_status')
col1_abs, col2_abs, col3_abs = st.columns(3)

tab_status, tab_absence_count, tab_absences_over_time = st.tabs(
    ['Absences by status', 'Absences by count', 'Absences over time'])
with col1_abs:
    absences_drilldown = st.selectbox(label='Show absences by',
                                      options=[
                                          'Class', 'Hall', 'Term', 'Program',
                                          'Year', 'Student leadership',
                                          'Advisors'
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

if (len(filter_abs_years) == 0 or len(filter_abs_terms) == 0
        or len(filter_abs_status) == 0):
    st.error('Choose at least one parameter in each filter')
    st.stop()


def get_filtered_absesence_data(df, years, status, terms):
    return df[(df['Year'].isin(years))
              & (df['Absence Status'].isin(status)) & (df['Term'].isin(terms))]


filtered_absence_data = get_filtered_absesence_data(absences_data,
                                                    filter_abs_years,
                                                    filter_abs_status,
                                                    filter_abs_terms)

with tab_status:
    absences_stacked_chart = plot_absences_stacked(filtered_absence_data,
                                                   absences_drilldown)
    st.info(
        'Hover over the stacked bar chart below with your cursor to see the corresponding number of traffic lights belonging to each category.'
    )
    st.altair_chart(absences_stacked_chart, use_container_width=True)

with tab_absence_count:
    absences_aggfunction = st.selectbox(label='Aggregate function',
                                        options=['mean', 'median', 'sum'],
                                        key='absences_aggfunction')

    all_absences_chart = absences_meta(filtered_absence_data,
                                       absences_drilldown,
                                       absences_aggfunction)

    st.altair_chart(all_absences_chart, use_container_width=True)

with tab_absences_over_time:
    sea_month_data = seaborn_barchart_resampe_data(filtered_absence_data,
                                                   'Month', 'abs_count')

    sea_month_chart = seaborn_barchart_create(sea_month_data, 'Month', 'avg', [
        'September', 'October', 'November', 'December', 'January', 'February',
        'March', 'April', 'May'
    ])
    st.pyplot(sea_month_chart.figure)

    sea_week_data = seaborn_barchart_resampe_data(filtered_absence_data,
                                                  'Week', 'abs_count')
    sea_week_chart = seaborn_barchart_create(sea_week_data,
                                             'Week',
                                             'avg',
                                             rotated_labels=True)
    st.pyplot(sea_week_chart.figure)

    sea_day_data = seaborn_barchart_resampe_data(filtered_absence_data,
                                                 'Day of Week', 'abs_count')
    sea_day_chart = seaborn_barchart_create(
        sea_day_data, 'Day of Week', 'avg',
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
    st.pyplot(sea_day_chart.figure)
