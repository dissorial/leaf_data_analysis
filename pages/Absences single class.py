import streamlit as st
import pandas as pd
from utils.absences_helper import plot_absences_stacked, absences_meta, seaborn_barchart_resampe_data, seaborn_barchart_create, load_data_absences, preprocess
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Absences: single class',
                   initial_sidebar_state='expanded')

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

df_loaded = load_data_absences(academic_year)
absences_data = preprocess(df_loaded)

statuses = absences_data['Absence Status'].unique().tolist()


def get_filtered_absesence_data(df, years, status, terms):
    return df[(df['Year'].isin(years))
              & (df['Absence Status'].isin(status)) & (df['Term'].isin(terms))]


st.markdown('# Absences: single class')

col1_abs_single, col2_abs_single, col3_abs_single = st.columns(3)
second_row_left, second_row_right = st.columns(2)

tab_status, tab_count, tab_over_time = st.tabs(
    ['Absences by status', 'Absences by count', 'Absences over time'])

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

with second_row_left:
    filter_abs_status = st.multiselect(label='Filter status',
                                       options=statuses,
                                       default=statuses,
                                       key='filter_abs_status_single')

with second_row_right:
    absence_split_input = st.selectbox(
        label='Split by',
        options=['Program', 'Class', 'Year', 'Hall', 'Advisors'],
        key='absence_split_input')

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

classdata = filtered_absence_data[filtered_absence_data['Class'] ==
                                  chosen_class]

with tab_status:
    single_absence_stacked = plot_absences_stacked(
        classdata,
        absence_split_input,
    )

    st.altair_chart(single_absence_stacked, use_container_width=True)

with tab_count:

    absences_aggfunction_single = st.selectbox(
        label='Aggregate function',
        options=['mean', 'median'],
        key='absences_aggfunction_single')

    absence_meta_single = absences_meta(
        classdata[classdata['Absence Status'].isin(filter_abs_status)],
        absence_split_input, absences_aggfunction_single)

    st.altair_chart(absence_meta_single, use_container_width=True)

with tab_over_time:

    sea_month_data = seaborn_barchart_resampe_data(classdata, 'Month',
                                                   'abs_count')

    sea_month_chart = seaborn_barchart_create(
        sea_month_data,
        'Month',
        'avg', [
            'September', 'October', 'November', 'December', 'January',
            'February', 'March', 'April', 'May'
        ],
        chart_ylabel='Average number of absences per month')
    st.pyplot(sea_month_chart.figure)

    sea_week_data = seaborn_barchart_resampe_data(classdata, 'Week',
                                                  'abs_count')
    sea_week_chart = seaborn_barchart_create(
        sea_week_data,
        'Week',
        'avg',
        rotated_labels=True,
        chart_ylabel='Average number of absences per week')
    st.pyplot(sea_week_chart.figure)

    sea_day_data = seaborn_barchart_resampe_data(classdata, 'Day of Week',
                                                 'abs_count')
    sea_day_chart = seaborn_barchart_create(
        sea_day_data,
        'Day of Week',
        'avg', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        chart_ylabel='Average number of absences per day')
    st.pyplot(sea_day_chart.figure)
