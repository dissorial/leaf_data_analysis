import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

pd.options.mode.chained_assignment = None


def get_question_data(df, question):
    return df[['Hall', 'Year', 'Term', question]]


def plot_bar_chart(df, x_axis, y_axis, _color, _sort, col, y_domain,
                   aggfunction):

    chart = alt.Chart(df).mark_bar().encode(x=alt.X(
        x_axis,
        aggregate=aggfunction,
        sort=_sort,
        axis=alt.Axis(title='Average number of hours per student'),
        scale=alt.Scale(domain=y_domain)),
                                            y=alt.Y(y_axis,
                                                    axis=alt.Axis(title=None)),
                                            color=alt.Color(_color,
                                                            legend=None),
                                            row=col).properties(width=600)
    return chart


def merge_business_weekend(business, weekend, renamed_question):
    business['Weekday/weekend'] = 'weekday'
    weekend['Weekday/weekend'] = 'weekend'

    business.rename(columns={business.columns[-2]: renamed_question},
                    inplace=True)

    weekend.rename(columns={weekend.columns[-2]: renamed_question},
                   inplace=True)

    return pd.concat([business, weekend])
