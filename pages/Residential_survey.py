import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from PIL import Image
from utils.residential_helper import get_question_data, merge_business_weekend, plot_bar_chart
from utils.data_load import decrypt_data

pd.options.mode.chained_assignment = None

st.set_page_config(layout="wide",
                   page_title='Residential Survey',
                   initial_sidebar_state='expanded')

df = decrypt_data('data/21_22/residential_survey/residential_survey_2122.csv')
# df = pd.read_csv('data/21_22/residential_survey/residential_survey_2122.csv')

st.markdown('# Residential survey responses 2021/2022')

with st.expander('Information about questionnaire responses', expanded=True):
    residential_q_img = Image.open('images/residential_q.png')
    st.image(residential_q_img)

meta_left_col, meta_right_col = st.columns(2)

with meta_left_col:
    hall_filter = st.multiselect(
        label='Hall filter',
        options=['Founders', 'Gentlemen', 'Sprouts', 'Fortes', 'Matej'],
        default=['Founders', 'Gentlemen', 'Sprouts', 'Fortes', 'Matej'],
        key='hall_filter_sleep')

with meta_left_col:
    year_filter = st.multiselect(
        label='Year filter',
        options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        key='year_filter_sleep')

aggfunction_input = st.selectbox(label='Aggregate function',
                                 options=['mean', 'median', 'stdev'])

df = df[df['Year'].isin(year_filter) & df['Hall'].isin(hall_filter)]

if (len(hall_filter) == 0 or len(year_filter) == 0):
    st.error('Choose at least year and hall')
    st.stop()

default_groupings = ['Hall', 'Term', 'Year']
with meta_right_col:
    split_input = st.selectbox(label='Inner group',
                               options=default_groupings,
                               key='color_input')

other_groupings = [x for x in default_groupings if x != split_input] + ['None']

with meta_right_col:
    col_inupt = st.selectbox(label='Outer group',
                             options=other_groupings,
                             key='col_input',
                             index=1)

tab_general, tab_sleep, tab_study, tab_entre, tab_eca, tab_phys, tab_leisure = st.tabs(
    [
        'General', 'Sleep', 'Academics', 'Entrepreneurship',
        'Extra-curriculars', 'Physical activity', 'Leisure'
    ])

with tab_general:
    hallmeetings_like = get_question_data(df, df.columns[0])
    chart_hallmeetings_like = plot_bar_chart(hallmeetings_like,
                                             hallmeetings_like.columns[-1],
                                             split_input,
                                             split_input,
                                             '-x',
                                             col_inupt, [0, 10],
                                             aggfunction_input,
                                             axis_title='Average score',
                                             w=1300)

    with st.expander('How do you like hall meetings?', expanded=True):
        st.altair_chart(chart_hallmeetings_like)

    hall_atmosphere = get_question_data(df, df.columns[1])
    chart_hall_atmosphere = plot_bar_chart(hall_atmosphere,
                                           hall_atmosphere.columns[-1],
                                           split_input,
                                           split_input,
                                           '-x',
                                           col_inupt, [0, 10],
                                           aggfunction_input,
                                           axis_title='Average score',
                                           w=1300)
    with st.expander(
            'How do you rate the atmosphere in the hall in terms of how welcome, safe and accepted you feel there?',
            expanded=True):
        st.altair_chart(chart_hall_atmosphere)

    performance_extent = get_question_data(df, df.columns[2])
    chart_performance_extent = plot_bar_chart(performance_extent,
                                              performance_extent.columns[-1],
                                              split_input,
                                              split_input,
                                              '-x',
                                              col_inupt, [0, 10],
                                              aggfunction_input,
                                              axis_title='Average score',
                                              w=1300)
    with st.expander(
            'To what extent has your residential experience helped/harmed your performance at LEAF Academy?',
            expanded=True):
        st.altair_chart(chart_performance_extent)

    residential_experience = get_question_data(df, df.columns[3])
    chart_residential_experience = plot_bar_chart(
        residential_experience,
        residential_experience.columns[-1],
        split_input,
        split_input,
        '-x',
        col_inupt, [0, 10],
        aggfunction_input,
        axis_title='Average score',
        w=1300)

    with st.expander(
            'How did you enjoy your residential experience in these Terms in general?',
            expanded=True):
        st.altair_chart(chart_residential_experience)

