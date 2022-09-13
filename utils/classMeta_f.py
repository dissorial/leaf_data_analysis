import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import joypy


def plot_single_trafficlight(df, x_axis, traffic_light, color):
    chart = alt.Chart(df).mark_bar().encode(x=alt.X(x_axis, sort='-y'),
                                            y=alt.Y(traffic_light,
                                                    aggregate='count'),
                                            color=alt.value(color))
    return chart


def plot_all_trafficlight(data, groupby_column):
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
        tooltip=['Traffic light', 'Total number'])
    return chart


def plot_all_assignments(data, groupby_column):
    new_df = data.groupby(by=[groupby_column, 'variable']).sum()
    new_df.reset_index(inplace=True)
    new_df.rename(columns={
        'variable': 'Assignment status',
        'value': 'Total number'
    },
                  inplace=True)
    chart = alt.Chart(new_df).mark_bar().encode(
        x=groupby_column,
        y=alt.Y('Total number',
                title='Percetange of assignments',
                axis=alt.Axis(format='%'),
                stack='normalize'),
        color='Assignment status',
        tooltip=['Assignment status', 'Total number']).properties(height=500)
    return chart


def plot_all_absences(data):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Class', sort='-y'),
        y=alt.Y('Absence count', aggregate='sum')).properties(height=500)

    chart_text = chart.mark_text(
        align='left', baseline='middle', dx=-7,
        dy=-5).encode(text=alt.Text('sum(Absence count):Q'))
    return (chart + chart_text)


def plot_grades_classes(data):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Class', sort='-y'),
        y=alt.Y('Grade', aggregate='mean',
                scale=alt.Scale(domain=[0, 10]))).properties(height=500)

    chart_text = chart.mark_text(
        align='left', baseline='middle', dx=-7,
        dy=-5).encode(text=alt.Text('mean(Grade):Q', format=',.1f'))
    return (chart + chart_text)


def ridgeline_plot(data, y_axis, x_axis, title):
    fig, axes = joypy.joyplot(data,
                              by=y_axis,
                              column=x_axis,
                              grid=True,
                              linewidth=1,
                              legend=False,
                              linecolor='white',
                              fade=True,
                              overlap=1,
                              alpha=0.4,
                              tails=0,
                              colormap=cm.cool,
                              x_range=[0, 10],
                              range_style='own',
                              title=title,
                              figsize=(5, 3))
    axes[-1].set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return fig


def violin_plot(data, x_axis, y_axis, title):
    fig = plt.figure(figsize=(5, 3))
    chart = sns.violinplot(data=data, x=x_axis, y=y_axis, cut=0, bw=.5)
    chart.set(title=title)
    return fig


def scatter_chart(df, col1, col2):
    scatter = alt.Chart(df).mark_point().encode(
        x=alt.X(col1, scale=alt.Scale(domain=[0, 10])),
        y=col2,
        tooltip=[col1, col2],
    )
    reg = scatter.transform_regression(col1, col2).mark_line()
    return (scatter + reg).interactive()