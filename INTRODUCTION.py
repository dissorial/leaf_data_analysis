import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout="wide",
                   page_title='Introduction',
                   initial_sidebar_state='expanded')

absence_query_img = Image.open('images/absence_query.png')
assignment_query_img = Image.open('images/assignment_query.png')
grades_query_img = Image.open('images/grades_query.png')
traffic_query_img = Image.open('images/traffic_query.png')

st.title('LEAF Academy: Veracross Data Analysis')
st.info(
    'Open the menu in the upper right corner and make sure that "Wide mode" is checked". Feel free to also change the theme color. Light mode is recommended, but dark mode should work fine too.'
)
st.markdown('## 1.0 Data exports from Veracross')

st.markdown(
    '**All data used for this web application considers the 21-22 academic year, meaning data from roughly the start of September 2021 until the end of August 2022**.'
)
with st.expander('Absence query'):
    st.image(absence_query_img)
with st.expander('Assignments query'):
    st.image(assignment_query_img)
with st.expander('Grades query'):
    st.image(grades_query_img)
with st.expander('Traffic lights query'):
    st.image(traffic_query_img)
with st.expander('Other student information'):
    st.markdown(
        "In addition to the above, the following information was added for each student: what hall they live in, whether they're in a 2-year or 4-year program, year (grade), and what (if any) student leadership positions they hold. Since Veracross does not contain some of this information, it was sourced from other places (mostly shared Google Spreadsheets)."
    )

st.markdown('## 1.1 Preprocessing')
st.markdown(
    '- All individual queries above were exported as .csv files, and if necessary, merged with other datasets (such as merging grades data with data about student leadership positions).'
)
st.markdown(
    '- All individual .csv files were then locally preprocessed by a script written in Python.'
)
st.markdown(
    "- During preprocessing, one major transformation was the merging of classes that were otherwise split into multiple groups. For example, certain classes are taught only in one year but split into two or more groups, such as 'AP ENG A' and 'AP ENG B'. These were merged into a single class 'AP ENG' under the assumption that the existence of two groups is the result of too many students enrolled in the class, not a difference in skill level."
)
st.markdown(
    "- Similarly, a single class taught across more years is always shown separately in Veracross. In other words, 'Character Seminar Y4' and 'Character Seminar Y3' are shown separately. This makes perfect sense, but to decluttered the data, I merged such instances into a single class, such as 'Character Semimnar'. Wherever this happens, however, there is an option within the application to filter for individual years, which accomplishes the same goal."
)

st.markdown('## 1.2 How to navigate this web application')
st.markdown(
    '- On the right sidebar, there are four pages you can go through: absences, assignments, grades, and traffic lights. On each page at the top, you can choose whether to view the data from two perspective. One is called "All classes", which considers data from all classes. The other is "Single class drilldown", where you can choose a single class of your interest and view the same/similar data in a more declutter manner.'
)

st.markdown('## 1.3 Data quality')
st.markdown(
    '- Since this dashboard is built with data exported from Veracross, the output quality is in many cases determined by the quality of data entered into Veracross on the part of the user. Since much of the data pertains to classes (assignments, grades, etc.), these users are usually teachers, but can also be non-teaching staffulty for something like absences.'
)
st.markdown(
    '- For example, if a teacher gave students assignments but never changed their status from "Pending" to "Complete", it will be shown as such in this dashboard. In a similar fashion, charts that show the sum or average of assignments can be highly skewed depending on how diligent a particular teacher is with entering class assignments to Veracross. Nothing can be done about this.'
)