with tab_sleep:
    st.markdown(
        '- *On average, how many hours of sleep do you get per day (includes afternoon naps)?*'
    )
    left_col_sleep, right_col_sleep = st.columns(2)

    sleep_business = get_question_data(df, df.columns[4])
    sleep_weekend = get_question_data(df, df.columns[5])
    sleep_data_merged = merge_business_weekend(
        sleep_business, sleep_weekend,
        'On average, how many hours of sleep do you get per day?')

    sleep_chart_weekday = plot_bar_chart(
        sleep_data_merged[sleep_data_merged['Weekday/weekend'] == 'weekday'],
        sleep_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 10], aggfunction_input)

    sleep_chart_weekend = plot_bar_chart(
        sleep_data_merged[sleep_data_merged['Weekday/weekend'] == 'weekend'],
        sleep_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 10], aggfunction_input)
    with left_col_sleep:
        st.markdown('## Work week')
        st.altair_chart(sleep_chart_weekday, use_container_width=False)
    with right_col_sleep:
        st.markdown('## Weekend')
        st.altair_chart(sleep_chart_weekend, use_container_width=False)

with tab_study:
    st.markdown(
        '- *On average, how many hours do you study per day (includes homework, individual study, self-study, group projects, EL homework and time spent on SEs unless they form a part of your private business... excludes class time, your own projects, entreprises, ...)?*'
    )
    left_col_study, right_col_study = st.columns(2)
    study_business = get_question_data(df, df.columns[6])
    study_weekend = get_question_data(df, df.columns[7])
    study_data_merged = merge_business_weekend(
        study_business, study_weekend,
        'On average, how many hours do you study per day?')

    study_chart_weekday = plot_bar_chart(
        study_data_merged[study_data_merged['Weekday/weekend'] == 'weekday'],
        study_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 8], aggfunction_input)

    study_chart_weekend = plot_bar_chart(
        study_data_merged[study_data_merged['Weekday/weekend'] == 'weekend'],
        study_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 8], aggfunction_input)

    with left_col_study:
        st.markdown('## Work week')
        st.altair_chart(study_chart_weekday)

    with right_col_study:
        st.markdown('## Weekend')
        st.altair_chart(study_chart_weekend)

with tab_entre:

    st.markdown(
        '- *On average, how many hours per day do you dedicate to your own entrepreneurial projects (includes your own companies, start-ups, websites, online graphic designing, paid jobs, ... excludes EL homework and time spent on SEs unless they form a part of your private business ...)?*'
    )
    left_col_entre, right_col_entre = st.columns(2)
    entre_business = get_question_data(df, df.columns[8])
    entre_weekend = get_question_data(df, df.columns[9])

    entre_data_merged = merge_business_weekend(
        entre_business, entre_weekend,
        'On average, how many hours per day do you dedicate to your own entrepreneurial projects?'
    )

    entre_weekday_chart = plot_bar_chart(
        entre_data_merged[entre_data_merged['Weekday/weekend'] == 'weekday'],
        entre_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 5], aggfunction_input)

    entre_weekend_chart = plot_bar_chart(
        entre_data_merged[entre_data_merged['Weekday/weekend'] == 'weekend'],
        entre_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 5], aggfunction_input)

    with left_col_entre:
        st.markdown('## Work week')
        st.altair_chart(entre_weekday_chart)

    with right_col_entre:
        st.markdown('## Weekend')
        st.altair_chart(entre_weekend_chart)

