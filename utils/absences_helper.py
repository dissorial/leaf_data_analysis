import altair as alt
import pandas as pd
import numpy as np


def plot_monthly_absences_count(data, title):
    n_students = data['Student'].unique().tolist()
    df_grouped = data.groupby(['Month']).sum().reset_index()
    df_grouped['avg'] = df_grouped['abs_count'] / len(n_students)

    y_domain = df_grouped['avg'].max()

    chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X('yearmonth(Month):T',
                axis=alt.Axis(tickCount=df_grouped.shape[0], title=None)),
        y=alt.Y('avg',
                scale=alt.Scale(domain=[0, y_domain + 1]),
                axis=alt.Axis(tickMinStep=1,
                              title='Average number of absences'))).properties(
                                  title=title).interactive(bind_y=False)

    return chart


def plot_weekly_absences_count(data, title):
    n_students = data['Student'].unique().tolist()
    domain_pd = pd.to_datetime(['2021-09-01', '2022-06-01'
                                ]).astype(int) / 10**6

    grouped_df = data.groupby(
        [pd.Grouper(key='Attendance Date', freq='W-MON')]).sum().reset_index()
    grouped_df['Avg #n of absences per student'] = grouped_df[
        'abs_count'] / len(n_students)
    ydomain = grouped_df['Avg #n of absences per student'].max()

    chart = alt.Chart(grouped_df).mark_bar(size=20).encode(
        x=alt.X('Attendance Date',
                axis=alt.Axis(tickCount=40,
                              labelAngle=-90,
                              format='%b %d, %y',
                              title=None),
                scale=alt.Scale(domain=list(domain_pd))),
        y=alt.Y('Avg #n of absences per student',
                axis=alt.Axis(tickMinStep=0.5,
                              title='Average number of absences'),
                scale=alt.Scale(domain=[0, ydomain + 0.5]))).properties(
                    title=title).interactive(bind_y=False)

    return chart


def plot_daily_absences_count(data, title):
    n_students = data['Student'].unique().tolist()
    new_df = data.groupby(['Day of Week']).sum().reset_index()
    # new_df['student_count'] = len(all_student_count)
    new_df['avg'] = new_df['abs_count'] / len(n_students)

    chart = alt.Chart(new_df).mark_bar().encode(
        x=alt.X('Day of Week',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                axis=alt.Axis(title=None)),
        y=alt.Y('avg', axis=alt.Axis(
            title='Average number of absences'))).properties(title=title)

    chart_text = chart.mark_text(
        align='left', baseline='middle', dy=15,
        color='white').encode(text=alt.Text('mean(avg):Q', format=',.1f'))

    return (chart + chart_text)


def plot_absences_stacked(data, groupby_column):
    new_df = data.groupby(by=[groupby_column, 'Absence Status']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'abs_count': 'Total number'}, inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(groupby_column, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X('Total number',
                title='Percentage of traffic lights',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Absence Status'),
        tooltip=['Absence Status', 'Total number']).interactive()
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