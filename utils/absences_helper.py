import altair as alt
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from utils.data_load import decrypt_data


def load_data_absences(academicYear):
    if academicYear == '2021/2022':
        return decrypt_data('data/21_22/absences/absences_2122.csv')
    elif academicYear == '2022/2023':
        return decrypt_data('data/22_23/absences/absences_2223.csv')
    else:
        return decrypt_data('data/21_22/absences/absences_2122.csv')


def preprocess(loaded_data):
    loaded_data['Attendance Date'] = pd.to_datetime(
        loaded_data['Attendance Date'], infer_datetime_format=True)

    loaded_data['abs_count'] = 1

    loaded_data['Month'] = loaded_data['Attendance Date'].dt.strftime('%B')
    loaded_data['Week'] = loaded_data['Attendance Date'].dt.strftime(
        '%Y, %m Week %W')
    return loaded_data


def seaborn_barchart_resampe_data(data, resampling_period_column,
                                  values_column):
    n_students = data['Student'].unique().tolist()
    df_grouped = data.groupby([resampling_period_column]).sum().reset_index()
    df_grouped['avg'] = df_grouped[values_column] / len(n_students)
    return df_grouped


def seaborn_barchart_create(data,
                            x_axis,
                            y_axis,
                            x_axis_order=None,
                            rotated_labels=False,
                            chart_ylabel=''):
    fig = plt.figure(figsize=(20, 4))
    chart = sns.barplot(data=data,
                        x=x_axis,
                        y=y_axis,
                        order=x_axis_order,
                        color='lightskyblue')
    if rotated_labels:
        chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    chart.set_xlabel('')
    chart.set_ylabel(chart_ylabel)
    chart.grid()
    chart.spines['top'].set_visible(False)
    chart.spines['right'].set_visible(False)
    chart.spines['bottom'].set_visible(False)
    chart.spines['left'].set_visible(False)

    return chart


def plot_absences_stacked(data, groupby_column):
    new_df = data.groupby(by=[groupby_column, 'Absence Status']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'abs_count': 'Total number'}, inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(groupby_column, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X('Total number',
                title='Percentage of absence status',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Absence Status'),
        tooltip=['Absence Status', 'Total number']).interactive()

    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(groupby_column, axis=alt.Axis(title=None), sort='-x'),
        x=alt.X('Total number',
                title='Percentage of absences',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Absence Status'),
        tooltip=['Absence Status', 'Total number'])
    return chart


def absences_meta(data, drilldown, aggfunction):
    data['absence count'] = 1
    grouped = data.groupby([drilldown, 'Student']).sum().reset_index()

    chart = alt.Chart(grouped).mark_bar().encode(
        y=alt.Y(drilldown, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X('absence count',
                aggregate=aggfunction,
                axis=alt.Axis(tickMinStep=1)))

    chart_text = chart.mark_text(
        align='right', baseline='middle', dx=-7,
        color='white').encode(text=alt.Text(
            '{}(absence count):Q'.format(aggfunction), format=',.1f'))

    return (chart + chart_text)