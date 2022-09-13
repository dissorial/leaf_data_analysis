import altair as alt


def plot_altair_line_chart(df, x_axis, y_axis, aggfunction, groupby):
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(x_axis, axis=alt.Axis(grid=True)),
        y=alt.Y(y_axis,
                aggregate=aggfunction,
                axis=alt.Axis(format=',.1f', grid=True)),
        color=alt.Color(groupby)
        if groupby != 'No grouping' else alt.value('blue'))
    return chart


def plot_class_charts(data, y_axis, agg_function, w, h):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Grade',
                aggregate=agg_function,
                scale=alt.Scale(domain=[0, 10])),
        y=alt.Y(y_axis, title=None, sort='-x'),
        color=y_axis).properties(width=w, height=h)
    return chart


def plot_altair_histogram(df, chart_type_input, chosen_terms, title):

    if (chosen_terms != 'All'):
        df = df[df['Term'] == chosen_terms]
    else:
        pass
    chart = alt.Chart(df).mark_bar(size=30).encode(
        x=alt.X('Grade'),
        y=alt.Y('count()', axis=alt.Axis(title='Number of instances')),
        tooltip=['Grade', 'count()']).properties(title=title).interactive()

    kde = alt.Chart(df).transform_density(
        'Grade',
        as_=['Grades', 'density']).mark_area(color='red', opacity=0.3).encode(
            x='Grades:Q', y='density:Q').properties(title=title).interactive()

    return (chart if chart_type_input == 'Histogram' else kde)