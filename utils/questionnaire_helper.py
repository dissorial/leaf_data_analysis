import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import math
import seaborn as sns
from matplotlib import pyplot as plt


def plot_barchart_answers(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('res',
                axis=alt.Axis(
                    gridOpacity=0.5,
                    title='Number of students who chose this answer choice')),
        y=alt.Y('value',
                sort=alt.EncodingSortField(field='res',
                                           op='sum',
                                           order='descending'),
                axis=alt.Axis(labels=False, title='Answer choice')))

    chart_text = chart.mark_text(align='left', baseline='middle',
                                 dx=5).encode(text=alt.Text('value'))

    return (chart + chart_text)


def get_question_data(df, chosen_question):
    studentgrades = df[['Grade']]

    isolated_question_df = df[[chosen_question, 'Grade']]
    split_isolated_df = isolated_question_df[chosen_question].str.split(
        ',', expand=True)

    merged = pd.concat([split_isolated_df, studentgrades], axis=1)

    melted = merged.melt(id_vars=['Grade'])
    melted['res'] = 1

    grouped = melted.groupby(['value']).sum().reset_index()

    return grouped


def get_mean_data(df):
    return round(df[df.columns[0]].mean(), 1)


def get_median_data(df):
    return round(df[df.columns[0]].median(), 1)


def get_std_data(df):
    return round(df[df.columns[0]].std(), 2)


def get_remaining_questions(df, free_response_question_input):
    # return df[[df.columns[5], 'Grade']]
    return df[[free_response_question_input, 'Grade']]


def get_classdata(df, grades):
    return df[df['Grade'].isin(grades)]


def plot_bar_chart_classes(df, aggfunction):

    cols_to_rename = {
        df.columns[1]: 'Standard deviation',
        df.columns[2]: 'Mean',
        df.columns[3]: 'Median'
    }

    df.rename(columns=cols_to_rename, inplace=True)

    df['Standard deviation'] = df['Standard deviation'].round(decimals=1)
    df['Mean'] = df['Mean'].round(decimals=1)
    df['Median'] = df['Median'].round(decimals=1)

    chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(aggfunction),
        x=alt.X('Class',
                axis=alt.Axis(title=None, gridOpacity=0.4),
                sort=alt.EncodingSortField(field=aggfunction,
                                           op='sum',
                                           order='descending')),
        tooltip=['Class', 'Standard deviation', 'Respondents'],
        color=alt.Color('Respondents',
                        scale=alt.Scale(scheme='goldgreen'),
                        legend=alt.Legend(
                            direction='vertical',
                            titleAnchor='middle',
                            gradientThickness=20,
                            gradientLength=250,
                            tickCount=10))).properties(height=600)

    chart_text = chart.mark_text(
        align='left', baseline='middle', dx=-7, fontWeight=400,
        dy=-8).encode(text=alt.Text('{}'.format(aggfunction)))

    return (chart + chart_text)


def sns_violin(df, question):
    fig = plt.figure(figsize=(10, 3))
    chart = sns.violinplot(x=df[question], cut=0)
    chart.set_xlim(0, 10)
    chart.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    return fig
