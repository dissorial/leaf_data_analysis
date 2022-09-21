import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import joypy

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
    scatter = alt.Chart(df).mark_point().encode(x=alt.X(
        col1, scale=alt.Scale(domain=[0, 10])),
                                                y=col2,
                                                tooltip=[col1, col2])
    reg = scatter.transform_regression(col1, col2).mark_line()
    return (scatter + reg)
