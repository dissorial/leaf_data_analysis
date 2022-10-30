import streamlit as st
from utils.assignments_helper import plot_all_assignments_stacked, assignments_meta, preprocess_data
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Assignments: all classes',
                   initial_sidebar_state='expanded')

initial_21_22 = decrypt_data('data/21_22/assignments/assignments_2122.csv')
initial_22_23 = decrypt_data('data/22_23/assignments/assignments_2223.csv')

st.markdown('# Assignments: all classes')

col1_assign, col2_assign, col3_assign = st.columns(3)

with col1_assign:
    assign_drilldown = st.selectbox(label='Show assignments by',
                                    options=[
                                        'Class', 'Hall', 'Term', 'Program',
                                        'Year', 'Student leadership',
                                        'Advisors'
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

with st.sidebar:
    academic_year = st.selectbox(label='Academic year',
                                 options=['2021/2022', '2022/2023'],
                                 key='academic_year')

pre_2122 = preprocess_data(initial_21_22)
pre_2223 = preprocess_data(initial_22_23)

assignments_data_datetime = pre_2122 if academic_year == '2021/2022' else pre_2223

classlist = assignments_data_datetime['Class'].unique().tolist()

c_left, c_right = st.columns([2, 1])

available_status_all = assignments_data_datetime['Completion Status'].unique(
).tolist()
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
        or len(filter_assign_status) == 0 or len(filter_assign_display) == 0):
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

tab_status, tab_number = st.tabs(
    ['Assignments by status', 'Assignments by count'])

with tab_status:
    assignments_stacked_chart = plot_all_assignments_stacked(
        filtered_assignment_data, assign_drilldown)

    with st.expander('Some additional information and explanation'):
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

with tab_number:
    st.markdown('## Comparison of number of assignments, grouped by {}'.format(
        assign_drilldown))

    assign_aggfunction = st.selectbox(label='Aggregate function',
                                      options=['mean', 'median'],
                                      key='assign_aggfunction')

    assignments_meta_chart = assignments_meta(filtered_assignment_data,
                                              assign_drilldown,
                                              assign_aggfunction)
    st.altair_chart(assignments_meta_chart, use_container_width=True)
