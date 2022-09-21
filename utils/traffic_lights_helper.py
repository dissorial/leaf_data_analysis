import altair as alt
import pandas as pd


def get_filtered_traffic_data(df, filter_years, filter_terms):
    return df[(df['Year'].isin(filter_years))
              & (df['Term'].isin(filter_terms))]


def plot_trafficLights_stacked(data, groupby_column):
    domain = ['Green', 'Praise', 'Orange', 'Red']
    range_ = ['Green', 'Blue', 'Orange', 'Red']
    new_df = data.groupby(by=[groupby_column, 'Traffic light']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={'count': 'Total number'}, inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(groupby_column, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X('Total number',
                title='Percentage of traffic lights',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Traffic light',
                        scale=alt.Scale(domain=domain, range=range_)),
        tooltip=['Traffic light', 'Total number']).interactive()
    return chart


def plot_traffic_meta(df, drilldown, traffic_light, aggfunction):
    colors = {
        'Green': 'Green',
        'Praise': 'Blue',
        'Orange': 'Orange',
        'Red': 'Red'
    }

    new_df = df.groupby([drilldown, 'Student']).sum().reset_index()
    chart = alt.Chart(new_df).mark_bar().encode(
        y=alt.Y(drilldown, sort='-x', axis=alt.Axis(title=None)),
        x=alt.X(traffic_light, aggregate=aggfunction),
        color=alt.value(colors[traffic_light])).properties(
            title="Single traffic light drilldown (Fig 2)")

    chart_text = chart.mark_text(
        align='left', baseline='middle', dx=5,
        color='white').encode(text=alt.Text(
            '{}({}):Q'.format(aggfunction, traffic_light), format=',.1f'))

    return (chart + chart_text)