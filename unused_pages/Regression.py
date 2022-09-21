import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from utils.data_load import get_classdata, get_data

st.set_page_config(layout="wide")

df = get_data()

sc = StandardScaler()

assignment_features = [
    'ASG_Complete', 'ASG_Complete/No Credit', 'ASG_Incomplete', 'ASG_Late',
    'ASG_Late complete', 'ASG_Not turned in', 'ASG_Turned in/Not graded'
]

traffic_features = ['TRF_Green', 'TRF_Praise', 'TRF_Orange', 'TRF_Red']

other_numeric_features = ['Absence count']

features_input = assignment_features + traffic_features + other_numeric_features

ts_input = 0.75

X = df[features_input]
y = df['Grade']

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=1 - ts_input,
                                                    random_state=30)

X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

try:
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
except ValueError:
    st.button('Click here to run the algorithm and create a model')
    st.stop()

pepe = pd.DataFrame({'actual': y_test, 'predicted': y_pred})
pepe.reset_index(inplace=True, drop=True)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(pepe)
ax.set_xticklabels('')
ax.set_ylabel('Time amount')
ax.set_title('Predicted vs. actual values')
ax.legend(['actual', 'predicted'], prop={'size': 6})
ax.grid(linestyle='--', linewidth=0.5)
st.markdown('# Chart of predicted vs. actual values')
with st.expander('Expand to see...'):
    st.markdown(
        "_If the predicted values seem suspiciously accurate and you're wondering why, read the sections above._"
    )
    st.pyplot(fig)

f_names = pd.DataFrame(model.coef_, X.columns, columns=['Coefficients'])
plt.figure()
coeffs_chart = (f_names['Coefficients'].sort_values(ascending=True).plot(
    kind='barh', xlabel='', figsize=(10, 5)))
coeffs_chart.grid(linestyle="--", linewidth=0.5)
coeffs_chart.set_title('Feature coefficients')

st.markdown('# Chart of feature coefficients')
with st.expander('Expand to see...'):
    st.pyplot(coeffs_chart.figure)


def mse():
    return np.round(mean_squared_error(y_test, y_pred, squared=True), 2)


def rmse():
    return np.round(mean_squared_error(y_test, y_pred, squared=False), 2)


def mae():
    return np.round(mean_absolute_error(y_test, y_pred), 2)


st.markdown('# Model metrics')
with st.expander('Expand to see...'):
    a, b, c = st.columns(3)
    with a:
        st.info('**Mean squared error:** {}'.format(mse()))
    with b:
        st.info('**Root mean squared error:** {}'.format(rmse()))
    with c:
        st.info('**Mean absolute error:** {}'.format(mae()))
