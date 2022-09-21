import altair as alt
import pandas as pd


def plot_weekly_assignments_count(data):

    n_students = data['Student'].unique().tolist()
    domain_pd = pd.to_datetime(['2021-09-01', '2022-08-24'
                                ]).astype(int) / 10**6

    grouped_df = data.groupby(
        ['Class', pd.Grouper(key='Date assigned',
                             freq='W-MON')]).sum().reset_index()
    grouped_df['Avg #n of assignments per student'] = grouped_df[
        'Assign_count'] / len(n_students)
    ydomain = grouped_df['Avg #n of assignments per student'].max()

    chart = alt.Chart(grouped_df).mark_bar(size=20).encode(
        x=alt.X('Date assigned',
                axis=alt.Axis(tickCount=40,
                              labelAngle=-90,
                              format='%b %d, %y',
                              title='Week'),
                scale=alt.Scale(domain=list(domain_pd))),
        y=alt.Y('Avg #n of assignments per student',
                axis=alt.Axis(tickMinStep=0.5,
                              title='Average number of assignments'),
                scale=alt.Scale(domain=[0, ydomain + 0.5]))).properties(
                    height=400).interactive(bind_y=False)

    return chart


def plot_weekly_assignments_duration(data):

    # n_students = data['Student'].unique().tolist()
    domain_pd = pd.to_datetime(['2021-09-01', '2022-08-24'
                                ]).astype(int) / 10**6

    grouped_df = data.groupby(
        ['Class', pd.Grouper(key='Date assigned',
                             freq='W-MON')]).mean().reset_index()

    ydomain = grouped_df['Assignment length'].max()

    chart = alt.Chart(grouped_df).mark_bar(size=20).encode(
        x=alt.X('Date assigned',
                axis=alt.Axis(tickCount=40,
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

    y_domain = df_grouped['avg'].max()
    chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X(
            'yearmonth(Month):T',
            axis=alt.Axis(tickCount=df_grouped.shape[0], title=None),
        ),
        y=alt.Y(
            'avg',
            scale=alt.Scale(domain=[0, y_domain + 1]),
            axis=alt.Axis(tickMinStep=1,
                          title='Average number of assignments'))).properties(
                              height=400).interactive(bind_y=False)
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