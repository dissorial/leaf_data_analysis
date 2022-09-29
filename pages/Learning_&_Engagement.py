import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from utils.questionnaire_helper import get_classdata, get_remaining_questions, plot_barchart_answers, get_question_data, get_mean_data, get_median_data, get_std_data, plot_bar_chart_classes, sns_violin
from utils.data_load import decrypt_data
import seaborn as sns
from functools import reduce
from PIL import Image

st.set_page_config(layout="wide",
                   page_title='Learning & Engagement',
                   initial_sidebar_state='expanded')

tab1, tab2, tab3 = st.tabs(['General part', 'Class-wise #1', 'Class-wise #2'])

with tab1:

    st.markdown('# End-of-year 2022: Learning & Engagement Questionnaire')
    st.markdown('## Explanation of data on this page')

    with st.expander('Expand/collapse', expanded=True):
        st.markdown(
            'This page shows data for the first, general part of the questionnaire. This part had 7 questions:'
        )
        st.markdown('- 1. What helps your learning and growth most?')
        st.markdown('- 2. I am motivated to study when…')
        st.markdown('- 3. The assigned work is meaningful when…')
        st.markdown('- 4. I feel challenged (in a good way) when…')
        st.markdown(
            '- 5. My concerns about the quality of learning that I expressed this year have been addressed (1 - No, not at all  vs 10 - Yes, all of them)'
        )
        st.markdown(
            '- 6. What is one thing you see at LEAF Academy working really well with regards to learning?'
        )
        st.markdown(
            '- 7. What is one thing you see at LEAF Academy that needs improvement with regards to learning?'
        )

        st.markdown(
            'The first four questions were multiple-choice answers, which are displayed below in a bar chart.'
        )
        st.markdown(
            'The fifth question is quantitative, the summary of which is below the bar chart.'
        )
        st.markdown(
            'Questions 6 and 7 were free response questions, the answers to which are displayed at the bottom in a table.'
        )

    df_csv = decrypt_data('data/questionnaire/general_data_enc.csv')
    # df_csv = pd.read_csv('data/questionnaire/general_data.csv')

    st.markdown('## Questions 1-4')
    selected_question = st.selectbox(
        label='Choose a question from the questionnaire to display',
        options=df_csv.columns[:-5].tolist())

    years_available = df_csv['Grade'].unique().tolist()

    years_chosen = st.multiselect(label='Filter years',
                                  options=years_available,
                                  default=years_available,
                                  key='years_chosen')

    if (len(years_chosen) == 0):
        st.error('Choose at least one year')
        st.stop()

    df_csv = df_csv[df_csv['Grade'].isin(years_chosen)]

    question_data = get_question_data(df_csv, selected_question)

    bar_chart_answers = plot_barchart_answers(question_data)

    with st.expander('Expand/collapse', expanded=True):
        st.altair_chart(bar_chart_answers, use_container_width=True)

    quality_of_learning_df = df_csv[[df_csv.columns[4], 'Grade']]

    st.markdown('## Question 5')
    with st.expander(
            'My concerns about the quality of learning that I expressed this year have been addressed (1 - No, not at all  vs 10 - Yes, all of them)',
            expanded=True):
        st.markdown(
            'Note: you can use the filter for years at the top of the page for this question too'
        )
        leftcol, middlecol, rightcol = st.columns(3)
        with leftcol:
            mean_data = get_mean_data(quality_of_learning_df)
            st.metric(label='Mean', value=mean_data)
        with middlecol:
            median_data = get_median_data(quality_of_learning_df)
            st.metric(label='Median', value=median_data)
        with rightcol:
            std_data = get_std_data(quality_of_learning_df)
            st.metric(label='Standard deviation', value=std_data)

    st.markdown('## Questions 6 and 7')
    free_response_question = st.selectbox(label='Select a question',
                                          options=df_csv.columns[5:8].tolist())

    other_questions_data = get_remaining_questions(df_csv,
                                                   free_response_question)

    with st.expander('Expand/collapse to see/hide answers'):
        st.table(other_questions_data)

