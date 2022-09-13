import altair as alt
import pandas as pd

def plot_assignments_stacked(data, groupby_column):
    new_df = data.groupby(by=[groupby_column, 'variable']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={
        'variable': 'Assignment status',
        'value': 'Total number'
    },
                  inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        x=alt.X(groupby_column, title=None),
        y=alt.Y('Total number',
                title='Percetange of assignments',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color=alt.Color('Assignment status', legend=alt.Legend(title=None)),
        tooltip=['Assignment status', 'Total number']).properties(height=400)
    return chart


def plot_assignments_default(data, groupby_column, assignment_status):
    new_df = data.groupby(by=[groupby_column, 'variable']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={
        'variable': 'Assignment status',
        'value': 'Total number'
    },
                  inplace=True)
    new_df = new_df[new_df['Assignment status'] == assignment_status]
    chart = alt.Chart(new_df).mark_bar().encode(
        x=alt.X(groupby_column, title=None),
        y=alt.Y('Total number', title='Number of assignments'),
        column='Assignment status',
        color=alt.Color(groupby_column, legend=alt.Legend(title=None)),
        tooltip=['Assignment status', 'Total number']).properties(width=350)
    return chart


def plot_altair_line_chart_assignments(df, x_axis, y_axis, aggfunction,
                                       splitBool):
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x_axis, axis=alt.Axis(grid=True)),
        y=alt.Y(y_axis,
                aggregate=aggfunction,
                axis=alt.Axis(format=',.1f', grid=True),
                title='{} of assignment count'.format(aggfunction)),
        color=alt.Color('variable', legend=alt.Legend(
            title=None)) if splitBool != 'No' else alt.value('blue'))

    return chart

def get_assignments_data_all(data, id_variables):
    value_variables = [
        'ASG_Complete', 'ASG_Complete/No Credit', 'ASG_Incomplete', 'ASG_Late',
        'ASG_Late complete', 'ASG_Not turned in', 'ASG_Turned in/Not graded'
    ]

    df = pd.melt(data, id_vars=id_variables, value_vars=value_variables)
    df = df[df['value'] != 0]

    return df