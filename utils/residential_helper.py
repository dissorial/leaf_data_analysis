import pandas as pd
import altair as alt

pd.options.mode.chained_assignment = None


def get_question_data(df, question):
    return df[['Hall', 'Year', 'Term', question]]


def plot_bar_chart(df,
                   x_axis,
                   y_axis,
                   _color,
                   _sort,
                   col,
                   y_domain,
                   aggfunction,
                   axis_title='Average number of hours per student',
                   w=550):

    chart_def = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_axis,
                aggregate=aggfunction,
                sort=_sort,
                axis=alt.Axis(title=axis_title),
                scale=alt.Scale(domain=y_domain)),
        y=alt.Y(y_axis, axis=alt.Axis(title=None), sort=_sort),
        color=alt.Color(_color, legend=None),
    ).properties(width=w)

    chart_row = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_axis,
                aggregate=aggfunction,
                sort=_sort,
                axis=alt.Axis(title=axis_title),
                scale=alt.Scale(domain=y_domain)),
        y=alt.Y(y_axis, axis=alt.Axis(title=None), sort=_sort),
        color=alt.Color(_color, legend=None),
        row=col).properties(width=w)

    return chart_def if col == 'None' else chart_row


def merge_business_weekend(business, weekend, renamed_question):
    business['Weekday/weekend'] = 'weekday'
    weekend['Weekday/weekend'] = 'weekend'

    business.rename(columns={business.columns[-2]: renamed_question},
                    inplace=True)

    weekend.rename(columns={weekend.columns[-2]: renamed_question},
                   inplace=True)

    return pd.concat([business, weekend])
