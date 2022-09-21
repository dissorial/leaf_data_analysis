import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from utils.data_load import get_classdata, get_data
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns

st.set_page_config(layout="wide")

df = get_data()

assignment_features = [
    'ASG_Complete', 'ASG_Complete/No Credit', 'ASG_Incomplete', 'ASG_Late',
    'ASG_Late complete', 'ASG_Not turned in', 'ASG_Turned in/Not graded'
]

traffic_features = ['TRF_Green', 'TRF_Praise', 'TRF_Orange', 'TRF_Red']
other_numeric_features = ['Absence count']

assignment_input = st.sidebar.multiselect(label='Assign',
                                          options=assignment_features,
                                          default=assignment_features)

traffic_input = st.sidebar.multiselect(label='traffic',
                                       options=traffic_features,
                                       default=traffic_features)

other_input = st.sidebar.multiselect(label='other',
                                     options=other_numeric_features,
                                     default=other_numeric_features)

features_input = assignment_input + traffic_input + other_input

# ts_input = st.sidebar.number_input(
#     "Training data size",
#     min_value=0.5,
#     max_value=0.9,
#     step=0.05,
#     value=0.75,
# )

crit_input = st.sidebar.selectbox(
    "Function to measure the quality of a split",
    ["gini", "entropy"],
)

splitter_input = st.sidebar.selectbox(
    "Strategy used to choose the split at each node",
    ["best", "random"],
)

depth_input = st.sidebar.selectbox(
    "Maximum tree depth",
    [None, 2, 3, 4, 5, 6],
)

sample_split_input = st.sidebar.number_input(
    'Min. #n of node samples to split internal node',
    min_value=2,
    max_value=10,
    step=1,
    value=2)

leaf_samples_input = st.sidebar.number_input(
    'Min. #n of samples needed for a leaf node',
    min_value=1,
    max_value=10,
    step=1,
    value=1)

X = df[features_input]
y = df['Grade']

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.25,
                                                    random_state=30)


def create_model():
    model = DecisionTreeClassifier(criterion=crit_input,
                                   random_state=0,
                                   max_depth=depth_input,
                                   splitter=splitter_input,
                                   min_samples_split=sample_split_input,
                                   min_samples_leaf=leaf_samples_input)

    model.fit(X_train, y_train)
    return model


def get_confusion_matrix():
    return confusion_matrix(y_test, y_pred)


def calculate_accuracy():
    return np.round((model.score(X_test, y_test) * 100), 2)


model = create_model()

y_pred = model.predict(X_test)

testAcc = calculate_accuracy()
st.write('Model classification accuracy is {}'.format(testAcc))

importances_data = {
    'Feature name': features_input,
    'Feature importance': model.feature_importances_
}

feature_importances = pd.DataFrame(data=importances_data)

feature_chart = alt.Chart(feature_importances).mark_bar().encode(
    x=alt.X('Feature name:N', sort='-y'),
    y='Feature importance:Q',
    tooltip=['Feature name', 'Feature importance']).properties(height=500)

left, right = st.columns(2)

with right:
    st.altair_chart(feature_chart, use_container_width=True)

with left:
    labelY, lebelX = np.unique(y_test), np.unique(y_pred)
    cm = get_confusion_matrix()
    labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    labelY, labelX = cm.shape[0], cm.shape[1]
    ax = sns.heatmap(cm, annot=True, fmt='g')
    ax.set_title('Predicted vs actual')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    # ax.set_xticklabels(labels[:labelX])
    # ax.set_yticklabels(labels[:labelY])
    st.pyplot(ax.figure)