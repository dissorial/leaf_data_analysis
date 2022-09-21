import streamlit as st
from utils.grades_helper import grades_meta, get_filtered_grades_data, plot_altair_histogram
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Grades',
                   initial_sidebar_state='expanded')

grades_data = decrypt_data('data/grades/Grades_enc.csv')

tab1, tab2 = st.tabs(['All classes', 'Single class drilldown'])

with tab1:

    st.markdown('# Grades')

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

    st.markdown('## Comparison of {} of grades by {}'.format(
        grades_aggfunction, grades_drilldown))
    with st.expander('Expand/collapse', expanded=True):
        grades_v_classes_chart = grades_meta(filtered_grades_data,
                                             grades_drilldown,
                                             grades_aggfunction)
        st.altair_chart(grades_v_classes_chart, use_container_width=True)

    st.markdown('## Distribution of grades')
    with st.expander('Expand/collapse', expanded=True):
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

##########################################################################
##########################################################################
##########################################################################

with tab2:
    st.markdown('# Grades')
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

    st.markdown('## Comparison of grades for {}'.format(grades_chosen_class))
    with st.expander('Expand/collapse', expanded=True):
        leftcolmeta, rightcolmeta = st.columns(2)

        with leftcolmeta:
            grades_drilldown_single = st.selectbox(
                label='Split by',
                options=[
                    'Class', 'Hall', 'Term', 'Program', 'Year',
                    'Student leadership'
                ],
                key='grades_drilldown_single',
                index=2)

        with rightcolmeta:
            grades_aggfunction_single = st.selectbox(
                label='Aggregate function',
                options=['mean', 'median'],
                key='grades_aggfunction_single')

        grades_v_classes_chart_single = grades_meta(
            filtered_grades_data_single, grades_drilldown_single,
            grades_aggfunction_single)

        st.altair_chart(grades_v_classes_chart_single,
                        use_container_width=True)
        st.markdown(
            'When you split the chart below by various groups, interpret the results with caution. Since graded classes at LEAF are often small, different leadership positions, years, halls, and programs are often represented by a very small number of students. If a class has one RA (and no other student leaders), and you split the chart by student leadership positions, the result is a comparison between the average grade of that one RA student and the rest of the class.'
        )

    st.markdown('## Distribution of grades for {}'.format(grades_chosen_class))
    with st.expander('Expand/collapse', expanded=True):
        st.info(
            'Hover over the individual bars to show the number of instances (records) for that particular bar (intersection of X and Y axis).'
        )
        st.info(
            'If using a mouse (as opposed to a touchpad), use the scroll wheel to adjust the chart width. Double-click the chart to reset width to default.'
        )

        density_input_single = st.selectbox(
            label='Show as',
            options=['Histogram', 'Density plot'],
            key='density_input_single')

        grades_histogram_chart_single = plot_altair_histogram(
            filtered_grades_data_single, density_input_single, 60)

        st.altair_chart(grades_histogram_chart_single,
                        use_container_width=True)
