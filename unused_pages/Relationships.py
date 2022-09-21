import streamlit as st
import pandas as pd
import altair as alt
from utils.unused_charts import scatter_chart
from utils.data_load import get_data, get_classdata

st.set_page_config(layout="wide")

df = get_data()

input_x_axis = st.selectbox(label='X Axis',
                            options=[
                                'Grade', 'Absence count', 'TRF_Green',
                                'TRF_Praise', 'TRF_Orange', 'TRF_Red',
                                'ASG_Count'
                            ],
                            key='xaxis')
input_y_axis = st.selectbox(label='Y Axis',
                            options=[
                                'Grade', 'Absence count', 'TRF_Green',
                                'TRF_Praise', 'TRF_Orange', 'TRF_Red',
                                'ASG_Count'
                            ],
                            key='yaxis',
                            index=1)

chart_one = scatter_chart(df, input_x_axis, input_y_axis)
st.altair_chart(chart_one, use_container_width=True)

binned_scatter = alt.Chart(df).mark_circle().encode(x=alt.X('Grade', bin=True),
                                                    y=alt.Y('Absence count',
                                                            bin=True),
                                                    size='count()')

heatmap = alt.Chart(df).mark_rect().encode(x='Grade:O',
                                           y='Absence count:O',
                                           color='TRF_Green:O')
st.altair_chart(heatmap, use_container_width=True)

st.altair_chart(binned_scatter, use_container_width=True)
