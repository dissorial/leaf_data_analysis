import streamlit as st
from utils.data_f import get_classdata, get_data
from utils.classMeta_f import scatter_chart, violin_plot, ridgeline_plot, plot_all_absences, plot_all_assignments, plot_all_trafficlight, plot_grades_classes, plot_single_trafficlight
from utils.traffic_f import get_traffic_data_all
from utils.assignments_f import get_assignments_data_all


st.set_page_config(layout="wide")

#data

csv_data = get_data()

traffic_data = get_traffic_data_all(
    csv_data, ['Class', 'Term', 'Hall', 'Program', 'Year'])

assignments_all_classes_df = get_assignments_data_all(csv_data, ['Class'])

#user inputs
traffic_drilldown = st.selectbox(
    label='Show traffic lights by',
    options=['Class', 'Hall', 'Term', 'Program', 'Year'])

#constructing charts
grades_v_classes_chart = plot_grades_classes(csv_data)

green_traffic_chart = plot_single_trafficlight(csv_data, 'Class', 'TRF_Green',
                                               'Green')

praise_traffic_chart = plot_single_trafficlight(csv_data, 'Class',
                                                'TRF_Praise', 'Chartreuse')

orange_traffic_chart = plot_single_trafficlight(csv_data, 'Class',
                                                'TRF_Orange', 'Orange')
red_traffic_chart = plot_single_trafficlight(csv_data, 'Class', 'TRF_Red',
                                             'Red')

all_traffic_chart = plot_all_trafficlight(traffic_data, traffic_drilldown)

all_assignments_chart = plot_all_assignments(assignments_all_classes_df,
                                             'Class')

all_absences_chart = plot_all_absences(csv_data)

#plotting charts

st.altair_chart(all_traffic_chart, use_container_width=True)
st.altair_chart(all_assignments_chart, use_container_width=True)

# st.altair_chart(green_traffic_chart, use_container_width=True)
# st.altair_chart(praise_traffic_chart, use_container_width=True)
# st.altair_chart(orange_traffic_chart, use_container_width=True)
# st.altair_chart(red_traffic_chart, use_container_width=True)
st.altair_chart(all_absences_chart, use_container_width=True)

st.altair_chart(grades_v_classes_chart, use_container_width=True)
