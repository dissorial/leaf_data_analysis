import altair as alt
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils.data_load import decrypt_data


def load_data_assignments(academicYear):
    if academicYear == '2021/2022':
        return decrypt_data('data/21_22/assignments/assignments_2122.csv')
    elif academicYear == '2022/2023':
        return decrypt_data('data/22_23/assignments/assignments_2223.csv')
    else:
        return decrypt_data('data/21_22/assignments/assignments_2122.csv')


def resample_test(data,
                  resampling_period_column,
                  values_column,
                  duration=False):
    n_students = data['Student'].unique().tolist()
    df_grouped = data.groupby([resampling_period_column,
                               'Class']).sum().reset_index()
    if duration:
        df_grouped['avg'] = df_grouped['Assignment length'] / df_grouped[
            values_column]
    else:
        df_grouped['avg'] = df_grouped[values_column] / len(n_students)
    return df_grouped


def seaborn_barchart_resampe_data(data,
                                  resampling_period_column,
                                  values_column,
                                  duration=False):
    n_students = data['Student'].unique().tolist()
    df_grouped = data.groupby([resampling_period_column]).sum().reset_index()
    if duration:
        df_grouped['avg'] = df_grouped['Assignment length'] / df_grouped[
            values_column]
    else:
        df_grouped['avg'] = df_grouped[values_column] / len(n_students)
    return df_grouped


def seaborn_barchart_create(data,
                            x_axis,
                            y_axis,
                            x_axis_order=None,
                            rotated_labels=False,
                            chart_ylabel='',
                            hue_input=None):
    fig = plt.figure(figsize=(20, 4))
    chart = sns.barplot(data=data,
                        x=x_axis,
                        y=y_axis,
                        order=x_axis_order,
                        color='lightskyblue',
                        hue=hue_input)
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


def preprocess_data(df):

    df['Date assigned'] = pd.to_datetime(df['Date assigned'],
                                         infer_datetime_format=True)
    df['Due date'] = pd.to_datetime(df['Due date'], infer_datetime_format=True)
    # df['Month'] = df['Date assigned'].to_numpy().astype('datetime64[M]')
    df['Month'] = df['Date assigned'].dt.strftime('%B')
    df['Week'] = df['Date assigned'].dt.strftime('%Y, %m Week %W')
    # df['Week'] = df['Date assigned'].to_numpy().astype('datetime64[W]')
    df['Assignment length'] = (df['Due date'] -
                               df['Date assigned']) / np.timedelta64(1, 'D')
    df['Assign_count'] = 1
    return df


def plot_monthly_assignment_duration(data):
    new_df = data.groupby(['Class', 'Month']).mean().reset_index()

    y_domain = new_df['Assignment length'].max()
    chart = alt.Chart(new_df).mark_bar().encode(
        x=alt.X('yearmonth(Month):T',
                axis=alt.Axis(tickCount=new_df.shape[0], title='Month')),
        y=alt.Y('Assignment length',
                axis=alt.Axis(tickMinStep=1,
                              title='Average assignment length in days'),
                scale=alt.Scale(domain=[0, y_domain + 0.5]))).properties(
                    height=400).interactive(bind_y=False)

    return chart


def plot_all_assignments_stacked(data, groupby_column):
    new_df = data.groupby(by=[groupby_column, 'Completion Status']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'Assign_count': 'Total number'}, inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(groupby_column, axis=alt.Axis(title=None)),
        x=alt.X('Total number',
                title='Percetange of assignments',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color='Completion Status',
        tooltip=['Completion Status', 'Total number']).interactive()
    return chart


def assignments_meta(data, drilldown, aggfunction):

    grouped = data.groupby([drilldown, 'Student']).sum().reset_index()

    chart = alt.Chart(grouped).mark_bar().encode(
        y=alt.Y(drilldown, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X('Assign_count', aggregate=aggfunction))

    chart_text = chart.mark_text(
        align='right', baseline='middle', dx=-7,
        color='white').encode(text=alt.Text(
            '{}(Assign_count):Q'.format(aggfunction), format=',.0f'))

    return (chart + chart_text)