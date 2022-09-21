import altair as alt


def plot_altair_histogram(df, chart_type_input, barwidth):

    chart = alt.Chart(df).mark_bar(size=barwidth).encode(
        x=alt.X('Grade',
                scale=alt.Scale(domain=[-0.4, 10.3]),
                axis=alt.Axis(tickCount=20, tickMinStep=0.5)),
        y=alt.Y('count()', axis=alt.Axis(title='Number of instances')),
        tooltip=['Grade', 'count()']).interactive()

    kde = alt.Chart(df).transform_density('Grade', as_=[
        'Grades', 'density'
    ]).mark_area(color='red', opacity=0.3).encode(x='Grades:Q',
                                                  y='density:Q').interactive()

    return (chart if chart_type_input == 'Histogram' else kde)


def get_filtered_grades_data(df, years, terms):
    return df[(df['Year'].isin(years)) & (df['Term'].isin(terms))]


def grades_meta(data, drilldown, aggfunction):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Grade',
                aggregate=aggfunction,
                scale=alt.Scale(domain=[0, 10]),
                axis=alt.Axis(tickMinStep=1)),
        y=alt.Y(drilldown, sort='-x', axis=alt.Axis(title=None)))

    chart_text = chart.mark_text(
        align='right', baseline='middle', dx=-7, color='white').encode(
            text=alt.Text('{}(Grade):Q'.format(aggfunction), format=',.1f'))
    return (chart + chart_text)