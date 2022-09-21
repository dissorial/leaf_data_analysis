import streamlit as st
from utils.traffic_lights_helper import plot_trafficLights_stacked, plot_traffic_meta, get_filtered_traffic_data
from utils.data_load import decrypt_data

st.set_page_config(layout="wide",
                   page_title='Traffic lights',
                   initial_sidebar_state='expanded')

df_wide = decrypt_data('data/traffic/wide_traffic_lights_enc.csv')
df_long = decrypt_data('data/traffic/long_traffic_lights_enc.csv')
# df_wide = pd.read_csv('data/traffic/wide_traffic_lights.csv')
# df_long = pd.read_csv('data/traffic/long_traffic_lights.csv')

#plotting charts
tab1, tab2 = st.tabs(['All classes', 'Single class drilldown'])

with tab1:

    st.markdown('# Traffic lights')

    st.markdown('## Filter and select')
    left_col, middle_col, right_col = st.columns(3)
    with left_col:
        traffic_drilldown = st.selectbox(
            label='Group traffic lights by',
            options=['Class', 'Hall', 'Term', 'Program', 'Year', 'Advisors'],
            key='traffic_drilldown')

    with middle_col:
        filter_traffic_years = st.multiselect(
            label='Years filter',
            options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            key='filter_traffic_years')

    with right_col:
        filter_traffic_terms = st.multiselect(label='Filter terms',
                                              options=['T1', 'T2', 'T3', 'T4'],
                                              default=['T1', 'T2', 'T3', 'T4'],
                                              key='filter_traffic_terms')

    filtered_data_long = get_filtered_traffic_data(df_long,
                                                   filter_traffic_years,
                                                   filter_traffic_terms)

    if (len(filter_traffic_years) == 0 or len(filter_traffic_terms) == 0):
        st.error('Choose at least one year and/or term')
        st.stop()

    all_traffic_chart_stacked = plot_trafficLights_stacked(
        filtered_data_long, traffic_drilldown)

    st.markdown(
        '## Comparison of traffic lights as a percentage of total, grouped by {}'
        .format(traffic_drilldown))
    with st.expander('Expand/collapse', expanded=True):
        st.info(
            'Hover over the stacked bar chart below with your cursor to see the corresponding number of traffic lights belonging to each category.'
        )
        st.info(
            'Use to mouse scroll wheel to zoom in and out; double-click to reset zoom to default.'
        )

        st.altair_chart(all_traffic_chart_stacked, use_container_width=True)

    st.markdown('## Single traffic light drilldown, grouped by {}'.format(
        traffic_drilldown))

    with st.expander('Expand/collapse', expanded=True):
        one, two = st.columns(2)
        with one:
            traffic_aggfunction = st.selectbox(
                label='Aggregate function',
                options=['mean', 'median', 'sum'],
                key='traffic_aggfunction')

        with two:
            traffic_single_selection = st.selectbox(
                label='Traffic light',
                options=['Green', 'Praise', 'Orange', 'Red'],
                key='traffic_single_selection')

        # Fig 2

        filtered_data_wide = get_filtered_traffic_data(df_wide,
                                                       filter_traffic_years,
                                                       filter_traffic_terms)

        single_traffic_chart = plot_traffic_meta(filtered_data_wide,
                                                 traffic_drilldown,
                                                 traffic_single_selection,
                                                 traffic_aggfunction)

        st.altair_chart(single_traffic_chart, use_container_width=True)

with tab2:

    st.markdown('# Traffic lights')

    st.markdown('## Filter and select')
    left_col1, right_col3 = st.columns(2)

    with left_col1:
        filter_traffic_years = st.multiselect(
            label='Years filter',
            options=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            default=['Year 1', 'Year 2', 'Year 3', 'Year 4'],
            key='filter_traffic_years_single')

    with right_col3:
        filter_traffic_terms = st.multiselect(
            label='Filter terms',
            options=['T1', 'T2', 'T3', 'T4'],
            default=['T1', 'T2', 'T3', 'T4'],
            key='filter_traffic_terms_single')

    filtered_data_long = get_filtered_traffic_data(df_long,
                                                   filter_traffic_years,
                                                   filter_traffic_terms)

    filtered_data_wide = get_filtered_traffic_data(df_wide,
                                                   filter_traffic_years,
                                                   filter_traffic_terms)

    if (len(filter_traffic_years) == 0 or len(filter_traffic_terms) == 0):
        st.error('Choose at least one year and/or term')
        st.stop()

    classList_long = filtered_data_long['Class'].unique().tolist()
    classList_wide = filtered_data_wide['Class'].unique().tolist()
    classlist = filtered_data_long['Class'].unique().tolist()

    col1_left, col2_right = st.columns(2)

    with col1_left:
        chosen_class = st.selectbox(label='Choose a class', options=classlist)

    classdata_long = filtered_data_long[filtered_data_long['Class'] ==
                                        chosen_class]
    classdata_wide = filtered_data_wide[filtered_data_wide['Class'] ==
                                        chosen_class]
    # classdata_long = df_long[df_long['Class'] == chosen_class]
    # classdata_wide = df_wide[df_wide['Class'] == chosen_class]

    with col2_right:
        traffic_split_input = st.selectbox(label='Split by',
                                           options=[
                                               'Program', 'Year', 'Hall',
                                               'Student leadership', 'Advisors'
                                           ])

    single_traffic_chart = plot_trafficLights_stacked(classdata_long,
                                                      traffic_split_input)

    st.markdown(
        '## Comparison of traffic lights as a percentage of total for {}'.
        format(chosen_class))
    st.altair_chart(single_traffic_chart, use_container_width=True)

    st.markdown(
        '## Single traffic light drilldown for {}'.format(chosen_class))
    left_two, middle_two = st.columns(2)
    with left_two:
        traffic_light_lineChart_input = st.selectbox(
            label='Traffic light',
            options=['Green', 'Praise', 'Orange', 'Red'],
            key='traffic_light_lineChart_input')

    with middle_two:
        traffic_light_lineChart_aggfunction_input = st.selectbox(
            label='Aggregate function',
            options=['mean', 'median', 'sum'],
            key='traffic_light_lineChart_aggfunction_input')

    signle_traffic_aggreagte = plot_traffic_meta(
        classdata_wide, traffic_split_input, traffic_light_lineChart_input,
        traffic_light_lineChart_aggfunction_input)

    st.altair_chart(signle_traffic_aggreagte, use_container_width=True)
