import pandas as pd
import altair as alt
from sklearn.metrics import mean_absolute_error
import streamlit as st


def wide_to_long(df):
    actual_count = df.groupby(['Actual'
                               ]).size().reset_index(name='Actual grade')
    actual_long_format = actual_count.melt(id_vars='Actual',
                                           value_vars='Actual grade',
                                           var_name='Type',
                                           value_name='Count')

    actual_long_format.rename(columns={'Actual': 'Grade'}, inplace=True)

    predicted_count = df.groupby(['Predicted Grade'
                                  ]).size().reset_index(name='Predicted grade')

    predicted_long_format = predicted_count.melt(id_vars='Predicted Grade',
                                                 value_vars='Predicted grade',
                                                 var_name='Type',
                                                 value_name='Count')

    predicted_long_format.rename(columns={'Predicted Grade': 'Grade'},
                                 inplace=True)

    return pd.concat([actual_long_format, predicted_long_format])


def plot_bar_chart_pred_v_actual(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Type:N', title=None, axis=alt.Axis(labelFontSize=16)),
        y=alt.Y('Count', axis=alt.Axis(labelFontSize=16)),
        color=alt.Color('Type:N', legend=None),
        column=alt.Column('Grade:N',
                          header=alt.Header(titleFontSize=16,
                                            labelFontSize=16)),
        tooltip=['Type', 'Count']).properties(width=250)

    return chart


@st.cache
def get_all_classes_mae_df(df):

    n_of_students = df.groupby(['Class'
                                ]).size().reset_index(name='Student count')

    classlist = df['Class'].unique().tolist()

    ers = []
    for c in classlist:
        temp_df = df[df['Class'] == c]
        mae = round(
            mean_absolute_error(temp_df['Actual'], temp_df['Predicted Grade']),
            2)
        ers.append(mae)

    ops = {'Class': classlist, 'mae': ers}
    idk = pd.DataFrame(ops)

    merged = pd.merge(idk,
                      n_of_students,
                      how='left',
                      left_on=['Class'],
                      right_on=['Class'])
    return merged


def plot_mae_all_classes(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('mae', axis=alt.Axis(title='Mean Absolute Error')),
        y=alt.Y('Class', axis=alt.Axis(title=None), sort='x'),
        tooltip=['Class', 'Student count'],
        color=alt.Color('Student count',
                        scale=alt.Scale(scheme='tealblues'),
                        legend=alt.Legend(direction='vertical',
                                          titleAnchor='middle',
                                          gradientThickness=20,
                                          gradientLength=250)))

    return chart


@st.cache
def get_all_correct_predictions_df(df):

    n_of_students = df.groupby(['Class'
                                ]).size().reset_index(name='Student count')

    df = df[df['Actual'] == df['Predicted Grade']]
    n_of_correct = df.groupby(
        ['Class']).size().reset_index(name='Correct predictions')

    merged = pd.merge(n_of_students,
                      n_of_correct,
                      how='left',
                      left_on=['Class'],
                      right_on=['Class']).fillna(0)

    merged['Percent of correct'] = round(
        (merged['Correct predictions'] / merged['Student count']) * 100, 1)

    return merged


def plot_percentage_correct(df):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Percent of correct',
                axis=alt.Axis(title='% of predictions that were correct')),
        y=alt.Y('Class', sort='-x', axis=alt.Axis(title=None)),
        tooltip=['Class', 'Student count', 'Correct predictions'],
        color=alt.Color('Student count',
                        scale=alt.Scale(scheme='tealblues'),
                        legend=alt.Legend(direction='vertical',
                                          titleAnchor='middle',
                                          gradientThickness=20,
                                          gradientLength=250)))

    return chart