# st.write(entre_data_merged[entre_data_merged['type'] == 'weekday'].describe())

with tab_eca:

    st.markdown(
        '- *On average, how many hours per day do you dedicate to extra-curriculars (includes extra-curricular time, preparation for extra curriculars, excellence activities, competitions and camps, preparation for competitions, ... excludes sports)?*'
    )
    left_col_eca, right_col_eca = st.columns(2)
    eca_business = get_question_data(df, df.columns[10])
    eca_weekend = get_question_data(df, df.columns[11])
    eca_data_merged = merge_business_weekend(
        eca_business, eca_weekend,
        'On average, how many hours per day do you dedicate to extra-curriculars?'
    )

    eca_weekday_chart = plot_bar_chart(
        eca_data_merged[eca_data_merged['Weekday/weekend'] == 'weekday'],
        eca_data_merged.columns[-2], split_input, split_input, '-y', col_inupt,
        [0, 5], aggfunction_input)

    eca_weekend_chart = plot_bar_chart(
        eca_data_merged[eca_data_merged['Weekday/weekend'] == 'weekend'],
        eca_data_merged.columns[-2], split_input, split_input, '-y', col_inupt,
        [0, 5], aggfunction_input)

    with left_col_eca:
        st.markdown('## Work week')
        st.altair_chart(eca_weekday_chart)
    with right_col_eca:
        st.markdown('## Weekend')
        st.altair_chart(eca_weekend_chart)

with tab_phys:

    st.markdown(
        '- *On average, how many hours of physical activity do you get per day (anything including and above fast walking)?*'
    )
    left_col_phys, right_col_phys = st.columns(2)
    phys_business = get_question_data(df, df.columns[12])
    phys_weekend = get_question_data(df, df.columns[13])
    phys_data_merged = merge_business_weekend(
        phys_business, phys_weekend,
        'On average, how many hours of physical activity do you get per day?')

    phys_weekday_chart = plot_bar_chart(
        phys_data_merged[phys_data_merged['Weekday/weekend'] == 'weekday'],
        phys_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 5], aggfunction_input)

    phys_weekend_chart = plot_bar_chart(
        phys_data_merged[phys_data_merged['Weekday/weekend'] == 'weekend'],
        phys_data_merged.columns[-2], split_input, split_input, '-y',
        col_inupt, [0, 5], aggfunction_input)

    with left_col_phys:
        st.markdown('## Work week')
        st.altair_chart(phys_weekday_chart)
    with right_col_phys:
        st.markdown('## Weekend')
        st.altair_chart(phys_weekend_chart)

with tab_leisure:

    st.markdown(
        '- *On average, how many hours of leisure do you get per day (includes leisure reading, watching movies, playing video games, using social media, ... excludes sports, sleep, academic reading)?*'
    )
    left_col_leisure, right_col_leisure = st.columns(2)
    leisure_business = get_question_data(df, df.columns[14])
    leisure_weekend = get_question_data(df, df.columns[15])
    leisure_data_merged = merge_business_weekend(
        leisure_business, leisure_weekend,
        'On average, how many hours of leisure do you get per day?')

    leisure_weekday_chart = plot_bar_chart(
        leisure_data_merged[leisure_data_merged['Weekday/weekend'] ==
                            'weekday'], leisure_data_merged.columns[-2],
        split_input, split_input, '-y', col_inupt, [0, 8], aggfunction_input)

    leisure_weekend_chart = plot_bar_chart(
        leisure_data_merged[leisure_data_merged['Weekday/weekend'] ==
                            'weekend'], leisure_data_merged.columns[-2],
        split_input, split_input, '-y', col_inupt, [0, 8], aggfunction_input)

    with left_col_leisure:
        st.markdown('## Work week')
        st.altair_chart(leisure_weekday_chart)
    with right_col_leisure:
        st.markdown('## Weekend')
        st.altair_chart(leisure_weekend_chart)
