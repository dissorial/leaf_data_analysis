import altair as alt


def plot_absences(data, y_axis, agg_function, w, h):
    chart = alt.Chart(data).mark_bar().encode(x=alt.X('Absence count',
                                                      aggregate=agg_function),
                                              y=alt.Y(y_axis,
                                                      title=None,
                                                      sort='-x'),
                                              color=y_axis).properties(
                                                  width=w, height=h)
    return chart