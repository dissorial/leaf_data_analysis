import altair as alt
import pandas as pd


def plot_single_traffic(data, traffic_light, aggfunction, split_by):
    chart = alt.Chart(data).mark_bar().encode(x=alt.X(traffic_light,
                                                      aggregate=aggfunction),
                                              y=alt.Y(split_by,
                                                      title=None,
                                                      sort='-x'),
                                              color=split_by)
    return chart


def plot_trafficLights(data, groupby_column):
    domain = ['TRF_Green', 'TRF_Praise', 'TRF_Orange', 'TRF_Red']
    range_ = ['Green', 'Chartreuse', 'Orange', 'Red']
    new_df = data.groupby(by=[groupby_column, 'variable']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={
        'variable': 'Traffic light',
        'value': 'Total number'
    },
                  inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        x=groupby_column,
        y=alt.Y('Total number',
                title='Percentage of traffic lights',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Traffic light',
                        scale=alt.Scale(domain=domain, range=range_)),
        tooltip=['Traffic light', 'Total number']).properties(height=400,
                                                              width=500)
    return chart


def plot_altair_line_chart_traffic(df, x_axis, y_axis, aggfunction, splitBool):
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x_axis, axis=alt.Axis(grid=True)),
        y=alt.Y(y_axis,
                aggregate=aggfunction,
                axis=alt.Axis(format=',.1f', grid=True),
                title='{} of assignment count'.format(aggfunction)),
        color=alt.Color('variable', legend=alt.Legend(
            title=None)) if splitBool != 'No' else alt.value('blue'))

    return chart


def get_traffic_data_all(data, id_variables):
    value_variables = ['TRF_Green', 'TRF_Praise', 'TRF_Orange', 'TRF_Red']
    df = pd.melt(data, id_vars=id_variables, value_vars=value_variables)
    df = df[df['value'] != 0]

    return df