with tab2:

    st.markdown('# End-of-year 2022: Learning & Engagement Questionnaire')
    st.markdown('## Explanation of data on this page')

    with st.expander('Expand/collapse', expanded=True):
        st.markdown(
            '- This page contains answers to questions that students answered for individual classes. You can see (and select) these questions in the drop-down menu below. The bar chart shows aggregate metrics for a selected question across all classes'
        )
        st.markdown(
            '- Hover with your mouse over the bar chart to see the standard deviation for a particular class'
        )

    classdata_df = decrypt_data('data/questionnaire/class_data_enc.csv')
    # classdata_df = pd.read_csv('data/questionnaire/class_data.csv')
    classdata_questions = classdata_df.columns[2:-1].tolist()

    col1_left, col2_right = st.columns(2)

    chosen_class_question = st.selectbox(label='Question',
                                         options=classdata_questions)

    isolated_df_class = classdata_df[[chosen_class_question, 'Grade', 'Class']]

    available_grades = isolated_df_class['Grade'].unique().tolist()

    col2_left, col2_right = st.columns(2)

    with col2_left:
        grade_filter_class = st.multiselect(label='Filter grades',
                                            options=available_grades,
                                            default=available_grades,
                                            key='grade_filter_class')

    with col2_right:
        aggFunction_input = st.selectbox(label='Aggregate function',
                                         options=['Mean', 'Median'],
                                         key='aggFunction')

    filtered_classdata = get_classdata(isolated_df_class, grade_filter_class)

    # st.dataframe(filtered_classdata)
    class_std = filtered_classdata.groupby(['Class']).std().reset_index()
    class_mean = filtered_classdata.groupby(['Class']).mean().reset_index()

    class_median = filtered_classdata.groupby(['Class']).median().reset_index()
    class_sum = filtered_classdata.groupby(['Class']).sum().reset_index()
    sth = filtered_classdata.groupby(['Class'
                                      ]).size().reset_index(name='Respondents')

    grouped_metrics = [class_std, class_mean, class_median, sth]
    df_metrics = reduce(
        lambda left, right: pd.merge(left, right, on=['Class'], how='left'),
        grouped_metrics)
    class_chart = plot_bar_chart_classes(df_metrics, aggFunction_input)

    st.altair_chart(class_chart, use_container_width=True)

with tab3:

    st.markdown('# End-of-year 2022: Learning & Engagement Questionnaire')
    violin_image = Image.open('images/violin_explanation.png')
    st.markdown('## Explanation of data on this page')

    with st.expander('Expand/collapse', expanded=True):
        st.markdown(
            '- This page contains the same data as the Class-wise #1 page. However, instead of visualizing answers to one question across all classes, it visualizes responses to all questions in a single class.'
        )
        st.markdown(
            '- Note: In the explanation image below, the percentages in green denote the percentage of responses that fall between two green lines.'
        )
        st.image(violin_image)

    single_class = decrypt_data('data/questionnaire/class_data_enc.csv')
    # single_class = pd.read_csv('data/questionnaire/class_data.csv')

    tab3_leftcol, tab3_rightcol = st.columns(2)

    with tab3_leftcol:
        chosen_class_single = st.selectbox(
            label='Choose a class',
            options=single_class['Class'].unique().tolist(),
            key='chosen_class_single')

    fil_df = single_class[single_class['Class'] == chosen_class_single]

    with tab3_rightcol:
        st.metric(label='Number of respondents', value=fil_df.shape[0])

    questions = single_class.columns[2:-1].tolist()

    q3 = sns_violin(fil_df, questions[2])

    q6 = sns_violin(fil_df, questions[5])
    q1 = sns_violin(fil_df, questions[0])
    q4 = sns_violin(fil_df, questions[3])
    q2 = sns_violin(fil_df, questions[1])
    q5 = sns_violin(fil_df, questions[4])
    a, b = st.columns(2)
    with a:
        st.pyplot(q1)
        st.pyplot(q3)
        st.pyplot(q5)
    with b:
        st.pyplot(q2)
        st.pyplot(q4)
        st.pyplot(q6)