import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def preprocess_data(df):

    df['Date assigned'] = pd.to_datetime(df['Date assigned'],
                                         infer_datetime_format=True)
    df['Due date'] = pd.to_datetime(df['Due date'], infer_datetime_format=True)
    df['Month'] = df['Date assigned'].to_numpy().astype('datetime64[M]')
    df['Week'] = df['Date assigned'].to_numpy().astype('datetime64[W]')
    df['Assignment length'] = (df['Due date'] -
                               df['Date assigned']) / np.timedelta64(1, 'D')
    df['Assign_count'] = 1
    return df


def plot_weekly_assignments_count(data):

    xmin = data['Date assigned'].min() - pd.to_timedelta(7, unit='d')
    startYear = xmin.year
    endYear = startYear + 1
    n_students = data['Student'].unique().tolist()

    domain_pd = pd.to_datetime([
        '{}-09-01'.format(startYear), '{}-08-24'.format(endYear)
    ]).astype(int) / 10**6

    grouped_df = data.groupby(
        ['Class', pd.Grouper(key='Date assigned',
                             freq='W-SUN')]).sum().reset_index()
    grouped_df['Avg #n of assignments per student'] = grouped_df[
        'Assign_count'] / len(n_students)
    ydomain = grouped_df['Avg #n of assignments per student'].max()
    grouped_df['Avg length'] = grouped_df['Assignment length'] / grouped_df[
        'Assign_count']

    chart = alt.Chart(grouped_df).mark_bar(size=24).encode(
        x=alt.X('Date assigned',
                axis=alt.Axis(tickCount=50,
                              labelAngle=-90,
                              format='%b %d, %y',
                              title='Week'),
                scale=alt.Scale(domain=list(domain_pd))),
        y=alt.Y('Avg #n of assignments per student',
                axis=alt.Axis(tickMinStep=0.5,
                              title='Average number of assignments'),
                scale=alt.Scale(domain=[0, ydomain + 0.5])),
        color=alt.Color('Avg length',
                        scale=alt.Scale(scheme='turbo'),
                        legend=alt.Legend(
                            direction='vertical',
                            titleAnchor='middle',
                            gradientThickness=20,
                            gradientLength=250,
                            tickCount=10))).properties(height=400).interactive(
                                bind_y=False)

    return chart


def plot_weekly_assignments_duration(data):

    xmin = data['Date assigned'].min()
    xmax = data['Date assigned'].max()
    # n_students = data['Student'].unique().tolist()
    domain_pd = pd.to_datetime([xmin, xmax]).astype(int) / 10**6
    # domain_pd = pd.to_datetime(['2021-09-01', '2022-08-24'
    #                             ]).astype(int) / 10**6

    grouped_df = data.groupby(
        ['Class', pd.Grouper(key='Date assigned',
                             freq='W-SUN')]).mean().reset_index()

    ydomain = grouped_df['Assignment length'].max()

    chart = alt.Chart(grouped_df).mark_bar(size=20).encode(
        x=alt.X('Date assigned',
                axis=alt.Axis(tickCount=grouped_df.shape[0],
                              labelAngle=-90,
                              format='%b %d, %y',
                              title='Week'),
                scale=alt.Scale(domain=list(domain_pd))),
        y=alt.Y('Assignment length',
                axis=alt.Axis(tickMinStep=0.5,
                              title='Average assignment length in days'),
                scale=alt.Scale(domain=[0, ydomain + 0.5]))).properties(
                    height=400).interactive(bind_y=False)

    return chart


def plot_monthly_assignments_count(data):
    # domain_pd = pd.to_datetime(['2021-08-31', '2022-08-24'
    #                             ]).astype(int) / 10**6
    n_students = data['Student'].unique().tolist()
    df_grouped = data.groupby(by=['Class', 'Month']).sum().reset_index()
    df_grouped['avg'] = df_grouped['Assign_count'] / len(n_students)
    df_grouped['Avg length'] = df_grouped['Assignment length'] / df_grouped[
        'Assign_count']
    y_domain = df_grouped['avg'].max()
    chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X(
            'yearmonth(Month):T',
            axis=alt.Axis(tickCount=df_grouped.shape[0], title=None),
        ),
        y=alt.Y('avg',
                scale=alt.Scale(domain=[0, y_domain + 1]),
                axis=alt.Axis(tickMinStep=1,
                              title='Average number of assignments')),
        color=alt.Color('Avg length',
                        scale=alt.Scale(scheme='turbo'),
                        legend=alt.Legend(
                            direction='vertical',
                            titleAnchor='middle',
                            gradientThickness=20,
                            gradientLength=250,
                            tickCount=10))).properties(height=400).interactive(
                                bind_y=False)
    return chart


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