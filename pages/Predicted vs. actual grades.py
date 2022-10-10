import streamlit as st
from sklearn.metrics import mean_absolute_error
from utils.predicted_helper import wide_to_long, plot_bar_chart_pred_v_actual, get_all_classes_mae_df, get_all_correct_predictions_df, plot_percentage_correct, plot_mae_all_classes
from utils.data_load import decrypt_data
from scipy import stats

st.set_page_config(layout="wide",
                   page_title='Predicted vs. actdual grades',
                   initial_sidebar_state='expanded')

df = decrypt_data('data/21_22/pred/pred_v_actual_2122.csv')

all_classes = df['Class'].unique().tolist()
class_options = ['All classes'] + all_classes

st.markdown('# Predicted vs. actual grades for the 21/22 academic year')

all_classes_mae_df = get_all_classes_mae_df(df)
all_correct_predictions_df = get_all_correct_predictions_df(df)

mae_chart = plot_mae_all_classes(all_classes_mae_df)
percentage_correct_chart = plot_percentage_correct(all_correct_predictions_df)

kendall_tau = stats.kendalltau(df['Predicted Grade'], df['Actual'])

class_filter = st.selectbox(label='Class filter',
                            options=class_options,
                            key='class_filter')

if class_filter != 'All classes':
    df = df[df['Class'] == class_filter]
else:
    pass

one, two, three = st.columns(3)

st.markdown(
    '## Predicted vs. actual grades distribution: {}'.format(class_filter))

long_grades_format = wide_to_long(df)

bar_chart_pred_v_actual = plot_bar_chart_pred_v_actual(long_grades_format)
st.altair_chart(bar_chart_pred_v_actual)

with one:
    average_actual = round(df['Actual'].mean(), 2)
    st.metric(label='Acutal grades average', value=average_actual)

with two:
    average_predicted = round(df['Predicted Grade'].mean(), 2)
    st.metric(label='Predicted grades average', value=average_predicted)

with one:
    median_actual = round(df['Actual'].median(), 2)
    st.metric(label='Actual grades median', value=median_actual)

with two:
    median_predicted = round(df['Predicted Grade'].median(), 2)
    st.metric(label='Predicted grades median', value=median_predicted)

with one:
    std_actual = round(df['Actual'].std(), 2)
    st.metric(label='Standard deviation of actual grades', value=std_actual)

with two:
    std_predicted = round(df['Predicted Grade'].std(), 2)
    st.metric(label='Standard deviation of predicted grades',
              value=std_predicted)

with three:
    mae = round(mean_absolute_error(df['Actual'], df['Predicted Grade']), 2)
    st.metric(label='Mean absolute error', value=mae)
    st.markdown(
        'Mean absoluate error calculated as the sum of the absolute value of difference between actual and predicted grades, divided by the number of students in the chosen class.'
    )

with three:
    number_of_correct_predictions = df[df['Actual'] ==
                                       df['Predicted Grade']].shape[0]
    st.metric(label='Correct predictdions',
              value='{} out of {}'.format(number_of_correct_predictions,
                                          df.shape[0]))

with st.expander('Percetange of correct predictions across all classes',
                 expanded=True):
    st.info('Hover over the chart for additional information')
    st.altair_chart(percentage_correct_chart, use_container_width=True)

with st.expander('Mean absolute error of predictions across all classes',
                 expanded=True):
    st.info('Hover over the chart for additional information')
    st.altair_chart(mae_chart, use_container_width=True)

with st.expander("Other metrics (only applies to data for all classes)",
                 expanded=True):
    other_metrics_left, other_metrics_right = st.columns(2)

    with other_metrics_left:
        st.metric(label="Correlation (Kendall Tau)",
                  value=round(kendall_tau.correlation, 2))
    with other_metrics_right:
        st.metric(label='p-value', value='<0.01')
